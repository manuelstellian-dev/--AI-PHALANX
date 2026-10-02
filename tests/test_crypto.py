"""
Tests for polis.crypto — ΛΕΩΝΙΔΑΣ's own cryptography (DEC-022).

Pinned by official vectors:
- FIPS-197 Appendix C (AES-128/192/256 block cipher)
- GCM specification test cases 13-16 (AES-256-GCM; McGrew & Viega, used by NIST SP 800-38D)
- RFC 5869 test case 1 (HKDF-SHA256)
- a legacy Fernet token verified against the reference implementation at migration time
"""

import base64
import os

import pytest

from polis.crypto import AES, AESGCM, INV_SBOX, SBOX, Fernet, InvalidTag, InvalidToken, hkdf_sha256

PT = bytes.fromhex("00112233445566778899aabbccddeeff")
K15 = "feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308"
P15 = ("d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72"
       "1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b391aafd255")
C15 = ("522dc1f099567d07f47f37a32a84427d643a8cdcbfe5c0c97598a2bd2555d1aa"
       "8cb08e48590dbb3da7b08b1056828838c5f61e6393ba7a0abcc9f662898015ad")


class TestAESBlockCipher:

    def test_derived_sbox_matches_fips197(self):
        assert (SBOX[0x00], SBOX[0x53], SBOX[0xFF]) == (0x63, 0xED, 0x16)
        assert sorted(SBOX) == list(range(256))  # a permutation
        assert all(INV_SBOX[SBOX[x]] == x for x in range(256))

    @pytest.mark.parametrize("key,ciphertext", [
        ("000102030405060708090a0b0c0d0e0f", "69c4e0d86a7b0430d8cdb78070b4c55a"),
        ("000102030405060708090a0b0c0d0e0f1011121314151617", "dda97ca4864cdfe06eaf70a0ec0d7191"),
        ("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f", "8ea2b7ca516745bfeafc49904b496089"),
    ])
    def test_fips197_appendix_c(self, key, ciphertext):
        aes = AES(bytes.fromhex(key))
        assert aes.encrypt_block(PT).hex() == ciphertext
        assert aes.decrypt_block(bytes.fromhex(ciphertext)) == PT
        assert aes.rounds == {16: 10, 24: 12, 32: 14}[len(bytes.fromhex(key))]

    def test_rejects_bad_key_length(self):
        with pytest.raises(ValueError):
            AES(b"short")


class TestAESGCM:

    @pytest.mark.parametrize("key,iv,plaintext,aad,ciphertext,tag", [
        ("00" * 32, "00" * 12, "", "", "", "530f8afbc74536b9a963b4f1c4cb738b"),
        ("00" * 32, "00" * 12, "00" * 16, "", "cea7403d4d606b6e074ec5d3baf39d18", "d0d1c8a799996bf0265b98b5d48ab919"),
        (K15, "cafebabefacedbaddecaf888", P15, "", C15, "b094dac5d93471bdec1a502270e3cc6c"),
        (K15, "cafebabefacedbaddecaf888", P15[:120], "feedfacedeadbeeffeedfacedeadbeefabaddad2",
         C15[:120], "76fc6ece0f4e1768cddf8853bb2d551b"),
    ], ids=["tc13", "tc14", "tc15", "tc16"])
    def test_gcm_specification_vectors(self, key, iv, plaintext, aad, ciphertext, tag):
        gcm = AESGCM(bytes.fromhex(key))
        k, n, p, a = bytes.fromhex(key), bytes.fromhex(iv), bytes.fromhex(plaintext), bytes.fromhex(aad)
        sealed = gcm.encrypt(n, p, a or None)
        assert sealed.hex() == ciphertext + tag
        assert AESGCM(k).decrypt(n, sealed, a or None) == p

    def test_round_trip_all_sizes_and_nonces(self):
        for key_bits in (128, 192, 256):
            gcm = AESGCM(AESGCM.generate_key(key_bits))
            for nonce_len in (8, 12, 16, 60):
                for size in (0, 1, 15, 16, 17, 100, 1000):
                    nonce, data, aad = os.urandom(nonce_len), os.urandom(size), os.urandom(size % 37)
                    assert gcm.decrypt(nonce, gcm.encrypt(nonce, data, aad), aad) == data

    def test_tampering_and_wrong_context_are_detected(self):
        gcm = AESGCM(AESGCM.generate_key())
        nonce = os.urandom(12)
        sealed = gcm.encrypt(nonce, b"secret orders", b"context")
        for corrupt in (bytes([sealed[0] ^ 1]) + sealed[1:], sealed[:-1] + bytes([sealed[-1] ^ 1]), sealed[:10]):
            with pytest.raises(InvalidTag):
                gcm.decrypt(nonce, corrupt, b"context")
        with pytest.raises(InvalidTag):
            gcm.decrypt(nonce, sealed, b"other context")
        with pytest.raises(InvalidTag):
            AESGCM(AESGCM.generate_key()).decrypt(nonce, sealed, b"context")

    def test_parameter_validation_and_usage_bound(self):
        with pytest.raises(ValueError):
            AESGCM(b"x" * 10)
        with pytest.raises(ValueError):
            AESGCM.generate_key(100)
        gcm = AESGCM(AESGCM.generate_key())
        with pytest.raises(ValueError):
            gcm.encrypt(b"", b"data", None)
        gcm.invocations = AESGCM.MAX_INVOCATIONS  # invariant I-C1: rotate before 2^32 messages
        with pytest.raises(RuntimeError, match="rotate"):
            gcm.encrypt(os.urandom(12), b"data", None)


