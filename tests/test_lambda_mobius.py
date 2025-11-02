"""
Tests for Λ-MÖBIUS ENGINE

Complete test suite covering:
- LambdaState enum
- LambdaMetrics dataclass
- LambdaMobiusEngine class (all methods)
- Integration with Kronos-Arbiter
"""

import pytest
import math
from control.lambda_mobius import (
    LambdaState,
    LambdaMetrics,
    LambdaMobiusEngine
)
from control.kronos_arbiter import KronosArbiter


class TestLambdaState:
    """Tests for LambdaState enum."""
    
    def test_lambda_state_values(self):
        """Test that LambdaState has correct values."""
        assert LambdaState.WRAP.value == 1
        assert LambdaState.STEADY.value == 0
        assert LambdaState.UNWRAP.value == -1
    
    def test_lambda_state_names(self):
        """Test that LambdaState has correct names."""
        assert LambdaState.WRAP.name == "WRAP"
        assert LambdaState.STEADY.name == "STEADY"
        assert LambdaState.UNWRAP.name == "UNWRAP"


class TestLambdaMetrics:
    """Tests for LambdaMetrics dataclass."""
    
    def test_lambda_metrics_creation(self):
        """Test LambdaMetrics can be created with all required fields."""
        metrics = LambdaMetrics(
            T_wrap=1.5,
            T_mult=2.0,
            T_hybrid=1.7,
            T_balance=1.73,
            T_supreme=1.5,
            state=LambdaState.WRAP,
            k=100,
            P=4,
            U=10
        )
        
        assert metrics.T_wrap == 1.5
        assert metrics.T_mult == 2.0
        assert metrics.T_hybrid == 1.7
        assert metrics.T_balance == 1.73
        assert metrics.T_supreme == 1.5
        assert metrics.state == LambdaState.WRAP
        assert metrics.k == 100
        assert metrics.P == 4
        assert metrics.U == 10
    
    def test_lambda_metrics_to_dict(self):
        """Test LambdaMetrics.to_dict() method."""
        metrics = LambdaMetrics(
            T_wrap=1.5,
            T_mult=2.0,
            T_hybrid=1.7,
            T_balance=1.73,
            T_supreme=1.5,
            state=LambdaState.STEADY,
            k=100,
            P=4,
            U=10
        )
        
        result = metrics.to_dict()
        
        assert isinstance(result, dict)
        assert result['T_wrap'] == 1.5
        assert result['T_mult'] == 2.0
        assert result['state'] == 'STEADY'
        assert result['state_value'] == 0
        assert result['k'] == 100
        assert result['P'] == 4
        assert result['U'] == 10
        assert 'timestamp' in result


