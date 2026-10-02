"""
ΛΕΩΝΙΔΑΣ Brain - Nucleul Decizional Principal (Λ-Core)
Orchestrează toate modulele și menține homeostazia sistemului (dS/dt=0)
"""

import asyncio
from typing import Dict, Any
from polis.log import logger
from control.fractal_pipeline import FractalFluxPipeline


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
        # Setat de api.server.initialize_system - sursa factorului U (Λ-Möbius)
        self.command_processor = None
        
        # Initialize FFP Pipeline
        self.ffp = FractalFluxPipeline(self)
        logger.info("🔄 FFP Pipeline initialized in LeondasBrain")
        
        logger.info("🛡️ ΛΕΩΝΙΔΑΣ Brain initialized")
        logger.info("🏛️ Motto: ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)")

    def calculate_lambda_tas(self, parallelism: float, workload: float) -> float:
        """
        Calculează Timpul Autonom Spartan (Λ-TAS).
        Reglează ritmul de lucru pe baza paralelismului hardware (P) și volumului de date (U).
        
        Formula avansată (pentru k·P > 1):
        T_new = (T_1 * ln(U + 1)) / (1 - 1 / (k * P))
        
        Unde:
        - T_1 = 1.0 secunde (valoare de bază)
        - k = 100 (constantă)
        - P = Factorul de Paralelism (calculat de Helot)
        - U = Mărimea Universului / Factor de Expansiune (calculat de CommandProcessor)
        
        Args:
            parallelism: Factorul de paralelism (P) - capacitatea de procesare paralelă
            workload: Factorul de expansiune (U) - volumul de sarcini și date
            
        Returns:
            Factorul Λ-TAS în secunde
        """
        import math
        
        if workload < 0:
            workload = 0
        if parallelism <= 0:
            parallelism = 1.0
        
        # Constante
        T_1 = 1.0  # Valoare de bază (secunde)
        k = 100    # Constantă de scalare
        
        # Formula avansată Λ-TAS
        # T_new = (T_1 * ln(U + 1)) / (1 - 1 / (k * P))
        k_times_P = k * parallelism
        
        if k_times_P <= 1:
            # Fallback la formula simplă dacă k·P ≤ 1
            lambda_tas = parallelism / (1 + workload)
        else:
            numerator = T_1 * math.log(workload + 1)
            denominator = 1 - (1 / k_times_P)
            lambda_tas = numerator / denominator if denominator > 0 else 1.0
            
            # Limitează valoarea pentru a evita extreme
            lambda_tas = max(0.1, min(10.0, lambda_tas))
        
        return lambda_tas

    def _current_parallelism(self) -> float:
        """
        Factorul de Paralelism (P) curent: măsurat de Helot dacă există o citire,
        altfel numărul de core-uri din configurație.
        """
        helot = self.modules.get('phalanx', {}).get('helot')
        last_resources = getattr(helot, 'last_resources', None)
        if isinstance(last_resources, dict) and 'parallelism_factor' in last_resources:
            return float(last_resources['parallelism_factor'])
        return self.config.get('hardware', {}).get('cpu_cores', 4)

    def _current_workload(self) -> float:
        """
        Factorul de Expansiune (U) curent: calculat de CommandProcessor dacă este
        conectat, altfel valoarea 'current_workload' din configurație.
        """
        processor = self.command_processor
        if processor is not None and hasattr(processor, 'calculate_universe_expansion_factor'):
            return processor.calculate_universe_expansion_factor()
        return self.config.get('current_workload', 0.5)

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
                    
                    # Thermopylae primește FIECARE eșantion (și recuperările): contorul de
                    # încălcări consecutive este corect doar dacă o singură buclă periodică
                    # îl alimentează cu toate observațiile (.memory DEC-019)
                    thermopylae = self.modules['phalanx'].get('thermopylae')
                    threshold = getattr(thermopylae, 'critical_threshold', 0.95)
                    if survival_prob < threshold:
                        logger.warning(f"⚠️ Survival probability critical: {survival_prob:.2f}")
                    if thermopylae is not None:
                        await thermopylae.check_emergency_protocol(survival_prob)
                
                # Actualizează Λ-TAS cu P (Helot) și U (CommandProcessor)
                self.lambda_tas = self.calculate_lambda_tas(
                    parallelism=self._current_parallelism(),
                    workload=self._current_workload()
                )
                
                # Pauză între iterații: Λ-TAS este perioada în secunde (T_new)
                await asyncio.sleep(self.lambda_tas)
                
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

    async def start_ffp(self):
        """
        Start Fractal Flux Pipeline.
        
        The FFP runs continuously in the background, executing the
        6-phase autoreparatory cycle: Scan → Detect → Quarantine → Heal → Improve → Reinvest
        """
        logger.info("🚀 Starting FFP Pipeline...")
        await self.ffp.run_forever()

    def get_ffp_status(self) -> dict:
        """
        Get current FFP Pipeline status.
        
        Returns:
            Dictionary with FFP status information
        """
        if hasattr(self, 'ffp'):
            return self.ffp.get_status()
        else:
            return {'error': 'FFP not initialized'}

    def stop_ffp(self):
        """Stop FFP Pipeline."""
        if hasattr(self, 'ffp'):
            logger.info("🛑 Stopping FFP Pipeline...")
            self.ffp.stop()
        else:
            logger.warning("⚠️ FFP not initialized, cannot stop")
