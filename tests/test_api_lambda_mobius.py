"""
Tests for Λ-MÖBIUS API endpoint

Tests the /api/v1/lambda-mobius endpoint functionality.
"""

import pytest
import api.server as server
from api.server import initialize_system

class TestLambdaMobiusEndpoint:
    """Tests for lambda-mobius API endpoint."""
    
    @pytest.mark.asyncio
    async def test_lambda_mobius_endpoint_unauthorized(self):
        """Test endpoint without authorization (brain not initialized)."""
        from api.routes.metrics import get_lambda_mobius_metrics
        
        # Save original state
        original_brain = server.leonidas_brain
        
        # Set brain to None
        server.leonidas_brain = None
        
        result = await get_lambda_mobius_metrics("test_token")
        
        # Should return error
        assert 'error' in result
        assert result['error'] == 'ΛΕΩΝΙΔΑΣ Brain not initialized'
        
        # Restore original state
        server.leonidas_brain = original_brain
    
    @pytest.mark.asyncio
    async def test_lambda_mobius_endpoint_with_token(self):
        """Test endpoint with valid token."""
        from api.routes.metrics import get_lambda_mobius_metrics
        
        # Initialize system
        config = {'hardware': {'cpu_cores': 4}}
        brain, processor = await initialize_system(config)
        
        # Save original state
        original_brain = server.leonidas_brain
        
        # Set brain for test
        server.leonidas_brain = brain
        
        result = await get_lambda_mobius_metrics("test_token")
        
        # Verify JSON structure
        assert 'current_metrics' in result
        assert 'current_state' in result
        assert 'state_value' in result
        assert 'history' in result
        assert 'timestamp' in result
        
        # Cleanup
        await brain.shutdown()
        
        # Restore original state
        server.leonidas_brain = original_brain
    
    @pytest.mark.asyncio
    async def test_lambda_mobius_metrics_structure(self):
        """Test that metrics have correct structure."""
        from api.routes.metrics import get_lambda_mobius_metrics
        
        # Initialize system
        config = {'hardware': {'cpu_cores': 4}}
        brain, processor = await initialize_system(config)
        
        # Save original state
        original_brain = server.leonidas_brain
        
        # Set brain for test
        server.leonidas_brain = brain
        
        result = await get_lambda_mobius_metrics("test_token")
        
        metrics = result['current_metrics']
        
        # Verify all 5 formulas are present
        assert 'T_wrap' in metrics
        assert 'T_mult' in metrics
        assert 'T_hybrid' in metrics
        assert 'T_balance' in metrics
        assert 'T_supreme' in metrics
        
        # Verify state information
        assert 'state' in metrics
        assert 'state_value' in metrics
        
        # Verify parameters
        assert 'k' in metrics
        assert 'P' in metrics
        assert 'U' in metrics
        
        # Verify all values are numeric
        assert isinstance(metrics['T_wrap'], (int, float))
        assert isinstance(metrics['T_mult'], (int, float))
        assert isinstance(metrics['T_hybrid'], (int, float))
        assert isinstance(metrics['T_balance'], (int, float))
        assert isinstance(metrics['T_supreme'], (int, float))
        
        # Cleanup
        await brain.shutdown()
        
        # Restore original state
        server.leonidas_brain = original_brain
    
    @pytest.mark.asyncio
    async def test_lambda_mobius_state_values(self):
        """Test that state values are valid."""
        from api.routes.metrics import get_lambda_mobius_metrics
        
        # Initialize system
        config = {'hardware': {'cpu_cores': 4}}
        brain, processor = await initialize_system(config)
        
        # Save original state
        original_brain = server.leonidas_brain
        
        # Set brain for test
        server.leonidas_brain = brain
        
        result = await get_lambda_mobius_metrics("test_token")
        
        # State should be one of: WRAP, STEADY, UNWRAP
        assert result['current_state'] in ['WRAP', 'STEADY', 'UNWRAP']
        
        # State value should be -1, 0, or 1
        assert result['state_value'] in [-1, 0, 1]
        
        # Cleanup
        await brain.shutdown()
        
        # Restore original state
        server.leonidas_brain = original_brain
    
    @pytest.mark.asyncio
    async def test_lambda_mobius_history(self):
        """Test that history is returned."""
        from api.routes.metrics import get_lambda_mobius_metrics
        
        # Initialize system
        config = {'hardware': {'cpu_cores': 4}}
        brain, processor = await initialize_system(config)
        
        # Save original state
        original_brain = server.leonidas_brain
        
        # Set brain for test
        server.leonidas_brain = brain
        
        result = await get_lambda_mobius_metrics("test_token")
        
        # History should be a list
        assert isinstance(result['history'], list)
        
        # If history has entries, verify structure
        if len(result['history']) > 0:
            entry = result['history'][0]
            assert 'T_wrap' in entry
            assert 'T_mult' in entry
            assert 'T_supreme' in entry
            assert 'state' in entry
            assert 'timestamp' in entry
        
        # Cleanup
        await brain.shutdown()
        
        # Restore original state
        server.leonidas_brain = original_brain
