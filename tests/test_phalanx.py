"""
Tests pentru modulele Phalanx (Helot, Agoge, Krypteia, Thermopylae)
"""

import pytest
import asyncio
from phalanx.helot import HelotModule
from phalanx.agoge import AgogeModule
from phalanx.krypteia import KrypteiaModule
from phalanx.thermopylae import ThermopylaeModule


class TestHelotModule:
    """Test suite pentru Helot."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test inițializare Helot."""
        config = {}
        helot = HelotModule(config)
        assert helot is not None
        assert helot.survival_probability == 1.0
    
    @pytest.mark.asyncio
    async def test_monitor_resources(self):
        """Test monitorizare resurse."""
        config = {}
        helot = HelotModule(config)
        resources = await helot.monitor_resources()
        
        assert 'cpu_percent' in resources
        assert 'memory_percent' in resources
        assert 'disk_percent' in resources
    
    @pytest.mark.asyncio
    async def test_survival_probability(self):
        """Test calculare probabilitate supraviețuire."""
        config = {}
        helot = HelotModule(config)
        prob = await helot.get_survival_probability()
        
        assert 0.0 <= prob <= 1.0


class TestAgogeModule:
    """Test suite pentru Agoge."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test inițializare Agoge."""
        config = {'learning_rate': 0.01}
        agoge = AgogeModule(config)
        assert agoge is not None
        assert agoge.adaptation_factor == 1.0
    
    @pytest.mark.asyncio
    async def test_training_cycle(self):
        """Test ciclu de antrenament."""
        config = {}
        agoge = AgogeModule(config)
        
        result = await agoge.run_training_cycle({'data': 'test'})
        
        assert 'cycle' in result
        assert 'adaptation_factor' in result
        assert result['status'] == 'completed'


class TestKrypteiaModule:
    """Test suite pentru Krypteia."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test inițializare Krypteia."""
        config = {}
        krypteia = KrypteiaModule(config)
        assert krypteia is not None
        assert not krypteia.is_monitoring
    
    @pytest.mark.asyncio
    async def test_threat_assessment(self):
        """Test evaluare amenințări."""
        config = {}
        krypteia = KrypteiaModule(config)
        
        assessment = await krypteia.get_threat_assessment()
        
        assert 'threat_level' in assessment
        assert 'threats_detected' in assessment


class TestThermopylaeModule:
    """Test suite pentru Thermopylae."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test inițializare Thermopylae."""
        config = {'survival_threshold': 0.95}
        thermopylae = ThermopylaeModule(config)
        assert thermopylae is not None
        assert not thermopylae.protocol_activated
    
    @pytest.mark.asyncio
    async def test_protocol_arming(self):
        """Test armare protocol."""
        config = {}
        thermopylae = ThermopylaeModule(config)
        
        await thermopylae.arm_protocol()
        assert thermopylae.is_armed
        
        await thermopylae.disarm_protocol()
        assert not thermopylae.is_armed