class TestHKDF:

    def test_rfc5869_case_1(self):
        okm = hkdf_sha256(bytes.fromhex("0b" * 22), 42, info=bytes.fromhex("f0f1f2f3f4f5f6f7f8f9"),
                          salt=bytes.fromhex("000102030405060708090a0b0c"))
        assert okm.hex() == ("3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf"
                             "34007208d5b887185865")

    def test_length_bound(self):
        assert len(hkdf_sha256(b"k", 100)) == 100
        with pytest.raises(ValueError):
            hkdf_sha256(b"k", 255 * 32 + 1)


class TestFernetLegacy:
    # Produced with fixed time and IV and verified against the reference implementation at migration
    KEY = b"vS9H1F4kC0lQf4Hq5W1Yd3Zr7Tq2Lx8Pm6Nb4Vc2Xa0="
    TOKEN = (b"gAAAAABnHbSAAAECAwQFBgcICQoLDA0OD9rSKElmxAKNap_dIppqqj_cRVR0Br3n6KwG5KtotjAjznfoVw8s"
             b"F519kicOBAQsTn3S8aPjwt3t-OXaEYWsD5c=")

    def test_legacy_vector(self):
        assert Fernet(self.KEY).decrypt(self.TOKEN) == b"legacy vault secret"
        assert Fernet(self.KEY).encrypt(b"legacy vault secret", current_time=1730000000,
                                        iv=bytes(range(16))) == self.TOKEN

    def test_round_trip_and_rejections(self):
        key = Fernet.generate_key()
        f = Fernet(key)
        assert f.decrypt(f.encrypt(b"x" * 33)) == b"x" * 33
        token = bytearray(base64.urlsafe_b64decode(f.encrypt(b"data")))
        token[-1] ^= 1
        for bad in (base64.urlsafe_b64encode(bytes(token)), b"!!not base64!!", base64.urlsafe_b64encode(b"\x80short")):
            with pytest.raises(InvalidToken):
                f.decrypt(bad)
        with pytest.raises(ValueError):
            Fernet(base64.urlsafe_b64encode(b"too short"))


class TestVaultCipher:

    def test_new_records_use_gcm_and_bind_the_entry_id(self, tmp_path):
        from vault.spartan_vault import SpartanVault, VAULT_TOKEN_PREFIX
        vault = SpartanVault(storage_path=str(tmp_path))
        vault.store("alpha", "orders for alpha")
        token = vault.encrypted_storage["alpha"]
        assert token.startswith(VAULT_TOKEN_PREFIX)
        assert vault.retrieve("alpha") == "orders for alpha"
        # Moving a ciphertext to another id is detected (id is associated data)
        vault.encrypted_storage["beta"] = token
        assert vault.retrieve("beta") is None

    def test_legacy_fernet_records_remain_readable(self, tmp_path):
        from vault.spartan_vault import SpartanVault
        vault = SpartanVault(encryption_key=TestFernetLegacy.KEY, storage_path=str(tmp_path))
        vault.encrypted_storage["old"] = TestFernetLegacy.TOKEN
        assert vault.retrieve("old") == "legacy vault secret"

    @pytest.mark.asyncio
    async def test_spartan_guard_round_trip(self):
        from hoplites.spartanguard import SpartanGuard
        guard = SpartanGuard({'master_key_hex': '11' * 32})
        sealed = await guard.encrypt("classified", associated_data="ctx")
        assert await guard.decrypt(sealed, associated_data="ctx") == "classified"
