"""
ΛΕΩΝΙΔΑΣ Brain - Nucleul Decizional Principal (Λ-Core)
Orchestrează toate modulele și menține homeostazia sistemului (dS/dt=0)
"""

import asyncio
import time
from typing import Dict, Any
from loguru import logger


class LeondasBrain:
    """
    Nucleul Central al Falangei Digitale.
    Responsabil cu:
    - Inițializarea tuturor modulelor (Phalanx și Hoplites)
    - Rularea buclei de homeostazie
    - Calcularea Timpului Autonom Spartan (Λ-TAS)
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Inițializează Λ-Core cu configurația spartană.
        
        Args:
            config: Configurația principală a sistemului
        """
        self.config = config
        self.lambda_tas = 1.0  # Timpul Autonom Spartan (factor de ritm)
        self.is_running = False
        self.modules = {}
        
        logger.info("🛡️ ΛΕΩΝΙΔΑΣ Brain initialized")
        logger.info(f"🏛️ Motto: ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)")

    def calculate_lambda_tas(self, parallelism: int, workload: float) -> float:
        """
        Calculează Timpul Autonom Spartan (Λ-TAS).
        Reglează ritmul de lucru pe baza paralelismului hardware (P) și volumului de date (U).
        
        Formula: Λ-TAS = P / (1 + U)
        
        Args:
            parallelism: Numărul de nucleuri disponibile
            workload: Volumul de sarcini (0.0 - 1.0)
            
        Returns:
            Factorul Λ-TAS
        """
        if workload < 0:
            workload = 0
        lambda_tas = parallelism / (1 + workload)
        return lambda_tas

    async def initialize_phalanx(self, phalanx_modules: Dict[str, Any]):
        """
        Inițializează modulele Phalanx (Helot, Agoge, Krypteia, Thermopylae).
        
        Args:
            phalanx_modules: Dicționar cu instanțe ale modulelor Phalanx
        """
        self.modules['phalanx'] = phalanx_modules
        logger.info("⚔️ Phalanx modules initialized")

    async def initialize_hoplites(self, hoplite_modules: Dict[str, Any]):
        """
        Inițializează modulele Hoplites (Guard, Shield, Oracle, Weapon, Messenger).
        
        Args:
            hoplite_modules: Dicționar cu instanțe ale modulelor Hoplites
        """
        self.modules['hoplites'] = hoplite_modules
        logger.info("🗡️ Hoplites arsenal initialized")

    async def homeostasis_loop(self):
        """
        Bucla principală de homeostazie.
        Menține echilibrul sistemului (dS/dt=0) și monitorizează starea continuă.
        """
        logger.info("🔄 Starting homeostasis loop...")
        self.is_running = True
        
        while self.is_running:
            try:
                # Verifică starea modulelor
                if 'phalanx' in self.modules and 'helot' in self.modules['phalanx']:
                    survival_prob = await self.modules['phalanx']['helot'].get_survival_probability()
                    
                    # Verifică protocolul Thermopylae
                    if survival_prob < 0.95:
                        logger.warning(f"⚠️ Survival probability critical: {survival_prob:.2f}")
                        if 'thermopylae' in self.modules['phalanx']:
                            await self.modules['phalanx']['thermopylae'].check_emergency_protocol(survival_prob)
                
                # Actualizează Λ-TAS
                self.lambda_tas = self.calculate_lambda_tas(
                    parallelism=self.config.get('hardware', {}).get('cpu_cores', 4),
                    workload=self.config.get('current_workload', 0.5)
                )
                
                # Pauză între iterații (ajustată de Λ-TAS)
                await asyncio.sleep(1.0 / self.lambda_tas)
                
            except Exception as e:
                logger.error(f"❌ Error in homeostasis loop: {e}")
                await asyncio.sleep(1)

    async def shutdown(self):
        """
        Oprire controlată a nucleului Λ-Core.
        """
        logger.info("🛑 Shutting down ΛΕΩΝΙΔΑΣ Brain...")
        self.is_running = False
        
        # Închide modulele în ordine inversă
        if 'hoplites' in self.modules:
            logger.info("Shutting down Hoplites...")
        if 'phalanx' in self.modules:
            logger.info("Shutting down Phalanx...")
        
        logger.info("✅ ΛΕΩΝΙΔΑΣ Brain shutdown complete")

    def get_status(self) -> Dict[str, Any]:
        """
        Returnează starea curentă a nucleului.
        
        Returns:
            Dicționar cu informații despre stare
        """
        return {
            "is_running": self.is_running,
            "lambda_tas": self.lambda_tas,
            "modules_loaded": list(self.modules.keys()),
            "motto": "ΜΟΛΩΝ ΛΑΒΕ"
        }