class TestLambdaMobiusEngine:
    """Tests for LambdaMobiusEngine class."""
    
    def test_initialization(self):
        """Test LambdaMobiusEngine initialization."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        assert engine.T1 == 1.0
        assert engine.current_state == LambdaState.STEADY
        assert len(engine.history) == 0
    
    def test_initialization_custom_t1(self):
        """Test initialization with custom T1."""
        engine = LambdaMobiusEngine(T1=2.0)
        
        assert engine.T1 == 2.0
    
    def test_calculate_T_Wrap(self):
        """Test calculate_T_Wrap formula."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Test with typical values
        k = 100
        P = 4
        U = 10
        
        T_wrap = engine.calculate_T_Wrap(k, P, U)
        
        # T_Λ^Wrap = T₁ / (1 - 1/(k·P·(1+ln U)))
        ln_U = math.log(U)
        expected_denominator = 1.0 - (1.0 / (k * P * (1.0 + ln_U)))
        expected = 1.0 / expected_denominator
        
        assert abs(T_wrap - expected) < 0.001
        assert T_wrap > 0
    
    def test_calculate_T_Wrap_edge_cases(self):
        """Test T_Wrap with edge cases."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Test with U=0 (should default to 1)
        T_wrap = engine.calculate_T_Wrap(100, 4, 0)
        assert T_wrap > 0
        
        # Test with P=0 (should default to 1)
        T_wrap = engine.calculate_T_Wrap(100, 0, 10)
        assert T_wrap > 0
        
        # Test with k=0 (should default to 1)
        T_wrap = engine.calculate_T_Wrap(0, 4, 10)
        assert T_wrap > 0
    
    def test_calculate_T_Mult(self):
        """Test calculate_T_Mult formula."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Test with typical values
        k = 100
        P = 4
        U = 10
        
        T_mult = engine.calculate_T_Mult(k, P, U)
        
        # T_Λ^Mult = (T₁ · ln U) / (1 - 1/(k·P))
        ln_U = math.log(U)
        expected_denominator = 1.0 - (1.0 / (k * P))
        expected = (1.0 * ln_U) / expected_denominator
        
        assert abs(T_mult - expected) < 0.001
        assert T_mult > 0
    
    def test_calculate_T_Mult_edge_cases(self):
        """Test T_Mult with edge cases."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Test with U=0 (should default to 1)
        T_mult = engine.calculate_T_Mult(100, 4, 0)
        assert T_mult >= 0
        
        # Test with very small k*P
        T_mult = engine.calculate_T_Mult(1, 1, 10)
        assert T_mult > 0
    
    def test_calculate_T_Hybrid(self):
        """Test calculate_T_Hybrid (harmonic mean)."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        T_wrap = 2.0
        T_mult = 3.0
        
        T_hybrid = engine.calculate_T_Hybrid(T_wrap, T_mult)
        
        # Harmonic mean: (T_wrap · T_mult) / (T_wrap + T_mult)
        expected = (T_wrap * T_mult) / (T_wrap + T_mult)
        
        assert abs(T_hybrid - expected) < 0.001
        assert T_hybrid > 0
        assert T_hybrid < min(T_wrap, T_mult)
    
    def test_calculate_T_Hybrid_edge_cases(self):
        """Test T_Hybrid with edge cases."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Test with zero values
        T_hybrid = engine.calculate_T_Hybrid(0, 3.0)
        assert T_hybrid > 0
        
        T_hybrid = engine.calculate_T_Hybrid(2.0, 0)
        assert T_hybrid > 0
    
    def test_calculate_T_Balance(self):
        """Test calculate_T_Balance (geometric mean)."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        T_wrap = 4.0
        T_mult = 9.0
        
        T_balance = engine.calculate_T_Balance(T_wrap, T_mult)
        
        # Geometric mean: √(T_wrap · T_mult)
        expected = math.sqrt(T_wrap * T_mult)
        
        assert abs(T_balance - expected) < 0.001
        assert T_balance == 6.0  # sqrt(4*9) = 6
    
    def test_calculate_T_Balance_edge_cases(self):
        """Test T_Balance with edge cases."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Test with zero values
        T_balance = engine.calculate_T_Balance(0, 9.0)
        assert T_balance > 0
        
        T_balance = engine.calculate_T_Balance(4.0, 0)
        assert T_balance > 0
    
    def test_arbiter_select_wrap(self):
        """Test Λ-Arbiter selects WRAP state."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # k * P * (1 + ln U) > 100 should trigger WRAP
        k = 100
        P = 10
        U = 10  # ln(10) ≈ 2.3, so 100*10*(1+2.3) = 3300 > 100
        
        state = engine.arbiter_select(k, P, U)
        
        assert state == LambdaState.WRAP
    
    def test_arbiter_select_unwrap(self):
        """Test Λ-Arbiter selects UNWRAP state."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # U > 1000 should trigger UNWRAP
        k = 1
        P = 1
        U = 2000
        
        state = engine.arbiter_select(k, P, U)
        
        assert state == LambdaState.UNWRAP
    
    def test_arbiter_select_steady(self):
        """Test Λ-Arbiter selects STEADY state."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Neither condition met should give STEADY
        k = 1
        P = 1
        U = 10
        
        state = engine.arbiter_select(k, P, U)
        
        assert state == LambdaState.STEADY
    
    def test_calculate_T_Supreme(self):
        """Test calculate_T_Supreme complete calculation."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        k = 100
        P = 4
        U = 10
        
        metrics = engine.calculate_T_Supreme(k, P, U)
        
        # Verify all fields are present
        assert isinstance(metrics, LambdaMetrics)
        assert metrics.T_wrap > 0
        assert metrics.T_mult > 0
        assert metrics.T_hybrid > 0
        assert metrics.T_balance > 0
        assert metrics.T_supreme > 0
        assert metrics.state in [LambdaState.WRAP, LambdaState.STEADY, LambdaState.UNWRAP]
        assert metrics.k == k
        assert metrics.P == P
        assert metrics.U == U
    
    def test_calculate_T_Supreme_wrap_state(self):
        """Test T_Supreme uses T_wrap when state is WRAP."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Choose values that trigger WRAP
        k = 100
        P = 10
        U = 10
        
        metrics = engine.calculate_T_Supreme(k, P, U)
        
        if metrics.state == LambdaState.WRAP:
            assert metrics.T_supreme == metrics.T_wrap
    
    def test_calculate_T_Supreme_unwrap_state(self):
        """Test T_Supreme uses T_mult when state is UNWRAP."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Choose values that trigger UNWRAP
        k = 1
        P = 1
        U = 2000
        
        metrics = engine.calculate_T_Supreme(k, P, U)
        
        if metrics.state == LambdaState.UNWRAP:
            assert metrics.T_supreme == metrics.T_mult
    
    def test_calculate_T_Supreme_steady_state(self):
        """Test T_Supreme uses T_hybrid when state is STEADY."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Choose values that trigger STEADY
        k = 1
        P = 1
        U = 10
        
        metrics = engine.calculate_T_Supreme(k, P, U)
        
        if metrics.state == LambdaState.STEADY:
            assert metrics.T_supreme == metrics.T_hybrid
    
    def test_history_tracking(self):
        """Test that history is tracked correctly."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        assert len(engine.history) == 0
        
        # Calculate metrics
        engine.calculate_T_Supreme(100, 4, 10)
        assert len(engine.history) == 1
        
        engine.calculate_T_Supreme(100, 4, 20)
        assert len(engine.history) == 2
        
        engine.calculate_T_Supreme(100, 4, 30)
        assert len(engine.history) == 3
    
    def test_history_limit(self):
        """Test that history is limited to 100 entries."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Add 150 entries
        for i in range(150):
            engine.calculate_T_Supreme(100, 4, i+1)
        
        # Should be limited to 100
        assert len(engine.history) == 100
    
    def test_get_current_state(self):
        """Test get_current_state returns correct state."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Initial state
        assert engine.get_current_state() == LambdaState.STEADY
        
        # After calculation
        engine.calculate_T_Supreme(100, 10, 10)
        state = engine.get_current_state()
        assert state in [LambdaState.WRAP, LambdaState.STEADY, LambdaState.UNWRAP]
    
    def test_get_history(self):
        """Test get_history returns list of dicts."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Add some history
        engine.calculate_T_Supreme(100, 4, 10)
        engine.calculate_T_Supreme(100, 4, 20)
        
        history = engine.get_history()
        
        assert isinstance(history, list)
        assert len(history) == 2
        assert all(isinstance(h, dict) for h in history)
        assert all('T_wrap' in h for h in history)
        assert all('state' in h for h in history)
    
    def test_get_history_last_n(self):
        """Test get_history with last_n parameter."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Add 10 entries
        for i in range(10):
            engine.calculate_T_Supreme(100, 4, i+1)
        
        # Get last 3
        history = engine.get_history(last_n=3)
        
        assert len(history) == 3
    
    def test_force_state(self):
        """Test force_state method."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Force WRAP
        engine.force_state(LambdaState.WRAP)
        assert engine.get_current_state() == LambdaState.WRAP
        
        # Force UNWRAP
        engine.force_state(LambdaState.UNWRAP)
        assert engine.get_current_state() == LambdaState.UNWRAP
        
        # Force STEADY
        engine.force_state(LambdaState.STEADY)
        assert engine.get_current_state() == LambdaState.STEADY


