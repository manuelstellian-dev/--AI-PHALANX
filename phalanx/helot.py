"""
Helot Module - Monitorizarea Resurselor Fizice
Responsabil cu monitorizarea CPU, RAM, GPU, NPU și calcularea probabilității de supraviețuire
"""

import psutil
import asyncio
from typing import Dict, Any
from loguru import logger


class HelotModule:
    """
    Modulul Helot - Monitorul de Resurse al Falangei.
    Monitorizează resursele hardware și calculează probabilitatea de supraviețuire a sistemului.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Inițializează modulul Helot.
        
        Args:
            config: Configurația modulului
        """
        self.config = config
        self.survival_probability = 1.0
        self.resource_thresholds = config.get('resource_thresholds', {
            'cpu_critical': 95.0,
            'memory_critical': 90.0,
            'disk_critical': 95.0
        })
        logger.info("🏺 Helot Module initialized - Resource monitoring active")

    async def monitor_resources(self) -> Dict[str, Any]:
        """
        Monitorizează toate resursele hardware disponibile.
        
        Returns:
            Dicționar cu statistici despre resurse
        """
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        
        resources = {
            'cpu_percent': cpu_percent,
            'cpu_count': cpu_count,
            'memory_percent': psutil.virtual_memory().percent,
            'memory_available_gb': psutil.virtual_memory().available / (1024**3),
            'disk_percent': psutil.disk_usage('/').percent,
            'disk_free_gb': psutil.disk_usage('/').free / (1024**3)
        }
        
        # Calculează factorul de paralelism (P)
        resources['parallelism_factor'] = self._calculate_parallelism_factor(resources)
        
        # Calculează probabilitatea de supraviețuire
        self.survival_probability = self._calculate_survival_probability(resources)
        
        return resources
    
    def _calculate_parallelism_factor(self, resources: Dict[str, Any]) -> float:
        """
        Calculează Factorul de Paralelism (P) conform formulei spartane.
        
        Formula: P = 1.0 + (CPU_Cores * (1 - CPU_Load/100)) + (GPU_Load * 5)
        
        Args:
            resources: Statistici despre resurse
            
        Returns:
            Factorul de paralelism (P)
        """
        cpu_cores = resources.get('cpu_count', 1)
        cpu_load = resources.get('cpu_percent', 0)
        
        # Simulare GPU load (în configurație reală, ar veni din GPUtil)
        gpu_load = self.config.get('simulated_gpu_load', 0.0)
        
        # Formula: P = 1.0 + (Numărul de Core-uri Logice * (1 - Încărcare CPU/100)) + (Încărcare GPU * 5)
        P = 1.0 + (cpu_cores * (1 - cpu_load / 100.0)) + (gpu_load * 5)
        
        # P trebuie să fie mai mare decât 1
        P = max(1.0, P)
        
        return P

    def _calculate_survival_probability(self, resources: Dict[str, Any]) -> float:
        """
        Calculează probabilitatea de supraviețuire pe baza resurselor disponibile.
        
        Args:
            resources: Statistici despre resurse
            
        Returns:
            Probabilitate între 0.0 și 1.0
        """
        probability = 1.0
        
        # Penalizare pentru CPU critic
        if resources['cpu_percent'] > self.resource_thresholds['cpu_critical']:
            probability -= 0.1
        
        # Penalizare pentru memorie critică
        if resources['memory_percent'] > self.resource_thresholds['memory_critical']:
            probability -= 0.15
        
        # Penalizare pentru disc critic
        if resources['disk_percent'] > self.resource_thresholds['disk_critical']:
            probability -= 0.1
        
        # Asigură că probabilitatea rămâne în intervalul [0, 1]
        probability = max(0.0, min(1.0, probability))
        
        return probability

    async def get_survival_probability(self) -> float:
        """
        Returnează probabilitatea curentă de supraviețuire.
        
        Returns:
            Probabilitatea de supraviețuire (0.0 - 1.0)
        """
        await self.monitor_resources()
        return self.survival_probability

    async def get_status(self) -> Dict[str, Any]:
        """
        Returnează starea curentă a modulului Helot.
        
        Returns:
            Dicționar cu starea modulului
        """
        resources = await self.monitor_resources()
        return {
            "module": "Helot",
            "status": "active",
            "survival_probability": self.survival_probability,
            "resources": resources
        }

    async def optimize_resources(self):
        """
        Încearcă să optimizeze utilizarea resurselor (placeholder pentru logică avansată).
        """
        logger.info("⚡ Helot: Attempting resource optimization...")
        # Aici ar putea fi implementate strategii de optimizare
        # De exemplu: eliberare cache, închidere procese neesențiale, etc.
        pass
