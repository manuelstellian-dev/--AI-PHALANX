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
    
    @pytest.mark.asyncio
    async def test_helot_get_status(self):
        """Test obținere status Helot complet."""
        config = {}
        helot = HelotModule(config)
        
        status = await helot.get_status()
        
        assert status['module'] == 'Helot'
        assert status['status'] == 'active'
        assert 'survival_probability' in status
        assert 'resources' in status
    
    @pytest.mark.asyncio
    async def test_helot_parallelism_factor(self):
        """Test calcul factor de paralelism."""
        config = {'simulated_gpu_load': 0.5}
        helot = HelotModule(config)
        
        resources = await helot.monitor_resources()
        
        assert 'parallelism_factor' in resources
        assert resources['parallelism_factor'] >= 1.0
    
    @pytest.mark.asyncio
    async def test_helot_optimize_resources(self):
        """Test optimizare resurse."""
        config = {}
        helot = HelotModule(config)
        
        # Ar trebui să ruleze fără erori
        await helot.optimize_resources()
    
    @pytest.mark.asyncio
    async def test_helot_critical_resources(self):
        """Test resurse critice."""
        config = {
            'resource_thresholds': {
                'cpu_critical': 50.0,  # Prag foarte jos pentru test
                'memory_critical': 50.0,
                'disk_critical': 50.0
            }
        }
        helot = HelotModule(config)
        
        resources = await helot.monitor_resources()
        # Verifică că probabilitatea este calculată
        assert 0.0 <= helot.survival_probability <= 1.0
    
    @pytest.mark.asyncio
    async def test_agoge_get_adaptation_factor(self):
        """Test obținere factor de adaptare."""
        config = {}
        agoge = AgogeModule(config)
        
        factor = await agoge.get_adaptation_factor()
        
        assert factor == 1.0
    
    @pytest.mark.asyncio
    async def test_agoge_adjust_learning_rate(self):
        """Test ajustare learning rate."""
        config = {}
        agoge = AgogeModule(config)
        
        await agoge.adjust_learning_rate(0.05)
        assert agoge.learning_rate == 0.05
        
        # Test limitare learning rate
        await agoge.adjust_learning_rate(0.5)  # Prea mare
        assert agoge.learning_rate <= 0.1
        
        await agoge.adjust_learning_rate(0.0001)  # Prea mic
        assert agoge.learning_rate >= 0.001
    
    @pytest.mark.asyncio
    async def test_agoge_reset_adaptation(self):
        """Test resetare adaptare."""
        config = {}
        agoge = AgogeModule(config)
        
        # Schimbă factorul de adaptare
        agoge.adaptation_factor = 1.5
        
        await agoge.reset_adaptation()
        
        assert agoge.adaptation_factor == 1.0
    
    @pytest.mark.asyncio
    async def test_agoge_multiple_training_cycles(self):
        """Test cicluri multiple de antrenament."""
        config = {}
        agoge = AgogeModule(config)
        
        for i in range(3):
            result = await agoge.run_training_cycle({'data': f'test{i}'})
            assert result['cycle'] == i + 1
            assert 0.5 <= result['adaptation_factor'] <= 2.0
    
    @pytest.mark.asyncio
    async def test_krypteia_start_stop_monitoring(self):
        """Test start/stop monitorizare."""
        config = {}
        krypteia = KrypteiaModule(config)
        
        await krypteia.start_monitoring()
        assert krypteia.is_monitoring
        
        # Test start când deja pornit
        await krypteia.start_monitoring()
        assert krypteia.is_monitoring
        
        await krypteia.stop_monitoring()
        assert not krypteia.is_monitoring
        
        # Test stop când deja oprit
        await krypteia.stop_monitoring()
        assert not krypteia.is_monitoring
    
    @pytest.mark.asyncio
    async def test_krypteia_report_threat(self):
        """Test raportare amenințare."""
        config = {}
        krypteia = KrypteiaModule(config)
        
        threat = {'type': 'network_intrusion', 'severity': 'high'}
        await krypteia.report_threat(threat)
        
        assessment = await krypteia.get_threat_assessment()
        assert assessment['threats_detected'] == 1
    
    @pytest.mark.asyncio
    async def test_krypteia_clear_threat_history(self):
        """Test ștergere istoric amenințări."""
        config = {}
        krypteia = KrypteiaModule(config)
        
        # Adaugă câteva amenințări
        await krypteia.report_threat({'type': 'test1'})
        await krypteia.report_threat({'type': 'test2'})
        
        await krypteia.clear_threat_history()
        
        assessment = await krypteia.get_threat_assessment()
        assert assessment['threats_detected'] == 0
    
    @pytest.mark.asyncio
    async def test_krypteia_threat_level_escalation(self):
        """Test escaladare nivel amenințare."""
        config = {}
        krypteia = KrypteiaModule(config)
        
        # Adaugă amenințări gradual
        for i in range(6):
            await krypteia.report_threat({'type': f'threat{i}'})
        
        # Actualizează manual threat level (de obicei se face în monitoring loop)
        krypteia._update_threat_level()
        
        assessment = await krypteia.get_threat_assessment()
        # Cu 6 amenințări, ar trebui să fie critical
        assert assessment['threat_level'] == 'critical'
    
    @pytest.mark.asyncio
    async def test_thermopylae_get_status(self):
        """Test obținere status Thermopylae."""
        config = {}
        thermopylae = ThermopylaeModule(config)
        
        status = await thermopylae.get_status()
        
        assert status['module'] == 'Thermopylae'
        assert 'is_armed' in status
        assert 'protocol_activated' in status
        assert 'warning' in status
    
    @pytest.mark.asyncio
    async def test_thermopylae_test_protocol(self):
        """Test protocol simulare."""
        config = {}
        thermopylae = ThermopylaeModule(config)
        
        result = await thermopylae.test_protocol()
        
        assert result['test'] == 'thermopylae_protocol'
        assert 'steps' in result
        assert result['status'] == 'simulation_complete'
    
    @pytest.mark.asyncio
    async def test_thermopylae_check_emergency_not_armed(self):
        """Test protocol emergency când nu e armat."""
        config = {'thermopylae_armed': False}
        thermopylae = ThermopylaeModule(config)
        
        # Nu ar trebui să activeze protocolul dacă nu e armat
        await thermopylae.check_emergency_protocol(0.5)
        
        assert not thermopylae.protocol_activated
    
    @pytest.mark.asyncio
    async def test_thermopylae_check_emergency_above_threshold(self):
        """Test protocol când probabilitatea e OK."""
        config = {'survival_threshold': 0.95, 'thermopylae_armed': True}
        thermopylae = ThermopylaeModule(config)
        
        # Probabilitate bună - nu ar trebui să activeze
        await thermopylae.check_emergency_protocol(0.98)
        
        assert not thermopylae.protocol_activated
    
    @pytest.mark.asyncio
    async def test_thermopylae_activate_protocol_duplicate(self):
        """Test activare protocol duplicat."""
        config = {}
        thermopylae = ThermopylaeModule(config)
        
        thermopylae.protocol_activated = True
        
        # Nu ar trebui să execute din nou
        await thermopylae.activate_protocol()
        
        assert thermopylae.protocol_activated
    
    @pytest.mark.asyncio
    async def test_thermopylae_destroy_keys_file_not_found(self):
        """Test distrugere chei când fișierul nu există."""
        config = {
            'keys_path': '/nonexistent/path.yaml',
            'base_path': '/tmp'
        }
        thermopylae = ThermopylaeModule(config)
        
        # Ar trebui să ruleze fără erori chiar dacă fișierul nu există
        await thermopylae._destroy_cryptographic_keys()
    
    @pytest.mark.asyncio
    async def test_thermopylae_destroy_vault_not_found(self):
        """Test distrugere vault când directorul nu există."""
        config = {
            'vault_path': '/nonexistent/vault',
            'base_path': '/tmp'
        }
        thermopylae = ThermopylaeModule(config)
        
        # Ar trebui să ruleze fără erori chiar dacă directorul nu există
        await thermopylae._destroy_encrypted_vault()
    
    @pytest.mark.asyncio
    async def test_thermopylae_config_paths(self):
        """Test configurare căi pentru protocol."""
        config = {
            'survival_threshold': 0.90,
            'thermopylae_armed': False
        }
        thermopylae = ThermopylaeModule(config)
        
        assert thermopylae.critical_threshold == 0.90
        assert not thermopylae.is_armed