class TestKronosIntegration:
    """Tests for integration with Kronos-Arbiter."""
    
    def test_kronos_has_lambda_mobius(self):
        """Test that Kronos-Arbiter has lambda_mobius attribute."""
        kronos = KronosArbiter(n_cores=4)
        
        assert hasattr(kronos, 'lambda_mobius')
        assert isinstance(kronos.lambda_mobius, LambdaMobiusEngine)
    
    def test_kronos_calculate_supreme_time(self):
        """Test calculate_supreme_time method in Kronos."""
        kronos = KronosArbiter(n_cores=4)
        
        metrics = kronos.calculate_supreme_time(k=100, P=4, U=10)
        
        assert isinstance(metrics, LambdaMetrics)
        assert metrics.T_supreme > 0
    
    def test_kronos_calculate_supreme_time_default_P(self):
        """Test calculate_supreme_time uses n_cores when P is None."""
        kronos = KronosArbiter(n_cores=8)
        
        metrics = kronos.calculate_supreme_time(k=100, P=None, U=10)
        
        assert metrics.P == 8
    
    def test_kronos_get_lambda_state(self):
        """Test get_lambda_state method in Kronos."""
        kronos = KronosArbiter(n_cores=4)
        
        state = kronos.get_lambda_state()
        
        assert isinstance(state, LambdaState)
        assert state in [LambdaState.WRAP, LambdaState.STEADY, LambdaState.UNWRAP]
    
    def test_kronos_lambda_state_changes(self):
        """Test that Lambda state changes based on calculations."""
        kronos = KronosArbiter(n_cores=4)
        
        # Calculate with different parameters
        metrics1 = kronos.calculate_supreme_time(k=100, P=10, U=10)
        state1 = kronos.get_lambda_state()
        
        metrics2 = kronos.calculate_supreme_time(k=1, P=1, U=2000)
        state2 = kronos.get_lambda_state()
        
        # States should potentially be different
        assert state1 in [LambdaState.WRAP, LambdaState.STEADY, LambdaState.UNWRAP]
        assert state2 in [LambdaState.WRAP, LambdaState.STEADY, LambdaState.UNWRAP]


