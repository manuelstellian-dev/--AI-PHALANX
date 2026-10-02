"""
polis.crypto — ΛΕΩΝΙΔΑΣ's own cryptography (replaces `cryptography`).

Implemented from the primary specifications, using only the standard library:

- AES-128/192/256 block cipher ........ FIPS-197
- GCM authenticated encryption ......... NIST SP 800-38D
- HKDF-SHA256 key derivation ........... RFC 5869 (on stdlib hmac/hashlib)
- Fernet tokens (legacy vault format) .. Fernet specification (AES-128-CBC + HMAC-SHA256)

The AES S-box is *derived* (multiplicative inverse in GF(2^8) followed by the
FIPS-197 affine transform), not transcribed, so a table typo is impossible.
Correctness is pinned by the official FIPS-197 / GCM test vectors in
tests/test_crypto.py.

Residual risk (DEC-022): an interpreted implementation with table lookups and
data-dependent branches is not constant-time; cache-timing side channels are
possible for a co-located attacker. Accepted under the air-gapped,
single-tenant threat model. Tag comparison uses hmac.compare_digest.
"""

import base64
import hashlib
import hmac
import os
import secrets
import struct
import time
from typing import List, Optional


class InvalidTag(Exception):
    """Authentication failed: wrong key, tampered data or wrong associated data."""


class InvalidToken(Exception):
    """A Fernet token is malformed or failed authentication."""


# --------------------------------------------------------------- GF(2^8)

def _gf_mul(a: int, b: int) -> int:
    """Multiply in GF(2^8) modulo x^8 + x^4 + x^3 + x + 1."""
    result = 0
    while b:
        if b & 1:
            result ^= a
        a = ((a << 1) ^ 0x11B) if a & 0x80 else (a << 1)
        b >>= 1
    return result


def _derive_sbox():
    """S(x) = affine(x^-1) per FIPS-197 §5.1.1; S(0) = 0x63."""
    inverse = [0] * 256
    for x in range(1, 256):
        for y in range(1, 256):
            if _gf_mul(x, y) == 1:
                inverse[x] = y
                break
    sbox = []
    for x in range(256):
        b = inverse[x]
        s = b
        for shift in range(1, 5):
            s ^= ((b << shift) | (b >> (8 - shift))) & 0xFF
        sbox.append(s ^ 0x63)
    inv_sbox = [0] * 256
    for i, s in enumerate(sbox):
        inv_sbox[s] = i
    return sbox, inv_sbox


SBOX, INV_SBOX = _derive_sbox()

# Encryption T-tables: Te0[x] = (2s, s, s, 3s) packed big-endian; Te1..3 are rotations
_TE = [[0] * 256 for _ in range(4)]
_TD = [[0] * 256 for _ in range(4)]
for _x in range(256):
    _s = SBOX[_x]
    _w = (_gf_mul(_s, 2) << 24) | (_s << 16) | (_s << 8) | _gf_mul(_s, 3)
    _i = INV_SBOX[_x]
    _wd = (_gf_mul(_i, 14) << 24) | (_gf_mul(_i, 9) << 16) | (_gf_mul(_i, 13) << 8) | _gf_mul(_i, 11)
    for _r in range(4):
        _TE[_r][_x] = ((_w >> (8 * _r)) | (_w << (32 - 8 * _r))) & 0xFFFFFFFF
        _TD[_r][_x] = ((_wd >> (8 * _r)) | (_wd << (32 - 8 * _r))) & 0xFFFFFFFF
_RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


def _inv_mix_word(w: int) -> int:
    """InvMixColumns applied to one 32-bit column (used for decryption round keys)."""
    b = [(w >> 24) & 0xFF, (w >> 16) & 0xFF, (w >> 8) & 0xFF, w & 0xFF]
    out = 0
    for row in range(4):
        coeffs = (14, 11, 13, 9)[-row:] + (14, 11, 13, 9)[:-row] if row else (14, 11, 13, 9)
        v = 0
        for c, byte in zip(coeffs, b):
            v ^= _gf_mul(byte, c)
        out = (out << 8) | v
    return out


