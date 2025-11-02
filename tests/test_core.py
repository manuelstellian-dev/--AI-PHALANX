"""
Tests pentru modulele Core (LeondasBrain, CommandProcessor)
"""

import pytest
import asyncio
from core.leonidasbrain import LeondasBrain
from core.commandprocessor import CommandProcessor


class TestLeondasBrain:
    """Test suite pentru LeondasBrain."""
    
    def test_initialization(self):
        """Test inițializare Λ-Core."""
        config = {
            'hardware': {'cpu_cores': 4},
            'current_workload': 0.5
        }
        brain = LeondasBrain(config)
        assert brain is not None
        assert brain.lambda_tas == 1.0
        assert not brain.is_running
    
    def test_calculate_lambda_tas(self):
        """Test calculare Λ-TAS."""
        config = {}
        brain = LeondasBrain(config)
        
        # Test cu paralelism 4 și workload 0.5
        # Formula: T_new = (T_1 * ln(U + 1)) / (1 - 1 / (k * P))
        # Unde k=100, P=4, U=0.5
        lambda_tas = brain.calculate_lambda_tas(4, 0.5)
        # Verifică că rezultatul este în range-ul valid
        assert 0.1 <= lambda_tas <= 10.0
        
        # Test cu workload 0
        # ln(0 + 1) = ln(1) = 0, deci rezultatul va fi limitat la 0.1
        lambda_tas = brain.calculate_lambda_tas(4, 0)
        assert 0.1 <= lambda_tas <= 1.0
    
    def test_get_status(self):
        """Test obținere status."""
        config = {}
        brain = LeondasBrain(config)
        status = brain.get_status()
        
        assert 'is_running' in status
        assert 'lambda_tas' in status
        assert status['motto'] == "ΜΟΛΩΝ ΛΑΒΕ"


class TestCommandProcessor:
    """Test suite pentru CommandProcessor."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test inițializare CommandProcessor."""
        modules = {'phalanx': {}, 'hoplites': {}}
        processor = CommandProcessor(modules)
        assert processor is not None
        assert processor.adaptation_factor == 1.0
    
    @pytest.mark.asyncio
    async def test_unknown_command(self):
        """Test comandă necunoscută."""
        modules = {'phalanx': {}, 'hoplites': {}}
        processor = CommandProcessor(modules)
        
        result = await processor.process_command({
            'type': 'unknown_command',
            'payload': {}
        })
        
        assert not result['success']
        assert 'Unknown command type' in result['error']
    
    def test_adaptation_factor(self):
        """Test setare/obținere adaptation factor."""
        modules = {'phalanx': {}, 'hoplites': {}}
        processor = CommandProcessor(modules)
        
        processor.set_adaptation_factor(1.5)
        assert processor.get_adaptation_factor() == 1.5
