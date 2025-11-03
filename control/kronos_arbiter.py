"""
KRONOS-ARBITER - Arbiter Temporal pentru Execuție Paralelă
Implementează formula: T_parallel = T_sequential / (N × Θ × Λ × η)

Θ (Theta) - Efficiency Factor: Cât de eficient este paralelizat codul
Λ (Lambda) - Load Balance: Cât de bine sunt distribuite sarcinile
η (Eta) - Overhead Factor: Penalizare pentru overhead-ul de sincronizare
N - Number of cores/workers

Acest modul calculează metrici de performanță pentru execuția paralelă,
bazate pe legea lui Amdahl și factori Spartan specifici.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Literal
from enum import Enum
import math
import time
from loguru import logger
from control.lambda_mobius import LambdaMobiusEngine, LambdaState, LambdaMetrics


class ThetaMode(str, Enum):
    """Moduri de calculare a factorului Theta (Efficiency)."""
    ADAPTIVE = "adaptive"      # Adaptiv bazat pe istoric
    FIXED = "fixed"           # Fix, definit de utilizator
    EXPONENTIAL = "exponential"  # Creștere exponențială cu workload


@dataclass
class MetrikosTachys:
    """
    Metrici de viteză pentru execuție paralelă.
    
    Attributes:
        t_sequential: Timpul de execuție secvențial (secunde)
        t_parallel: Timpul de execuție paralel calculat (secunde)
        speedup: Factorul de accelerare (T_sequential / T_parallel)
        efficiency: Eficiența paralelizării (Speedup / N_cores)
        theta: Factorul de eficiență (Θ)
        lambda_balance: Factorul de load balancing (Λ)
        eta_overhead: Factorul de overhead (η)
        n_cores: Numărul de core-uri utilizate
        amdahl_fraction: Fracțiunea paralelizabilă (pentru legea lui Amdahl)
    """
    t_sequential: float
    t_parallel: float
    speedup: float
    efficiency: float
    theta: float
    lambda_balance: float
    eta_overhead: float
    n_cores: int
    amdahl_fraction: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertește metricile în dicționar."""
        return {
            't_sequential': self.t_sequential,
            't_parallel': self.t_parallel,
            'speedup': self.speedup,
            'efficiency': self.efficiency,
            'theta': self.theta,
            'lambda_balance': self.lambda_balance,
            'eta_overhead': self.eta_overhead,
            'n_cores': self.n_cores,
            'amdahl_fraction': self.amdahl_fraction
        }


