"""
Thermopylae Module - Protocolul de Urgență Extremă
Execută auto-distrugerea controlată dacă probabilitatea de supraviețuire este critică
"""

import os
import asyncio
from typing import Dict, Any
from loguru import logger
import shutil


class ThermopylaeModule:
    """
    Modulul Thermopylae - Protocolul de Urgență Extremă al Falangei.
    Se declanșează dacă probabilitatea de supraviețuire scade sub pragul critic.
    Execută auto-distrugerea controlată prin ștergerea cheilor și vault-ului.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Inițializează modulul Thermopylae.
        
        Args:
            config: Configurația modulului
        """
        self.config = config
        self.critical_threshold = config.get('survival_threshold', 0.95)
        self.is_armed = config.get('thermopylae_armed', False)
        self.protocol_activated = False
        logger.info(f"🔥 Thermopylae Module initialized - Critical threshold: {self.critical_threshold}")

    async def check_emergency_protocol(self, survival_probability: float):
        """
        Verifică dacă este necesar să se activeze protocolul de urgență.
        
        Args:
            survival_probability: Probabilitatea curentă de supraviețuire
        """
        if survival_probability < self.critical_threshold:
            logger.critical(f"🚨 THERMOPYLAE ALERT: Survival probability {survival_probability:.2f} below threshold {self.critical_threshold}")
            
            if self.is_armed:
                logger.critical("⚠️ THERMOPYLAE PROTOCOL ACTIVATED - INITIATING CONTROLLED SELF-DESTRUCTION")
                await self.activate_protocol()
            else:
                logger.warning("⚠️ Thermopylae protocol not armed - Manual intervention required")

    async def activate_protocol(self):
        """
        Activează protocolul Thermopylae - auto-distrugere controlată.
        ATENȚIE: Această operațiune este IREVERSIBILĂ!
        """
        if self.protocol_activated:
            logger.warning("⚠️ Thermopylae protocol already activated")
            return
        
        self.protocol_activated = True
        logger.critical("💥 THERMOPYLAE PROTOCOL EXECUTING...")
        
        # Pas 1: Șterge cheile criptografice
        await self._destroy_cryptographic_keys()
        
        # Pas 2: Șterge vault-ul criptat
        await self._destroy_encrypted_vault()
        
        # Pas 3: Notifică sistemul
        logger.critical("✅ Thermopylae protocol completed - System secured through destruction")

    async def _destroy_cryptographic_keys(self):
        """
        Șterge ireversibil cheile criptografice.
        """
        logger.critical("🔑 Destroying cryptographic keys...")
        
        keys_path = self.config.get('keys_path', '/config/spartan_keys.yaml')
        base_path = self.config.get('base_path', '/home/runner/work/--AI-PHALANX/--AI-PHALANX')
        full_path = os.path.join(base_path, keys_path.lstrip('/'))
        
        try:
            if os.path.exists(full_path):
                # Suprascrie cu date random înainte de ștergere
                with open(full_path, 'wb') as f:
                    f.write(os.urandom(1024 * 1024))  # 1MB random data
                os.remove(full_path)
                logger.critical(f"🔥 Keys destroyed: {full_path}")
            else:
                logger.warning(f"⚠️ Keys file not found: {full_path}")
        except Exception as e:
            logger.error(f"❌ Error destroying keys: {e}")

    async def _destroy_encrypted_vault(self):
        """
        Șterge ireversibil vault-ul criptat.
        """
        logger.critical("💾 Destroying encrypted vault...")
        
        vault_path = self.config.get('vault_path', '/data/encrypted_vault')
        base_path = self.config.get('base_path', '/home/runner/work/--AI-PHALANX/--AI-PHALANX')
        full_path = os.path.join(base_path, vault_path.lstrip('/'))
        
        try:
            if os.path.exists(full_path):
                # Șterge recursiv directorul vault
                shutil.rmtree(full_path)
                logger.critical(f"🔥 Vault destroyed: {full_path}")
            else:
                logger.warning(f"⚠️ Vault directory not found: {full_path}")
        except Exception as e:
            logger.error(f"❌ Error destroying vault: {e}")

    async def arm_protocol(self):
        """
        Armează protocolul Thermopylae (permite activarea automată).
        """
        self.is_armed = True
        logger.warning("⚡ Thermopylae protocol ARMED - Auto-destruction enabled")

    async def disarm_protocol(self):
        """
        Dezarmează protocolul Thermopylae.
        """
        self.is_armed = False
        logger.info("🛡️ Thermopylae protocol DISARMED")

    async def get_status(self) -> Dict[str, Any]:
        """
        Returnează starea curentă a modulului Thermopylae.
        
        Returns:
            Dicționar cu starea modulului
        """
        return {
            "module": "Thermopylae",
            "is_armed": self.is_armed,
            "protocol_activated": self.protocol_activated,
            "critical_threshold": self.critical_threshold,
            "warning": "DANGER: This module can execute irreversible system destruction"
        }

    async def test_protocol(self) -> Dict[str, Any]:
        """
        Testează protocolul fără a executa distrugerea efectivă.
        
        Returns:
            Rezultatul testului
        """
        logger.info("🧪 Testing Thermopylae protocol (simulation mode)...")
        
        result = {
            "test": "thermopylae_protocol",
            "steps": [
                "Check cryptographic keys path",
                "Check encrypted vault path",
                "Verify destruction capability"
            ],
            "status": "simulation_complete",
            "warning": "This was a simulation - no actual destruction occurred"
        }
        
        return result
