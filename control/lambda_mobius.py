"""
Λ-MÖBIUS ENGINE - Temporal Compression Engine with 5 Layers

Implements the complete Λ-MÖBIUS architecture:
1. T_Λ^Wrap - Wrapping/Compression layer
2. T_Λ^Mult - Multiplication/Distribution layer
3. T_Λ^Hybrid - Harmonic mean of Wrap and Mult
4. T_Λ^Balance - Geometric mean of Wrap and Mult
5. T_Λ^Supreme - Final supreme temporal metric

The Λ-Arbiter selects the optimal state (+1 WRAP, 0 STEADY, -1 UNWRAP)
based on system conditions.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import math
import time
from loguru import logger


class LambdaState(Enum):
    """
    Lambda States for Möbius Engine.
    
    WRAP (+1): Compression mode - optimizing for speed
    STEADY (0): Steady state - balanced operation
    UNWRAP (-1): Diagnostic mode - detailed analysis
    """
    WRAP = 1      # Compression mode
    STEADY = 0    # Steady state
    UNWRAP = -1   # Diagnostic mode


@dataclass
class LambdaMetrics:
    """
    Complete metrics for Λ-MÖBIUS Engine.
    
    Attributes:
        T_wrap: Wrapping/Compression time
        T_mult: Multiplication/Distribution time
        T_hybrid: Harmonic mean of T_wrap and T_mult
        T_balance: Geometric mean of T_wrap and T_mult
        T_supreme: Final supreme temporal metric
        state: Current Lambda state
        k: Compression constant
        P: Parallelism factor (cores)
        U: Universe size (workload factor)
        timestamp: When metrics were calculated
    """
    T_wrap: float
    T_mult: float
    T_hybrid: float
    T_balance: float
    T_supreme: float
    state: LambdaState
    k: int
    P: int
    U: int
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            'T_wrap': self.T_wrap,
            'T_mult': self.T_mult,
            'T_hybrid': self.T_hybrid,
            'T_balance': self.T_balance,
            'T_supreme': self.T_supreme,
            'state': self.state.name,
            'state_value': self.state.value,
            'k': self.k,
            'P': self.P,
            'U': self.U,
            'timestamp': self.timestamp
        }


class LambdaMobiusEngine:
    """
    Λ-MÖBIUS Engine: Complete temporal compression engine with 5 layers.
    
    Implements formulas:
    1. T_Λ^Wrap = T₁ / (1 - 1/(k·P·(1+ln U)))
    2. T_Λ^Mult = (T₁ · ln U) / (1 - 1/(k·P))
    3. T_Λ^Hybrid = (T_wrap · T_mult) / (T_wrap + T_mult)  [Harmonic mean]
    4. T_Λ^Balance = √(T_wrap · T_mult)  [Geometric mean]
    5. T_Λ^Supreme = Arbiter-selected optimal time
    
    The Λ-Arbiter selects the optimal state based on system conditions.
    """
    
    def __init__(self, T1: float = 1.0):
        """
        Initialize Λ-MÖBIUS Engine.
        
        Args:
            T1: Base time unit (default 1.0 second)
        """
        self.T1 = T1
        self.current_state = LambdaState.STEADY
        self.history: List[LambdaMetrics] = []
        
        logger.info(f"⚡ Λ-MÖBIUS Engine initialized with T1={T1}s")
    
    def calculate_T_Wrap(self, k: int, P: int, U: int) -> float:
        """
        Calculate T_Λ^Wrap - Wrapping/Compression time.
        
        Formula: T_Λ^Wrap = T₁ / (1 - 1/(k·P·(1+ln U)))
        
        Args:
            k: Compression constant (typically 100)
            P: Parallelism factor (number of cores)
            U: Universe size (workload factor)
            
        Returns:
            T_wrap time value
        """
        if U <= 0:
            U = 1
        if P <= 0:
            P = 1
        if k <= 0:
            k = 1
        
        try:
            ln_U = math.log(U)
            denominator = 1.0 - (1.0 / (k * P * (1.0 + ln_U)))
            
            # Avoid division by zero or negative denominator
            if denominator <= 0.0:
                logger.warning(f"Invalid T_Wrap denominator: {denominator}, using fallback")
                return self.T1
            
            T_wrap = self.T1 / denominator
            
            # Sanity check: T_wrap should be positive and reasonable
            if T_wrap <= 0 or T_wrap > 1000:
                logger.warning(f"T_Wrap out of bounds: {T_wrap}, using T1")
                return self.T1
            
            return T_wrap
            
        except Exception as e:
            logger.error(f"Error calculating T_Wrap: {e}")
            return self.T1
    
    def calculate_T_Mult(self, k: int, P: int, U: int) -> float:
        """
        Calculate T_Λ^Mult - Multiplication/Distribution time.
        
        Formula: T_Λ^Mult = (T₁ · ln U) / (1 - 1/(k·P))
        
        Args:
            k: Compression constant (typically 100)
            P: Parallelism factor (number of cores)
            U: Universe size (workload factor)
            
        Returns:
            T_mult time value
        """
        if U <= 0:
            U = 1
        if P <= 0:
            P = 1
        if k <= 0:
            k = 1
        
        try:
            ln_U = math.log(U)
            denominator = 1.0 - (1.0 / (k * P))
            
            # Avoid division by zero or negative denominator
            if denominator <= 0.0:
                logger.warning(f"Invalid T_Mult denominator: {denominator}, using fallback")
                return self.T1 * ln_U if ln_U > 0 else self.T1
            
            T_mult = (self.T1 * ln_U) / denominator
            
            # Sanity check
            if T_mult < 0 or T_mult > 1000:
                logger.warning(f"T_Mult out of bounds: {T_mult}, using T1*ln(U)")
                return self.T1 * ln_U if ln_U > 0 else self.T1
            
            return T_mult
            
        except Exception as e:
            logger.error(f"Error calculating T_Mult: {e}")
            return self.T1
    
    def calculate_T_Hybrid(self, T_wrap: float, T_mult: float) -> float:
        """
        Calculate T_Λ^Hybrid - Harmonic mean of T_wrap and T_mult.
        
        Formula: T_Λ^Hybrid = (T_wrap · T_mult) / (T_wrap + T_mult)
        
        Args:
            T_wrap: Wrapping time
            T_mult: Multiplication time
            
        Returns:
            T_hybrid time value (harmonic mean)
        """
        if T_wrap <= 0 or T_mult <= 0:
            logger.warning(f"Invalid inputs for T_Hybrid: T_wrap={T_wrap}, T_mult={T_mult}")
            return min(T_wrap, T_mult) if min(T_wrap, T_mult) > 0 else self.T1
        
        # At this point, both T_wrap and T_mult are > 0, so denominator is always > 0
        denominator = T_wrap + T_mult
        T_hybrid = (T_wrap * T_mult) / denominator
        return T_hybrid
    
    def calculate_T_Balance(self, T_wrap: float, T_mult: float) -> float:
        """
        Calculate T_Λ^Balance - Geometric mean of T_wrap and T_mult.
        
        Formula: T_Λ^Balance = √(T_wrap · T_mult)
        
        Args:
            T_wrap: Wrapping time
            T_mult: Multiplication time
            
        Returns:
            T_balance time value (geometric mean)
        """
        if T_wrap <= 0 or T_mult <= 0:
            logger.warning(f"Invalid inputs for T_Balance: T_wrap={T_wrap}, T_mult={T_mult}")
            return min(T_wrap, T_mult) if min(T_wrap, T_mult) > 0 else self.T1
        
        T_balance = math.sqrt(T_wrap * T_mult)
        return T_balance
    
    def arbiter_select(self, k: int, P: int, U: int) -> LambdaState:
        """
        Λ-Arbiter: Selects the optimal Lambda state based on system conditions.
        
        Logic:
        - If k * P * (1 + ln U) > 100: WRAP (compression mode)
        - Else if U > 1000: UNWRAP (diagnostic mode)
        - Else: STEADY (balanced operation)
        
        Args:
            k: Compression constant
            P: Parallelism factor
            U: Universe size
            
        Returns:
            Selected LambdaState
        """
        try:
            ln_U = math.log(U) if U > 0 else 0
            
            # Arbiter logic
            if k * P * (1 + ln_U) > 100:
                state = LambdaState.WRAP
                logger.debug(f"🔄 Λ-Arbiter selected WRAP (k·P·(1+ln U) = {k * P * (1 + ln_U):.2f})")
            elif U > 1000:
                state = LambdaState.UNWRAP
                logger.debug(f"🔍 Λ-Arbiter selected UNWRAP (U = {U})")
            else:
                state = LambdaState.STEADY
                logger.debug(f"⚖️ Λ-Arbiter selected STEADY")
            
            return state
            
        except Exception as e:
            logger.error(f"Error in arbiter_select: {e}")
            return LambdaState.STEADY
    
    def calculate_T_Supreme(self, k: int, P: int, U: int) -> LambdaMetrics:
        """
        Calculate T_Λ^Supreme - Final supreme temporal metric.
        
        Calculates all layers and uses Λ-Arbiter to select the optimal time.
        
        Args:
            k: Compression constant (typically 100)
            P: Parallelism factor (number of cores)
            U: Universe size (workload factor)
            
        Returns:
            Complete LambdaMetrics with all calculated values
        """
        # Calculate all layers
        T_wrap = self.calculate_T_Wrap(k, P, U)
        T_mult = self.calculate_T_Mult(k, P, U)
        T_hybrid = self.calculate_T_Hybrid(T_wrap, T_mult)
        T_balance = self.calculate_T_Balance(T_wrap, T_mult)
        
        # Use Λ-Arbiter to select state
        state = self.arbiter_select(k, P, U)
        self.current_state = state
        
        # Select T_supreme based on state
        if state == LambdaState.WRAP:
            T_supreme = T_wrap
        elif state == LambdaState.UNWRAP:
            T_supreme = T_mult
        else:  # STEADY
            T_supreme = T_hybrid
        
        # Create metrics object
        metrics = LambdaMetrics(
            T_wrap=T_wrap,
            T_mult=T_mult,
            T_hybrid=T_hybrid,
            T_balance=T_balance,
            T_supreme=T_supreme,
            state=state,
            k=k,
            P=P,
            U=U
        )
        
        # Add to history
        self.history.append(metrics)
        
        # Keep only last 100 entries
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        logger.info(f"⚡ T_Λ^Supreme calculated: {T_supreme:.3f}s (state={state.name})")
        
        return metrics
    
    def get_current_state(self) -> LambdaState:
        """
        Get the current Lambda state.
        
        Returns:
            Current LambdaState
        """
        return self.current_state
    
    def get_history(self, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get history of metrics calculations.
        
        Args:
            last_n: Number of recent entries to return (None = all)
            
        Returns:
            List of metrics dictionaries
        """
        history = self.history
        
        if last_n is not None and last_n > 0:
            history = history[-last_n:]
        
        return [m.to_dict() for m in history]
    
    def force_state(self, state: LambdaState):
        """
        Force a specific Lambda state (for testing).
        
        Args:
            state: LambdaState to force
        """
        self.current_state = state
        logger.warning(f"⚠️ Lambda state forced to {state.name}")
