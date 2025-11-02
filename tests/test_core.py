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
    
    @pytest.mark.asyncio
    async def test_initialize_phalanx(self):
        """Test inițializare module Phalanx."""
        config = {}
        brain = LeondasBrain(config)
        
        phalanx_modules = {
            'helot': {'name': 'helot'},
            'agoge': {'name': 'agoge'}
        }
        await brain.initialize_phalanx(phalanx_modules)
        
        assert 'phalanx' in brain.modules
        assert brain.modules['phalanx'] == phalanx_modules
    
    @pytest.mark.asyncio
    async def test_initialize_hoplites(self):
        """Test inițializare module Hoplites."""
        config = {}
        brain = LeondasBrain(config)
        
        hoplite_modules = {
            'guard': {'name': 'guard'},
            'shield': {'name': 'shield'}
        }
        await brain.initialize_hoplites(hoplite_modules)
        
        assert 'hoplites' in brain.modules
        assert brain.modules['hoplites'] == hoplite_modules
    
    @pytest.mark.asyncio
    async def test_shutdown(self):
        """Test oprire controlată."""
        config = {}
        brain = LeondasBrain(config)
        brain.is_running = True
        
        await brain.shutdown()
        
        assert not brain.is_running
    
    def test_calculate_lambda_tas_edge_cases(self):
        """Test edge cases pentru calculate_lambda_tas."""
        config = {}
        brain = LeondasBrain(config)
        
        # Test cu workload negativ (ar trebui normalizat la 0)
        lambda_tas = brain.calculate_lambda_tas(4, -5)
        assert 0.1 <= lambda_tas <= 10.0
        
        # Test cu paralelism 0 (ar trebui normalizat la 1)
        lambda_tas = brain.calculate_lambda_tas(0, 0.5)
        assert 0.1 <= lambda_tas <= 10.0
        
        # Test cu paralelism negativ
        lambda_tas = brain.calculate_lambda_tas(-2, 0.5)
        assert 0.1 <= lambda_tas <= 10.0
        
        # Test cu workload foarte mare
        lambda_tas = brain.calculate_lambda_tas(8, 100)
        assert 0.1 <= lambda_tas <= 10.0
    
    def test_calculate_universe_expansion_factor(self):
        """Test calculare factor de expansiune."""
        modules = {'phalanx': {}, 'hoplites': {}}
        processor = CommandProcessor(modules)
        
        processor.active_tasks = 5
        processor.data_vault_size_mb = 100.0
        processor.adaptation_factor = 1.2
        
        U = processor.calculate_universe_expansion_factor()
        assert U > 0
        assert isinstance(U, float)
    
    @pytest.mark.asyncio
    async def test_handle_status_command_empty_modules(self):
        """Test comandă status cu module goale."""
        modules = {'phalanx': {}, 'hoplites': {}}
        processor = CommandProcessor(modules)
        
        result = await processor.process_command({
            'type': 'status',
            'payload': {}
        })
        
        assert result['success']
        assert result['motto'] == "ΜΟΛΩΝ ΛΑΒΕ"
        assert 'modules' in result
    
    @pytest.mark.asyncio
    async def test_handle_encryption_missing_guard(self):
        """Test encryption când Guard nu e disponibil."""
        modules = {'phalanx': {}, 'hoplites': {}}
        processor = CommandProcessor(modules)
        
        result = await processor.process_command({
            'type': 'encrypt_data',
            'payload': {'data': 'test'}
        })
        
        assert not result['success']
        assert 'Guard' in result['error']
    
    @pytest.mark.asyncio
    async def test_handle_airgap_check_missing_shield(self):
        """Test airgap check când Shield nu e disponibil."""
        modules = {'phalanx': {}, 'hoplites': {}}
        processor = CommandProcessor(modules)
        
        result = await processor.process_command({
            'type': 'check_airgap',
            'payload': {}
        })
        
        assert not result['success']
        assert 'Shield' in result['error']
    
    @pytest.mark.asyncio
    async def test_handle_message_send_missing_messenger(self):
        """Test trimitere mesaj când Messenger nu e disponibil."""
        modules = {'phalanx': {}, 'hoplites': {}}
        processor = CommandProcessor(modules)
        
        result = await processor.process_command({
            'type': 'send_message',
            'payload': {'message': 'test'}
        })
        
        assert not result['success']
        assert 'Messenger' in result['error']
    
    @pytest.mark.asyncio
    async def test_handle_risk_analysis_missing_oracle(self):
        """Test analiză risc când Oracle nu e disponibil."""
        modules = {'phalanx': {}, 'hoplites': {}}
        processor = CommandProcessor(modules)
        
        result = await processor.process_command({
            'type': 'analyze_risk',
            'payload': {'scenario': 'test'}
        })
        
        assert not result['success']
        assert 'Oracle' in result['error']
    
    @pytest.mark.asyncio
    async def test_handle_agoge_training_missing_agoge(self):
        """Test training când Agoge nu e disponibil."""
        modules = {'phalanx': {}, 'hoplites': {}}
        processor = CommandProcessor(modules)
        
        result = await processor.process_command({
            'type': 'train_agoge',
            'payload': {'data': 'test'}
        })
        
        assert not result['success']
        assert 'Agoge' in result['error']
