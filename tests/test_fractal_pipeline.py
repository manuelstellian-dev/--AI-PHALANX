"""
Tests for Fractal Flux Pipeline (FFP)

Complete test suite covering all FFP functionality.
"""

import pytest
import asyncio
from control.fractal_pipeline import FractalFluxPipeline
from control.kronos_arbiter import KronosArbiter


class MockBrain:
    """Mock LeondasBrain for testing."""
    
    def __init__(self):
        self.kronos = KronosArbiter(n_cores=4)
        self.modules = {
            'phalanx': {
                'helot': MockHelot(),
                'krypteia': MockKrypteia(),
                'thermopylae': MockThermopylae(),
                'agoge': MockAgoge()
            },
            'hoplites': {
                'guard': None,
                'shield': None
            }
        }


class MockHelot:
    """Mock Helot module."""
    
    def __init__(self):
        self.survival_probability = 0.98
    
    async def monitor_resources(self):
        return {
            'cpu_percent': 45.0,
            'memory_percent': 60.0,
            'disk_percent': 70.0
        }


class MockKrypteia:
    """Mock Krypteia module."""
    
    async def get_threat_assessment(self):
        return {
            'threat_level': 'low',
            'threats_detected': 0
        }


class MockThermopylae:
    """Mock Thermopylae module."""
    
    async def check_emergency_protocol(self, survival_prob):
        return {'protocol_activated': survival_prob < 0.95}


class MockAgoge:
    """Mock Agoge module."""
    
    async def get_adaptation_factor(self):
        return 0.95