class TestHelotEdgeCases:
    """Test edge cases pentru Helot."""
    
    @pytest.mark.asyncio
    async def test_helot_critical_cpu(self):
        """Test Helot cu CPU critic."""
        config = {
            'resource_thresholds': {
                'cpu_critical': 0.1,  # Foarte jos pentru a fi sigur că e depășit
                'memory_critical': 0.1,
                'disk_critical': 0.1
            }
        }
        helot = HelotModule(config)
        
        resources = await helot.monitor_resources()
        
        # Verifică că probabilitatea e redusă din cauza resurselor critice
        assert helot.survival_probability < 1.0
    
    @pytest.mark.asyncio
    async def test_helot_with_gpu_load(self):
        """Test Helot cu GPU load simulat."""
        config = {
            'simulated_gpu_load': 0.8
        }
        helot = HelotModule(config)
        
        resources = await helot.monitor_resources()
        
        # Factorul de paralelism ar trebui să fie mai mare cu GPU
        assert resources['parallelism_factor'] > 1.0


class TestThermopylaeEdgeCases:
    """Test edge cases pentru Thermopylae."""
    
    @pytest.mark.asyncio
    async def test_thermopylae_emergency_armed(self):
        """Test protocol emergency când e armat și sub prag."""
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                'survival_threshold': 0.95,
                'thermopylae_armed': True,
                'base_path': tmpdir,
                'keys_path': 'keys.yaml',
                'vault_path': 'vault'
            }
            thermopylae = ThermopylaeModule(config)
            
            # Check emergency cu probabilitate critică
            await thermopylae.check_emergency_protocol(0.5)
            
            # Protocolul ar trebui să fie activat
            assert thermopylae.protocol_activated
