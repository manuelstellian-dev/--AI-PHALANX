"""
Command Processor - Λ-Möbius Engine
Interpretează intențiile Comandantului și rutează comenzile către modulul corect
"""

from typing import Dict, Any, Optional
from loguru import logger


class CommandProcessor:
    """
    Λ-Möbius Engine - Procesorul de Comenzi al Falangei.
    Responsabil cu:
    - Interpretarea intenției Comandantului
    - Rutarea comenzilor către modulele corecte
    - Aplicarea factorului de adaptare din Agoge
    """

    def __init__(self, modules: Dict[str, Any]):
        """
        Inițializează procesorul de comenzi.
        
        Args:
            modules: Referințe către modulele Phalanx și Hoplites
        """
        self.modules = modules
        self.adaptation_factor = 1.0
        self.active_tasks = 0
        self.data_vault_size_mb = 0.0
        logger.info("⚙️ Λ-Möbius Command Processor initialized")
    
    def calculate_universe_expansion_factor(self) -> float:
        """
        Calculează Factorul de Expansiune a Universului (U).
        Reflectă volumul de date și sarcinile active.
        
        Formula: U = (1 + Sarcini active + ln(max(1.0, Volum Vault MB))) * Factor Adaptare Agoge
        
        Returns:
            Factorul de expansiune (U)
        """
        import math
        
        # Formula: U = (1 + Sarcini active + ln(max(1.0, Volum Vault MB))) * Factor Adaptare Agoge
        base_expansion = 1 + self.active_tasks + math.log(max(1.0, self.data_vault_size_mb))
        U = base_expansion * self.adaptation_factor
        
        return U

    async def process_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesează o comandă tactică de la Comandant.
        
        Args:
            command: Dicționar cu detalii despre comandă
                {
                    "type": "analyze_risk" | "encrypt_data" | "status" | etc.,
                    "payload": {...},
                    "priority": "high" | "normal" | "low"
                }
        
        Returns:
            Rezultatul execuției comenzii
        """
        cmd_type = command.get("type")
        payload = command.get("payload", {})
        priority = command.get("priority", "normal")
        
        logger.info(f"📥 Processing command: {cmd_type} (priority: {priority})")
        
        try:
            # Rutare către modulul corespunzător
            if cmd_type == "status":
                return await self._handle_status_command()
            
            elif cmd_type == "analyze_risk":
                return await self._handle_risk_analysis(payload)
            
            elif cmd_type == "encrypt_data":
                return await self._handle_encryption(payload)
            
            elif cmd_type == "check_airgap":
                return await self._handle_airgap_check()
            
            elif cmd_type == "send_message":
                return await self._handle_message_send(payload)
            
            elif cmd_type == "train_agoge":
                return await self._handle_agoge_training(payload)
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown command type: {cmd_type}",
                    "suggestion": "Available commands: status, analyze_risk, encrypt_data, check_airgap, send_message, train_agoge"
                }
        
        except Exception as e:
            logger.error(f"❌ Error processing command {cmd_type}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _handle_status_command(self) -> Dict[str, Any]:
        """Obține starea sistemului."""
        status = {
            "success": True,
            "system": "ΛΕΩΝΙΔΑΣ-AI PHALANX",
            "motto": "ΜΟΛΩΝ ΛΑΒΕ",
            "modules": {}
        }
        
        # Colectează starea de la toate modulele
        if 'phalanx' in self.modules:
            phalanx = self.modules['phalanx']
            if 'helot' in phalanx:
                status['modules']['helot'] = await phalanx['helot'].get_status()
            if 'agoge' in phalanx:
                status['modules']['agoge'] = await phalanx['agoge'].get_status()
            if 'krypteia' in phalanx:
                status['modules']['krypteia'] = await phalanx['krypteia'].get_status()
        
        if 'hoplites' in self.modules:
            hoplites = self.modules['hoplites']
            if 'shield' in hoplites:
                status['modules']['shield'] = await hoplites['shield'].get_status()
        
        return status

    async def _handle_risk_analysis(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Trimite cerere de analiză de risc către Battle Oracle."""
        if 'hoplites' not in self.modules or 'oracle' not in self.modules['hoplites']:
            return {"success": False, "error": "Battle Oracle not available"}
        
        oracle = self.modules['hoplites']['oracle']
        result = await oracle.analyze_risk(payload)
        return {"success": True, "result": result}

    async def _handle_encryption(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Criptează date folosind Spartan Guard."""
        if 'hoplites' not in self.modules or 'guard' not in self.modules['hoplites']:
            return {"success": False, "error": "Spartan Guard not available"}
        
        guard = self.modules['hoplites']['guard']
        data = payload.get("data", "")
        encrypted = await guard.encrypt(data)
        return {"success": True, "encrypted_data": encrypted}

    async def _handle_airgap_check(self) -> Dict[str, Any]:
        """Verifică starea Air-Gap prin Shield Bearer."""
        if 'hoplites' not in self.modules or 'shield' not in self.modules['hoplites']:
            return {"success": False, "error": "Shield Bearer not available"}
        
        shield = self.modules['hoplites']['shield']
        is_secure = await shield.check_airgap()
        return {"success": True, "airgap_active": is_secure}

    async def _handle_message_send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Trimite mesaj securizat prin Messenger."""
        if 'hoplites' not in self.modules or 'messenger' not in self.modules['hoplites']:
            return {"success": False, "error": "Messenger not available"}
        
        messenger = self.modules['hoplites']['messenger']
        result = await messenger.send_secure_message(payload)
        return {"success": True, "result": result}

    async def _handle_agoge_training(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Inițiază micro-antrenament în Agoge."""
        if 'phalanx' not in self.modules or 'agoge' not in self.modules['phalanx']:
            return {"success": False, "error": "Agoge module not available"}
        
        agoge = self.modules['phalanx']['agoge']
        result = await agoge.run_training_cycle(payload)
        self.adaptation_factor = result.get('adaptation_factor', 1.0)
        return {"success": True, "result": result}

    def set_adaptation_factor(self, factor: float):
        """
        Setează factorul de adaptare din Agoge.
        
        Args:
            factor: Noul factor de adaptare
        """
        self.adaptation_factor = factor
        logger.info(f"📊 Adaptation factor updated: {factor:.3f}")

    def get_adaptation_factor(self) -> float:
        """
        Returnează factorul curent de adaptare.
        
        Returns:
            Factorul de adaptare
        """
        return self.adaptation_factor