class AES:
    """
    AES block cipher (FIPS-197) with 128-, 192- or 256-bit keys.

    Attributes:
        rounds: Nr (10, 12 or 14)
    """

    def __init__(self, key: bytes):
        if len(key) not in (16, 24, 32):
            raise ValueError("AES key must be 16, 24 or 32 bytes")
        nk = len(key) // 4
        self.rounds = nk + 6
        words = list(struct.unpack(f">{nk}I", key))
        for i in range(nk, 4 * (self.rounds + 1)):
            t = words[i - 1]
            if i % nk == 0:
                t = ((t << 8) | (t >> 24)) & 0xFFFFFFFF  # RotWord
                t = (SBOX[t >> 24] << 24) | (SBOX[(t >> 16) & 0xFF] << 16) | \
                    (SBOX[(t >> 8) & 0xFF] << 8) | SBOX[t & 0xFF]
                t ^= _RCON[i // nk - 1] << 24
            elif nk > 6 and i % nk == 4:
                t = (SBOX[t >> 24] << 24) | (SBOX[(t >> 16) & 0xFF] << 16) | \
                    (SBOX[(t >> 8) & 0xFF] << 8) | SBOX[t & 0xFF]
            words.append(words[i - nk] ^ t)
        self._enc = words
        # Equivalent inverse cipher key schedule (FIPS-197 §5.3.5)
        dec = []
        for r in range(self.rounds, -1, -1):
            block = words[4 * r:4 * r + 4]
            if 0 < r < self.rounds:
                block = [_inv_mix_word(w) for w in block]
            dec.extend(block)
        self._dec = dec

    def encrypt_block(self, block: bytes) -> bytes:
        """Encrypt one 16-byte block."""
        te0, te1, te2, te3 = _TE
        k = self._enc
        s0, s1, s2, s3 = struct.unpack(">4I", block)
        s0 ^= k[0]
        s1 ^= k[1]
        s2 ^= k[2]
        s3 ^= k[3]
        for r in range(1, self.rounds):
            o = 4 * r
            t0 = te0[s0 >> 24] ^ te1[(s1 >> 16) & 0xFF] ^ te2[(s2 >> 8) & 0xFF] ^ te3[s3 & 0xFF] ^ k[o]
            t1 = te0[s1 >> 24] ^ te1[(s2 >> 16) & 0xFF] ^ te2[(s3 >> 8) & 0xFF] ^ te3[s0 & 0xFF] ^ k[o + 1]
            t2 = te0[s2 >> 24] ^ te1[(s3 >> 16) & 0xFF] ^ te2[(s0 >> 8) & 0xFF] ^ te3[s1 & 0xFF] ^ k[o + 2]
            t3 = te0[s3 >> 24] ^ te1[(s0 >> 16) & 0xFF] ^ te2[(s1 >> 8) & 0xFF] ^ te3[s2 & 0xFF] ^ k[o + 3]
            s0, s1, s2, s3 = t0, t1, t2, t3
        o = 4 * self.rounds
        sb = SBOX
        out = (
            ((sb[s0 >> 24] << 24) | (sb[(s1 >> 16) & 0xFF] << 16) | (sb[(s2 >> 8) & 0xFF] << 8) | sb[s3 & 0xFF]) ^ k[o],
            ((sb[s1 >> 24] << 24) | (sb[(s2 >> 16) & 0xFF] << 16) | (sb[(s3 >> 8) & 0xFF] << 8) | sb[s0 & 0xFF]) ^ k[o + 1],
            ((sb[s2 >> 24] << 24) | (sb[(s3 >> 16) & 0xFF] << 16) | (sb[(s0 >> 8) & 0xFF] << 8) | sb[s1 & 0xFF]) ^ k[o + 2],
            ((sb[s3 >> 24] << 24) | (sb[(s0 >> 16) & 0xFF] << 16) | (sb[(s1 >> 8) & 0xFF] << 8) | sb[s2 & 0xFF]) ^ k[o + 3],
        )
        return struct.pack(">4I", *out)

    def decrypt_block(self, block: bytes) -> bytes:
        """Decrypt one 16-byte block (equivalent inverse cipher)."""
        td0, td1, td2, td3 = _TD
        k = self._dec
        s0, s1, s2, s3 = struct.unpack(">4I", block)
        s0 ^= k[0]
        s1 ^= k[1]
        s2 ^= k[2]
        s3 ^= k[3]
        for r in range(1, self.rounds):
            o = 4 * r
            t0 = td0[s0 >> 24] ^ td1[(s3 >> 16) & 0xFF] ^ td2[(s2 >> 8) & 0xFF] ^ td3[s1 & 0xFF] ^ k[o]
            t1 = td0[s1 >> 24] ^ td1[(s0 >> 16) & 0xFF] ^ td2[(s3 >> 8) & 0xFF] ^ td3[s2 & 0xFF] ^ k[o + 1]
            t2 = td0[s2 >> 24] ^ td1[(s1 >> 16) & 0xFF] ^ td2[(s0 >> 8) & 0xFF] ^ td3[s3 & 0xFF] ^ k[o + 2]
            t3 = td0[s3 >> 24] ^ td1[(s2 >> 16) & 0xFF] ^ td2[(s1 >> 8) & 0xFF] ^ td3[s0 & 0xFF] ^ k[o + 3]
            s0, s1, s2, s3 = t0, t1, t2, t3
        o = 4 * self.rounds
        ib = INV_SBOX
        out = (
            ((ib[s0 >> 24] << 24) | (ib[(s3 >> 16) & 0xFF] << 16) | (ib[(s2 >> 8) & 0xFF] << 8) | ib[s1 & 0xFF]) ^ k[o],
            ((ib[s1 >> 24] << 24) | (ib[(s0 >> 16) & 0xFF] << 16) | (ib[(s3 >> 8) & 0xFF] << 8) | ib[s2 & 0xFF]) ^ k[o + 1],
            ((ib[s2 >> 24] << 24) | (ib[(s1 >> 16) & 0xFF] << 16) | (ib[(s0 >> 8) & 0xFF] << 8) | ib[s3 & 0xFF]) ^ k[o + 2],
            ((ib[s3 >> 24] << 24) | (ib[(s2 >> 16) & 0xFF] << 16) | (ib[(s1 >> 8) & 0xFF] << 8) | ib[s0 & 0xFF]) ^ k[o + 3],
        )
        return struct.pack(">4I", *out)


# --------------------------------------------------------------- GCM

_R = 0xE1 << 120


def _ghash_tables(h: int) -> List[List[int]]:
    """
    Per-key tables for GF(2^128) multiplication by H (SP 800-38D bit order).

    M[i][b] = (byte b placed at byte position i of X) · H, so that
    X · H = XOR over the 16 bytes of X of M[i][X_i]  (multiplication is linear).
    """
    # V_j = H · x^j in GCM's reflected representation (j = 0..127)
    v = []
    cur = h
    for _ in range(128):
        v.append(cur)
        cur = (cur >> 1) ^ _R if cur & 1 else cur >> 1
    tables = []
    for i in range(16):
        row = [0] * 256
        for b in range(256):
            acc = 0
            for bit in range(8):
                if b & (0x80 >> bit):
                    acc ^= v[8 * i + bit]
            row[b] = acc
        tables.append(row)
    return tables


def _ghash(tables: List[List[int]], data: bytes) -> int:
    y = 0
    for off in range(0, len(data), 16):
        y ^= int.from_bytes(data[off:off + 16], "big")
        x = y.to_bytes(16, "big")
        y = 0
        for i in range(16):
            y ^= tables[i][x[i]]
    return y


def _pad16(data: bytes) -> bytes:
    return data + b"\x00" * (-len(data) % 16)


class AESGCM:
    """
    AES-GCM authenticated encryption (NIST SP 800-38D), API-compatible with the
    `cryptography` package: ciphertext output is ``ct || tag`` (16-byte tag).

    Invariant I-C1 (Supreme Specification E25): with random 96-bit nonces a key
    may protect at most 2^32 messages. Each instance counts its encryptions and
    refuses to exceed the bound; callers must rotate the key.
    """

    MAX_INVOCATIONS = 2 ** 32
    TAG_SIZE = 16

    def __init__(self, key: bytes):
        if len(key) not in (16, 24, 32):
            raise ValueError("AESGCM key must be 128, 192 or 256 bits")
        self._aes = AES(key)
        h = int.from_bytes(self._aes.encrypt_block(b"\x00" * 16), "big")
        self._tables = _ghash_tables(h)
        self.invocations = 0

    @staticmethod
    def generate_key(bit_length: int = 256) -> bytes:
        if bit_length not in (128, 192, 256):
            raise ValueError("bit_length must be 128, 192 or 256")
        return secrets.token_bytes(bit_length // 8)

    def _j0(self, nonce: bytes) -> int:
        if len(nonce) == 12:
            return int.from_bytes(nonce + b"\x00\x00\x00\x01", "big")
        data = _pad16(nonce) + struct.pack(">QQ", 0, len(nonce) * 8)
        return _ghash(self._tables, data)

    def _gctr(self, counter: int, data: bytes) -> bytes:
        out = bytearray()
        enc = self._aes.encrypt_block
        prefix = counter & ~0xFFFFFFFF
        low = counter & 0xFFFFFFFF
        for off in range(0, len(data), 16):
            block = (prefix | low).to_bytes(16, "big")
            keystream = enc(block)
            chunk = data[off:off + 16]
            out += bytes(a ^ b for a, b in zip(chunk, keystream))
            low = (low + 1) & 0xFFFFFFFF  # inc32
        return bytes(out)

    def _tag(self, j0: int, aad: bytes, ciphertext: bytes) -> bytes:
        s = _ghash(self._tables, _pad16(aad) + _pad16(ciphertext)
                   + struct.pack(">QQ", len(aad) * 8, len(ciphertext) * 8))
        return self._gctr(j0, s.to_bytes(16, "big"))

    def encrypt(self, nonce: bytes, data: bytes, associated_data: Optional[bytes]) -> bytes:
        if not nonce:
            raise ValueError("Nonce must not be empty")
        if self.invocations >= self.MAX_INVOCATIONS:
            raise RuntimeError("AES-GCM key usage bound reached (2^32 messages): rotate the key")
        self.invocations += 1
        aad = associated_data or b""
        j0 = self._j0(nonce)
        ciphertext = self._gctr((j0 & ~0xFFFFFFFF) | ((j0 + 1) & 0xFFFFFFFF), data)
        return ciphertext + self._tag(j0, aad, ciphertext)

    def decrypt(self, nonce: bytes, data: bytes, associated_data: Optional[bytes]) -> bytes:
        if len(data) < self.TAG_SIZE:
            raise InvalidTag("Ciphertext shorter than the tag")
        if not nonce:
            raise ValueError("Nonce must not be empty")
        aad = associated_data or b""
        ciphertext, tag = data[:-self.TAG_SIZE], data[-self.TAG_SIZE:]
        j0 = self._j0(nonce)
        if not hmac.compare_digest(self._tag(j0, aad, ciphertext), tag):
            raise InvalidTag("Authentication tag mismatch")
        return self._gctr((j0 & ~0xFFFFFFFF) | ((j0 + 1) & 0xFFFFFFFF), ciphertext)


# --------------------------------------------------------------- HKDF

def hkdf_sha256(key_material: bytes, length: int, info: bytes = b"", salt: Optional[bytes] = None) -> bytes:
    """HKDF-SHA256 (RFC 5869): extract-then-expand."""
    if length > 255 * 32:
        raise ValueError("HKDF-SHA256 output length too large")
    prk = hmac.new(salt if salt else b"\x00" * 32, key_material, hashlib.sha256).digest()
    okm, block = b"", b""
    counter = 1
    while len(okm) < length:
        block = hmac.new(prk, block + info + bytes([counter]), hashlib.sha256).digest()
        okm += block
        counter += 1
    return okm[:length]


# --------------------------------------------------------------- Fernet (legacy)

class Fernet:
    """
    Fernet tokens: version 0x80 | timestamp | IV | AES-128-CBC(PKCS7) | HMAC-SHA256.

    Kept so that vault data written before the sovereignty migration remains
    readable (LAW-001); new vault data uses AES-256-GCM.
    """

    def __init__(self, key: bytes):
        raw = base64.urlsafe_b64decode(key)
        if len(raw) != 32:
            raise ValueError("Fernet key must be 32 url-safe base64-encoded bytes")
        self._signing_key, self._encryption_key = raw[:16], raw[16:]
        self._aes = AES(self._encryption_key)

    @staticmethod
    def generate_key() -> bytes:
        return base64.urlsafe_b64encode(os.urandom(32))

    def encrypt(self, data: bytes, current_time: Optional[int] = None, iv: Optional[bytes] = None) -> bytes:
        iv = iv or os.urandom(16)
        pad = 16 - len(data) % 16
        padded = data + bytes([pad]) * pad
        ciphertext, prev = bytearray(), iv
        for off in range(0, len(padded), 16):
            block = bytes(a ^ b for a, b in zip(padded[off:off + 16], prev))
            prev = self._aes.encrypt_block(block)
            ciphertext += prev
        timestamp = int(time.time()) if current_time is None else current_time
        body = b"\x80" + struct.pack(">Q", timestamp) + iv + bytes(ciphertext)
        mac = hmac.new(self._signing_key, body, hashlib.sha256).digest()
        return base64.urlsafe_b64encode(body + mac)

    def decrypt(self, token: bytes) -> bytes:
        try:
            data = base64.urlsafe_b64decode(token)
        except (ValueError, TypeError) as e:
            raise InvalidToken("Token is not valid base64") from e
        if len(data) < 1 + 8 + 16 + 16 + 32 or data[0] != 0x80 or (len(data) - 57) % 16:
            raise InvalidToken("Malformed token")
        body, mac = data[:-32], data[-32:]
        if not hmac.compare_digest(hmac.new(self._signing_key, body, hashlib.sha256).digest(), mac):
            raise InvalidToken("Signature mismatch")
        iv, ciphertext = body[9:25], body[25:]
        plain, prev = bytearray(), iv
        for off in range(0, len(ciphertext), 16):
            block = ciphertext[off:off + 16]
            plain += bytes(a ^ b for a, b in zip(self._aes.decrypt_block(block), prev))
            prev = block
        pad = plain[-1]
        if not 1 <= pad <= 16 or plain[-pad:] != bytes([pad]) * pad:
            raise InvalidToken("Bad padding")
        return bytes(plain[:-pad])
