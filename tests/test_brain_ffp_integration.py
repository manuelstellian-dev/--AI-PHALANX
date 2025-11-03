"""
Integration tests for LeondasBrain + FFP Pipeline

Tests the integration between LeondasBrain and Fractal Flux Pipeline.
"""

import pytest
import asyncio
from core.leonidasbrain import LeondasBrain
from control.fractal_pipeline import FractalFluxPipeline


class TestBrainFFPIntegration:
    """Tests for LeondasBrain + FFP integration."""
    
    def test_brain_initializes_ffp(self):
        """Test that LeondasBrain initializes FFP."""
        # Create minimal config
        config = {
            'cpu_cores': 4,
            'survival_threshold': 0.95
        }
        
        brain = LeondasBrain(config)
        
        # Verify FFP is initialized
        assert hasattr(brain, 'ffp')
        assert isinstance(brain.ffp, FractalFluxPipeline)
    
    def test_get_ffp_status(self):
        """Test get_ffp_status method."""
        config = {'cpu_cores': 4}
        brain = LeondasBrain(config)
        
        status = brain.get_ffp_status()
        
        assert isinstance(status, dict)
        assert 'running' in status
        assert 'cycle_count' in status
        assert 'scan_interval' in status
    
    def test_stop_ffp(self):
        """Test stop_ffp method."""
        config = {'cpu_cores': 4}
        brain = LeondasBrain(config)
        
        # Should not raise any errors
        brain.stop_ffp()
        
        # Verify FFP is stopped
        status = brain.get_ffp_status()
        assert status['running'] is False
    
    @pytest.mark.asyncio
    async def test_start_ffp_method_exists(self):
        """Test that start_ffp method exists and is async."""
        config = {'cpu_cores': 4}
        brain = LeondasBrain(config)
        
        # Verify method exists
        assert hasattr(brain, 'start_ffp')
        assert asyncio.iscoroutinefunction(brain.start_ffp)