class KronosArbiter:
    """
    Kronos-Arbiter: Arbitru temporal pentru execuție paralelă.
    
    Calculează metrici de performanță folosind formula Kronos:
    T_parallel = T_sequential / (N × Θ × Λ × η)
    
    Unde:
    - N = număr de core-uri/workers
    - Θ = efficiency factor (cât de bine se paralelizează codul)
    - Λ = load balance factor (cât de uniform sunt distribuite sarcinile)
    - η = overhead factor (penalizare pentru sincronizare)
    """
    
    def __init__(
        self,
        n_cores: int = 4,
        theta_mode: ThetaMode = ThetaMode.ADAPTIVE,
        default_theta: float = 0.85,
        default_lambda: float = 0.95,
        default_eta: float = 0.90
    ):
        """
        Inițializează Kronos-Arbiter.
        
        Args:
            n_cores: Numărul de core-uri disponibile
            theta_mode: Modul de calculare a factorului Theta
            default_theta: Valoarea default pentru Theta (0.0-1.0)
            default_lambda: Valoarea default pentru Lambda (0.0-1.0)
            default_eta: Valoarea default pentru Eta (0.0-1.0)
        """
        self.n_cores = n_cores
        self.theta_mode = theta_mode
        self.default_theta = self._validate_factor(default_theta, "theta")
        self.default_lambda = self._validate_factor(default_lambda, "lambda")
        self.default_eta = self._validate_factor(default_eta, "eta")
        
        # Istoric de execuții pentru mod adaptiv
        self.execution_history: List[Dict[str, float]] = []
        
        # Mapare Theta -> Dynamis (putere efectivă)
        self.theta_to_dynamis_map: Dict[float, float] = {}
        
        # Initialize Λ-MÖBIUS Engine
        self.lambda_mobius = LambdaMobiusEngine(T1=1.0)
        
        logger.info(f"🕐 Kronos-Arbiter initialized with {n_cores} cores")
        logger.info(f"⚙️ Theta mode: {theta_mode}, defaults: Θ={default_theta}, Λ={default_lambda}, η={default_eta}")
    
    @staticmethod
    def _validate_factor(value: float, name: str) -> float:
        """
        Validează că un factor este între 0.0 și 1.0.
        
        Args:
            value: Valoarea de validat
            name: Numele factorului (pentru mesaje de eroare)
            
        Returns:
            Valoarea validată
            
        Raises:
            ValueError: Dacă valoarea nu este în range-ul valid
        """
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be between 0.0 and 1.0, got {value}")
        return value
    
    def calculate_theta(
        self,
        workload_complexity: float = 0.5,
        parallelizable_fraction: float = 1.0
    ) -> float:
        """
        Calculează factorul Theta (efficiency) bazat pe modul selectat.
        
        Args:
            workload_complexity: Complexitatea workload-ului (0.0-1.0)
            parallelizable_fraction: Fracțiunea paralelizabilă (0.0-1.0)
            
        Returns:
            Valoarea calculată pentru Theta
        """
        if self.theta_mode == ThetaMode.FIXED:
            return self.default_theta
        
        elif self.theta_mode == ThetaMode.ADAPTIVE:
            # Adaptiv: învață din istoric
            if len(self.execution_history) < 3:
                # Prea puține date, folosește valoarea default
                return self.default_theta
            
            # Calculează media Theta din ultimele 10 execuții
            recent_thetas = [h['theta'] for h in self.execution_history[-10:]]
            avg_theta = sum(recent_thetas) / len(recent_thetas)
            
            # Ajustează bazat pe parallelizable_fraction
            adjusted_theta = avg_theta * parallelizable_fraction
            
            return self._validate_factor(adjusted_theta, "theta")
        
        elif self.theta_mode == ThetaMode.EXPONENTIAL:
            # Creștere exponențială cu complexitatea
            # Formula: Θ = Θ_default × (1 - e^(-k × complexity))
            k = 2.0  # Factor de creștere
            theta = self.default_theta * (1.0 - math.exp(-k * workload_complexity))
            
            # Ajustează cu parallelizable_fraction
            theta *= parallelizable_fraction
            
            return self._validate_factor(theta, "theta")
        
        return self.default_theta
    
    def calculate_parallel_time(
        self,
        t_sequential: float,
        theta: Optional[float] = None,
        lambda_balance: Optional[float] = None,
        eta_overhead: Optional[float] = None,
        n_cores: Optional[int] = None
    ) -> float:
        """
        Calculează timpul de execuție paralel folosind formula Kronos:
        T_parallel = T_sequential / (N × Θ × Λ × η)
        
        Args:
            t_sequential: Timpul de execuție secvențial
            theta: Factorul de eficiență (sau None pentru default/adaptiv)
            lambda_balance: Factorul de load balancing (sau None pentru default)
            eta_overhead: Factorul de overhead (sau None pentru default)
            n_cores: Numărul de core-uri (sau None pentru default)
            
        Returns:
            Timpul de execuție paralel calculat
        """
        # Folosește valori default dacă nu sunt specificate
        theta = theta if theta is not None else self.default_theta
        lambda_balance = lambda_balance if lambda_balance is not None else self.default_lambda
        eta_overhead = eta_overhead if eta_overhead is not None else self.default_eta
        n_cores = n_cores if n_cores is not None else self.n_cores
        
        # Formula Kronos
        denominator = n_cores * theta * lambda_balance * eta_overhead
        
        # Evită împărțirea la zero
        if denominator <= 0.0:
            logger.warning(f"Invalid denominator: {denominator}, returning sequential time")
            return t_sequential
        
        t_parallel = t_sequential / denominator
        
        return t_parallel
    
    def calculate_amdahl_aristeia(
        self,
        parallelizable_fraction: float,
        n_cores: Optional[int] = None
    ) -> float:
        """
        Calculează speedup-ul maxim teoretic folosind Legea lui Amdahl.
        
        Legea lui Amdahl:
        Speedup = 1 / ((1 - P) + P/N)
        
        unde P = fracțiunea paralelizabilă, N = numărul de core-uri
        
        Aristeia (αριστεία) = excelență, virtute supremă în greaca antică
        
        Args:
            parallelizable_fraction: Fracțiunea paralelizabilă (0.0-1.0)
            n_cores: Numărul de core-uri (sau None pentru default)
            
        Returns:
            Speedup-ul maxim teoretic conform legii lui Amdahl
        """
        n_cores = n_cores if n_cores is not None else self.n_cores
        
        # Validare
        if not 0.0 <= parallelizable_fraction <= 1.0:
            raise ValueError(f"parallelizable_fraction must be [0.0, 1.0], got {parallelizable_fraction}")
        
        # Legea lui Amdahl
        serial_fraction = 1.0 - parallelizable_fraction
        speedup = 1.0 / (serial_fraction + parallelizable_fraction / n_cores)
        
        logger.debug(f"Amdahl's Law: P={parallelizable_fraction:.2f}, N={n_cores}, Speedup={speedup:.2f}x")
        
        return speedup
    
    def calculate_metrikos(
        self,
        t_sequential: float,
        theta: Optional[float] = None,
        lambda_balance: Optional[float] = None,
        eta_overhead: Optional[float] = None,
        n_cores: Optional[int] = None,
        amdahl_fraction: float = 1.0
    ) -> MetrikosTachys:
        """
        Calculează metrici complete de performanță pentru execuție paralelă.
        
        Args:
            t_sequential: Timpul de execuție secvențial
            theta: Factorul de eficiență (sau None pentru default)
            lambda_balance: Factorul de load balancing (sau None pentru default)
            eta_overhead: Factorul de overhead (sau None pentru default)
            n_cores: Numărul de core-uri (sau None pentru default)
            amdahl_fraction: Fracțiunea paralelizabilă pentru legea lui Amdahl
            
        Returns:
            MetrikosTachys cu metrici complete
        """
        # Folosește valori default dacă nu sunt specificate
        theta = theta if theta is not None else self.default_theta
        lambda_balance = lambda_balance if lambda_balance is not None else self.default_lambda
        eta_overhead = eta_overhead if eta_overhead is not None else self.default_eta
        n_cores = n_cores if n_cores is not None else self.n_cores
        
        # Calculează timpul paralel
        t_parallel = self.calculate_parallel_time(
            t_sequential, theta, lambda_balance, eta_overhead, n_cores
        )
        
        # Calculează speedup
        speedup = t_sequential / t_parallel if t_parallel > 0 else 1.0
        
        # Calculează eficiența
        efficiency = speedup / n_cores if n_cores > 0 else 0.0
        
        # Creează obiect MetrikosTachys
        metrikos = MetrikosTachys(
            t_sequential=t_sequential,
            t_parallel=t_parallel,
            speedup=speedup,
            efficiency=efficiency,
            theta=theta,
            lambda_balance=lambda_balance,
            eta_overhead=eta_overhead,
            n_cores=n_cores,
            amdahl_fraction=amdahl_fraction
        )
        
        # Adaugă la istoric pentru mod adaptiv
        self.execution_history.append({
            'theta': theta,
            'lambda': lambda_balance,
            'eta': eta_overhead,
            'speedup': speedup,
            'efficiency': efficiency
        })
        
        # Păstrează doar ultimele 100 de execuții
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
        
        logger.info(f"📊 Metrikos: Speedup={speedup:.2f}x, Efficiency={efficiency:.2%}, T_par={t_parallel:.3f}s")
        
        return metrikos
    
    def map_theta_to_dynamis(self, theta: float) -> float:
        """
        Mapează Theta (eficiență) la Dynamis (putere efectivă).
        
        Dynamis (δύναμις) = putere, capacitate în greaca antică
        
        Formula: Dynamis = N × Θ × Λ × η
        
        Args:
            theta: Factorul de eficiență
            
        Returns:
            Puterea efectivă (număr echivalent de core-uri)
        """
        dynamis = self.n_cores * theta * self.default_lambda * self.default_eta
        
        # Salvează maparea
        self.theta_to_dynamis_map[theta] = dynamis
        
        logger.debug(f"Θ={theta:.3f} → Dynamis={dynamis:.2f} effective cores")
        
        return dynamis
    
    def get_adaptive_theta(self) -> float:
        """
        Returnează valoarea adaptivă a lui Theta bazată pe istoric.
        
        Returns:
            Theta adaptiv calculat din istoric
        """
        if len(self.execution_history) < 3:
            return self.default_theta
        
        # Media ponderată: mai mult greutate la execuțiile recente
        weights = [1.0 / (i + 1) for i in range(len(self.execution_history))]
        weights.reverse()
        
        weighted_sum = sum(
            h['theta'] * w 
            for h, w in zip(self.execution_history, weights)
        )
        total_weight = sum(weights)
        
        adaptive_theta = weighted_sum / total_weight if total_weight > 0 else self.default_theta
        
        return self._validate_factor(adaptive_theta, "theta")
    
    def reset_history(self):
        """Resetează istoricul de execuții."""
        self.execution_history.clear()
        self.theta_to_dynamis_map.clear()
        logger.info("🔄 Execution history reset")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Returnează statistici despre execuțiile anterioare.
        
        Returns:
            Dicționar cu statistici
        """
        if not self.execution_history:
            return {
                'executions': 0,
                'avg_speedup': 0.0,
                'avg_efficiency': 0.0,
                'avg_theta': self.default_theta
            }
        
        avg_speedup = sum(h['speedup'] for h in self.execution_history) / len(self.execution_history)
        avg_efficiency = sum(h['efficiency'] for h in self.execution_history) / len(self.execution_history)
        avg_theta = sum(h['theta'] for h in self.execution_history) / len(self.execution_history)
        
        return {
            'executions': len(self.execution_history),
            'avg_speedup': avg_speedup,
            'avg_efficiency': avg_efficiency,
            'avg_theta': avg_theta,
            'max_speedup': max(h['speedup'] for h in self.execution_history),
            'min_speedup': min(h['speedup'] for h in self.execution_history)
        }
    
    def calculate_supreme_time(self, k: int = 100, P: int = None, U: int = 1) -> LambdaMetrics:
        """
        Calculate T_Λ^Supreme using Λ-MÖBIUS Engine.
        
        Args:
            k: Compression constant (default 100)
            P: Parallelism factor (None = use n_cores)
            U: Universe size/workload factor (default 1)
            
        Returns:
            Complete LambdaMetrics with all temporal compression values
        """
        if P is None:
            P = self.n_cores
        
        return self.lambda_mobius.calculate_T_Supreme(k, P, U)
    
    def get_lambda_state(self) -> LambdaState:
        """
        Get current Lambda state from Λ-MÖBIUS Engine.
        
        Returns:
            Current LambdaState (WRAP/STEADY/UNWRAP)
        """
        return self.lambda_mobius.get_current_state()
