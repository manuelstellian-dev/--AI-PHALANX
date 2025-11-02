"""
Spartan Guard - Modulul de Criptografie
Asigură integritatea și confidențialitatea datelor prin AES-256-GCM
"""

import os
import base64
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from loguru import logger


class SpartanGuard:
    """
    Modulul Spartan Guard - Criptografia Falangei.
    Utilizează AES-256-GCM pentru criptare și decriptare securizată.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Inițializează Spartan Guard.
        
        Args:
            config: Configurația cu cheile criptografice
        """
        self.config = config
        self.master_key = self._load_master_key()
        self.aesgcm = AESGCM(self.master_key) if self.master_key else None
        
        if self.aesgcm:
            logger.info("🛡️ Spartan Guard initialized - AES-256-GCM encryption ready")
        else:
            logger.warning("⚠️ Spartan Guard: Master key not loaded - encryption unavailable")

    def _load_master_key(self) -> Optional[bytes]:
        """
        Încarcă cheia master de criptare.
        
        Returns:
            Cheia master sau None dacă nu este disponibilă
        """
        # Încearcă să încarce din configurație
        master_key_hex = self.config.get('master_key_hex')
        
        if master_key_hex:
            try:
                return bytes.fromhex(master_key_hex)
            except Exception as e:
                logger.error(f"❌ Error loading master key from config: {e}")
        
        # Încearcă să încerce din environment
        master_key_env = os.getenv('SPARTA_MASTER_KEY')
        if master_key_env:
            try:
                return bytes.fromhex(master_key_env)
            except Exception as e:
                logger.error(f"❌ Error loading master key from environment: {e}")
        
        logger.warning("⚠️ No master key available - using temporary key for development")
        # Generează o cheie temporară pentru dezvoltare
        return AESGCM.generate_key(bit_length=256)

    async def encrypt(self, plaintext: str, associated_data: Optional[str] = None) -> str:
        """
        Criptează un text folosind AES-256-GCM.
        
        Args:
            plaintext: Textul de criptat
            associated_data: Date asociate opționale (pentru GCM)
            
        Returns:
            Text criptat (base64)
        """
        if not self.aesgcm:
            raise RuntimeError("Spartan Guard not properly initialized")
        
        try:
            # Generează un nonce unic
            nonce = os.urandom(12)  # 96 bits pentru GCM
            
            # Convertește plaintext la bytes
            plaintext_bytes = plaintext.encode('utf-8')
            
            # Criptează
            aad = associated_data.encode('utf-8') if associated_data else None
            ciphertext = self.aesgcm.encrypt(nonce, plaintext_bytes, aad)
            
            # Combină nonce + ciphertext pentru transport
            encrypted_data = nonce + ciphertext
            
            # Codifică în base64 pentru transport
            encrypted_b64 = base64.b64encode(encrypted_data).decode('utf-8')
            
            logger.debug(f"🔒 Data encrypted successfully ({len(plaintext)} bytes)")
            return encrypted_b64
            
        except Exception as e:
            logger.error(f"❌ Encryption error: {e}")
            raise

    async def decrypt(self, encrypted_b64: str, associated_data: Optional[str] = None) -> str:
        """
        Decriptează un text criptat cu AES-256-GCM.
        
        Args:
            encrypted_b64: Text criptat (base64)
            associated_data: Date asociate opționale (trebuie să corespundă cu cele de la criptare)
            
        Returns:
            Text decriptat
        """
        if not self.aesgcm:
            raise RuntimeError("Spartan Guard not properly initialized")
        
        try:
            # Decodifică din base64
            encrypted_data = base64.b64decode(encrypted_b64)
            
            # Extrage nonce și ciphertext
            nonce = encrypted_data[:12]
            ciphertext = encrypted_data[12:]
            
            # Decriptează
            aad = associated_data.encode('utf-8') if associated_data else None
            plaintext_bytes = self.aesgcm.decrypt(nonce, ciphertext, aad)
            
            # Convertește înapoi la string
            plaintext = plaintext_bytes.decode('utf-8')
            
            logger.debug(f"🔓 Data decrypted successfully ({len(plaintext)} bytes)")
            return plaintext
            
        except Exception as e:
            logger.error(f"❌ Decryption error: {e}")
            raise

    async def hash_data(self, data: str) -> str:
        """
        Calculează hash-ul SHA-256 al datelor.
        
        Args:
            data: Datele de hash-uit
            
        Returns:
            Hash-ul (hex)
        """
        import hashlib
        hash_obj = hashlib.sha256(data.encode('utf-8'))
        return hash_obj.hexdigest()

    async def verify_integrity(self, data: str, expected_hash: str) -> bool:
        """
        Verifică integritatea datelor comparând hash-ul.
        
        Args:
            data: Datele de verificat
            expected_hash: Hash-ul așteptat
            
        Returns:
            True dacă hash-ul corespunde
        """
        actual_hash = await self.hash_data(data)
        return actual_hash == expected_hash

    async def get_status(self) -> Dict[str, Any]:
        """
        Returnează starea curentă a Spartan Guard.
        
        Returns:
            Dicționar cu starea modulului
        """
        return {
            "module": "SpartanGuard",
            "status": "active" if self.aesgcm else "inactive",
            "encryption": "AES-256-GCM",
            "key_loaded": self.master_key is not None
        }