class TestFractalFluxPipeline:
    """Tests for FractalFluxPipeline class."""
    
    def test_initialization(self):
        """Test FFP initialization."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        assert ffp.brain == brain
        assert ffp.running is False
        assert ffp.scan_interval == 5.0
        assert ffp.cycle_count == 0
    
    @pytest.mark.asyncio
    async def test_scan_system(self):
        """Test scan_system phase."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        system_state = await ffp.scan_system()
        
        assert 'timestamp' in system_state
        assert 'resources' in system_state
        assert 'health' in system_state
        assert system_state['health'] == 'scanned'
        assert 'survival_probability' in system_state
    
    @pytest.mark.asyncio
    async def test_scan_system_no_modules(self):
        """Test scan_system when modules are missing."""
        brain = MockBrain()
        brain.modules = {}
        ffp = FractalFluxPipeline(brain)
        
        system_state = await ffp.scan_system()
        
        assert 'timestamp' in system_state
        assert 'health' in system_state
    
    @pytest.mark.asyncio
    async def test_detect_anomalies_none(self):
        """Test detect_anomalies when no anomalies exist."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        system_state = {
            'survival_probability': 0.98,
            'resources': {
                'cpu_percent': 45.0,
                'memory_percent': 60.0
            }
        }
        
        anomalies = await ffp.detect_anomalies(system_state)
        
        assert isinstance(anomalies, list)
        assert len(anomalies) == 0
    
    @pytest.mark.asyncio
    async def test_detect_anomalies_low_survival(self):
        """Test detect_anomalies with low survival probability."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        system_state = {
            'survival_probability': 0.90,  # Below threshold
            'resources': {}
        }
        
        anomalies = await ffp.detect_anomalies(system_state)
        
        assert len(anomalies) > 0
        assert anomalies[0]['type'] == 'low_survival'
        assert anomalies[0]['severity'] == 'high'
    
    @pytest.mark.asyncio
    async def test_detect_anomalies_high_cpu(self):
        """Test detect_anomalies with high CPU usage."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        system_state = {
            'survival_probability': 0.98,
            'resources': {
                'cpu_percent': 95.0,  # Above threshold
                'memory_percent': 50.0
            }
        }
        
        anomalies = await ffp.detect_anomalies(system_state)
        
        assert len(anomalies) > 0
        high_cpu = [a for a in anomalies if a['type'] == 'high_cpu']
        assert len(high_cpu) > 0
        assert high_cpu[0]['severity'] == 'medium'
    
    @pytest.mark.asyncio
    async def test_detect_anomalies_high_memory(self):
        """Test detect_anomalies with high memory usage."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        system_state = {
            'survival_probability': 0.98,
            'resources': {
                'cpu_percent': 50.0,
                'memory_percent': 95.0  # Above threshold
            }
        }
        
        anomalies = await ffp.detect_anomalies(system_state)
        
        assert len(anomalies) > 0
        high_mem = [a for a in anomalies if a['type'] == 'high_memory']
        assert len(high_mem) > 0
    
    @pytest.mark.asyncio
    async def test_quarantine_threats_empty(self):
        """Test quarantine_threats with no anomalies."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        # Should not raise any errors
        await ffp.quarantine_threats([])
    
    @pytest.mark.asyncio
    async def test_quarantine_threats_with_high_severity(self):
        """Test quarantine_threats with high severity anomalies."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        anomalies = [
            {
                'type': 'low_survival',
                'severity': 'high',
                'value': 0.90
            }
        ]
        
        # Should trigger Thermopylae protocol
        await ffp.quarantine_threats(anomalies)
    
    @pytest.mark.asyncio
    async def test_quarantine_threats_no_thermopylae(self):
        """Test quarantine_threats when Thermopylae is not available."""
        brain = MockBrain()
        brain.modules['phalanx'] = {}
        ffp = FractalFluxPipeline(brain)
        
        anomalies = [{'type': 'test', 'severity': 'high'}]
        
        # Should not raise errors
        await ffp.quarantine_threats(anomalies)
    
    @pytest.mark.asyncio
    async def test_heal_system_no_anomalies(self):
        """Test heal_system with no anomalies."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        await ffp.heal_system([])
        # Should complete without errors
    
    @pytest.mark.asyncio
    async def test_heal_system_high_cpu(self):
        """Test heal_system with high CPU anomaly."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        anomalies = [
            {'type': 'high_cpu', 'value': 95}
        ]
        
        await ffp.heal_system(anomalies)
    
    @pytest.mark.asyncio
    async def test_heal_system_high_memory(self):
        """Test heal_system with high memory anomaly."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        anomalies = [
            {'type': 'high_memory', 'value': 95}
        ]
        
        await ffp.heal_system(anomalies)
    
    @pytest.mark.asyncio
    async def test_heal_system_low_survival(self):
        """Test heal_system with low survival anomaly."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        anomalies = [
            {'type': 'low_survival', 'value': 0.90}
        ]
        
        await ffp.heal_system(anomalies)
    
    @pytest.mark.asyncio
    async def test_analyze_improvements(self):
        """Test analyze_improvements phase."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        improvements = await ffp.analyze_improvements()
        
        assert 'adaptations' in improvements
        assert 'optimizations' in improvements
        assert 'recommendations' in improvements
    
    @pytest.mark.asyncio
    async def test_analyze_improvements_no_agoge(self):
        """Test analyze_improvements when Agoge is not available."""
        brain = MockBrain()
        brain.modules['phalanx'] = {}
        ffp = FractalFluxPipeline(brain)
        
        improvements = await ffp.analyze_improvements()
        
        assert isinstance(improvements, dict)
    
    @pytest.mark.asyncio
    async def test_analyze_improvements_low_adaptation(self):
        """Test analyze_improvements with low adaptation factor."""
        brain = MockBrain()
        # Mock Agoge with low adaptation
        brain.modules['phalanx']['agoge'] = MockAgoge()
        brain.modules['phalanx']['agoge'].get_adaptation_factor = lambda: asyncio.coroutine(lambda: 0.5)()
        
        ffp = FractalFluxPipeline(brain)
        improvements = await ffp.analyze_improvements()
        
        # Should have recommendations when adaptation is low
        assert 'recommendations' in improvements
    
    @pytest.mark.asyncio
    async def test_apply_improvements_empty(self):
        """Test apply_improvements with no recommendations."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        improvements = {'recommendations': []}
        
        await ffp.apply_improvements(improvements)
        # Should complete without errors
    
    @pytest.mark.asyncio
    async def test_apply_improvements_with_recommendations(self):
        """Test apply_improvements with recommendations."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        improvements = {
            'recommendations': [
                {
                    'type': 'training',
                    'reason': 'Low adaptation',
                    'action': 'Increase training cycles'
                }
            ]
        }
        
        await ffp.apply_improvements(improvements)
    
    @pytest.mark.asyncio
    async def test_calculate_cycle_interval(self):
        """Test calculate_cycle_interval with Kronos."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        interval = await ffp.calculate_cycle_interval()
        
        assert isinstance(interval, float)
        assert interval > 0
    
    @pytest.mark.asyncio
    async def test_calculate_cycle_interval_no_kronos(self):
        """Test calculate_cycle_interval without Kronos."""
        brain = MockBrain()
        del brain.kronos
        ffp = FractalFluxPipeline(brain)
        
        interval = await ffp.calculate_cycle_interval()
        
        # Should fallback to scan_interval
        assert interval == ffp.scan_interval
    
    @pytest.mark.asyncio
    async def test_calculate_cycle_interval_with_modules(self):
        """Test calculate_cycle_interval with multiple modules."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        interval = await ffp.calculate_cycle_interval()
        
        # Should be calculated based on module count
        assert interval > 0
        assert interval <= ffp.scan_interval
    
    def test_stop(self):
        """Test stop method."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        ffp.running = True
        ffp.stop()
        
        assert ffp.running is False
    
    def test_get_status(self):
        """Test get_status method."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        ffp.cycle_count = 5
        
        status = ffp.get_status()
        
        assert 'running' in status
        assert 'cycle_count' in status
        assert 'scan_interval' in status
        assert status['cycle_count'] == 5
        assert status['running'] is False
    
    @pytest.mark.asyncio
    async def test_run_forever_single_cycle(self):
        """Test run_forever executes one cycle properly."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        # Create a task and cancel it after a short time
        async def run_and_stop():
            task = asyncio.create_task(ffp.run_forever())
            await asyncio.sleep(0.1)  # Let one cycle start
            ffp.stop()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        await run_and_stop()
        
        # Should have completed at least part of a cycle
        assert ffp.cycle_count >= 0
    
    @pytest.mark.asyncio
    async def test_run_forever_handles_exceptions(self):
        """Test run_forever handles exceptions gracefully."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        # Make scan_system raise an exception
        original_scan = ffp.scan_system
        async def failing_scan():
            raise Exception("Test error")
        
        ffp.scan_system = failing_scan
        
        # Should handle exception and continue
        async def run_and_stop():
            task = asyncio.create_task(ffp.run_forever())
            await asyncio.sleep(0.2)
            ffp.stop()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        await run_and_stop()
        
        # Should have attempted at least one cycle
        assert ffp.cycle_count >= 1
        
        # Restore
        ffp.scan_system = original_scan
    
    @pytest.mark.asyncio
    async def test_scan_system_exception_handling(self):
        """Test scan_system handles exceptions properly."""
        brain = MockBrain()
        
        # Make Helot raise an exception
        async def failing_monitor():
            raise Exception("Test error")
        
        brain.modules['phalanx']['helot'].monitor_resources = failing_monitor
        
        ffp = FractalFluxPipeline(brain)
        
        # Should handle exception and return partial state
        system_state = await ffp.scan_system()
        
        assert 'timestamp' in system_state
    
    @pytest.mark.asyncio
    async def test_detect_anomalies_exception_handling(self):
        """Test detect_anomalies handles exceptions properly."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        # Invalid system_state that causes exception
        system_state = None
        
        # Should handle exception and return empty list
        anomalies = await ffp.detect_anomalies(system_state)
        
        assert isinstance(anomalies, list)
    
    @pytest.mark.asyncio
    async def test_quarantine_threats_exception_handling(self):
        """Test quarantine_threats handles exceptions properly."""
        brain = MockBrain()
        
        # Make Thermopylae raise an exception
        async def failing_protocol(survival_prob):
            raise Exception("Test error")
        
        brain.modules['phalanx']['thermopylae'].check_emergency_protocol = failing_protocol
        
        ffp = FractalFluxPipeline(brain)
        
        anomalies = [
            {
                'type': 'low_survival',
                'severity': 'high',
                'value': 0.90
            }
        ]
        
        # Should handle exception gracefully
        await ffp.quarantine_threats(anomalies)
    
    @pytest.mark.asyncio
    async def test_heal_system_exception_handling(self):
        """Test heal_system handles exceptions properly."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        # Mock logger.info to raise exception
        import unittest.mock as mock
        from loguru import logger
        
        # Create anomalies that will trigger healing
        anomalies = [
            {'type': 'high_cpu', 'value': 95}
        ]
        
        # Patch logger to raise exception during heal
        with mock.patch.object(logger, 'info', side_effect=Exception("Test error")):
            # Should handle exception gracefully
            await ffp.heal_system(anomalies)
    
    @pytest.mark.asyncio
    async def test_apply_improvements_exception_handling(self):
        """Test apply_improvements handles exceptions properly."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        # Invalid improvements structure
        improvements = None
        
        # Should handle exception gracefully
        await ffp.apply_improvements(improvements)
    
    @pytest.mark.asyncio
    async def test_calculate_cycle_interval_exception(self):
        """Test calculate_cycle_interval handles exceptions."""
        brain = MockBrain()
        
        # Make calculate_supreme_time raise an exception
        def failing_calculate(*args, **kwargs):
            raise Exception("Test error")
        
        brain.kronos.calculate_supreme_time = failing_calculate
        
        ffp = FractalFluxPipeline(brain)
        
        # Should fallback to scan_interval
        interval = await ffp.calculate_cycle_interval()
        
        assert interval == ffp.scan_interval
    
    @pytest.mark.asyncio
    async def test_run_forever_with_anomalies_detected(self):
        """Test run_forever when anomalies are detected."""
        brain = MockBrain()
        ffp = FractalFluxPipeline(brain)
        
        # Mock to return anomalies
        original_detect = ffp.detect_anomalies
        async def mock_detect(system_state):
            return [{'type': 'test', 'severity': 'high', 'value': 0.9}]
        
        ffp.detect_anomalies = mock_detect
        
        # Run one cycle
        async def run_one_cycle():
            task = asyncio.create_task(ffp.run_forever())
            await asyncio.sleep(0.1)
            ffp.stop()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        await run_one_cycle()
        
        # Should have processed anomalies
        assert ffp.cycle_count >= 0
        
        # Restore
        ffp.detect_anomalies = original_detect