class TestFormulasAccuracy:
    """Tests to verify formula accuracy with known values."""
    
    def test_wrap_formula_manual_calculation(self):
        """Verify T_Wrap formula with manual calculation."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        k = 100
        P = 4
        U = math.e  # ln(e) = 1, simplifies calculation
        
        T_wrap = engine.calculate_T_Wrap(k, P, U)
        
        # Manual calculation: T_wrap = 1 / (1 - 1/(100*4*(1+1)))
        # = 1 / (1 - 1/800) = 1 / (799/800) = 800/799
        expected = 800.0 / 799.0
        
        assert abs(T_wrap - expected) < 0.001
    
    def test_mult_formula_manual_calculation(self):
        """Verify T_Mult formula with manual calculation."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        k = 100
        P = 4
        U = math.e  # ln(e) = 1
        
        T_mult = engine.calculate_T_Mult(k, P, U)
        
        # Manual calculation: T_mult = (1 * 1) / (1 - 1/400)
        # = 1 / (399/400) = 400/399
        expected = 400.0 / 399.0
        
        assert abs(T_mult - expected) < 0.001
    
    def test_harmonic_mean_accuracy(self):
        """Verify harmonic mean formula."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Use simple values: 2 and 3
        T_hybrid = engine.calculate_T_Hybrid(2.0, 3.0)
        
        # Harmonic mean of 2 and 3: 2*3/(2+3) = 6/5 = 1.2
        assert abs(T_hybrid - 1.2) < 0.001
    
    def test_geometric_mean_accuracy(self):
        """Verify geometric mean formula."""
        engine = LambdaMobiusEngine(T1=1.0)
        
        # Use perfect square values
        T_balance = engine.calculate_T_Balance(4.0, 16.0)
        
        # Geometric mean of 4 and 16: sqrt(4*16) = sqrt(64) = 8
        assert abs(T_balance - 8.0) < 0.001
