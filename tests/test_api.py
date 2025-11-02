"""
Tests pentru modulele API (server, routes)
"""

import pytest
from fastapi.testclient import TestClient


class TestAPIServer:
    """Test suite pentru API server."""
    
    def test_load_config_default(self):
        """Test încărcare configurație default."""
        from api.server import load_config
        
        config = load_config()
        
        assert 'system' in config
        assert config['system']['name'] == "ΛΕΩΝΙΔΑΣ-AI PHALANX"
        assert "ΜΟΛΩΝ ΛΑΒΕ" in config['system']['motto']
    
    def test_verify_token_valid(self):
        """Test verificare token valid."""
        from api.server import verify_token
        from fastapi.security import HTTPAuthorizationCredentials
        import os
        
        # Setează token-ul în environment
        os.environ['SPARTA_AUTH_TOKEN'] = 'test_token'
        
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="test_token"
        )
        
        token = verify_token(credentials)
        assert token == "test_token"
    
    def test_verify_token_invalid(self):
        """Test verificare token invalid."""
        from api.server import verify_token
        from fastapi.security import HTTPAuthorizationCredentials
        from fastapi import HTTPException
        import os
        
        # Setează token-ul în environment
        os.environ['SPARTA_AUTH_TOKEN'] = 'correct_token'
        
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="wrong_token"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(credentials)
        
        assert exc_info.value.status_code == 401
    
    @pytest.mark.asyncio
    async def test_initialize_system(self):
        """Test inițializare sistem."""
        from api.server import initialize_system
        
        config = {
            'hardware': {'cpu_cores': 4, 'npu_tops': 50},
            'system': {'name': 'Test'}
        }
        
        brain, processor = await initialize_system(config)
        
        assert brain is not None
        assert processor is not None
        assert 'phalanx' in brain.modules
        assert 'hoplites' in brain.modules
        
        # Cleanup
        await brain.shutdown()


class TestHealthRoutes:
    """Test suite pentru health check routes."""
    
    @pytest.mark.asyncio
    async def test_basic_health_check(self):
        """Test health check de bază."""
        from api.routes.health import health_check
        
        result = await health_check()
        
        assert result['status'] == 'healthy'
        assert result['system'] == 'ΛΕΩΝΙΔΑΣ-AI PHALANX'
        assert result['motto'] == 'ΜΟΛΩΝ ΛΑΒΕ'
    
    @pytest.mark.asyncio
    async def test_detailed_health_no_server(self):
        """Test detailed health când serverul nu e inițializat."""
        from api.routes.health import detailed_health_check
        import api.server as server
        
        # Salvează starea originală
        original_brain = server.leonidas_brain
        original_processor = server.command_processor
        
        # Setează la None pentru test
        server.leonidas_brain = None
        server.command_processor = None
        
        result = await detailed_health_check("test_token")
        
        assert result['status'] == 'initializing'
        
        # Restabilește starea originală
        server.leonidas_brain = original_brain
        server.command_processor = original_processor
    
    @pytest.mark.asyncio
    async def test_detailed_health_with_server(self):
        """Test detailed health cu server inițializat."""
        from api.routes.health import detailed_health_check
        from api.server import initialize_system
        import api.server as server
        
        # Inițializează sistemul
        config = {'hardware': {'cpu_cores': 4}}
        brain, processor = await initialize_system(config)
        
        # Salvează starea originală
        original_brain = server.leonidas_brain
        original_processor = server.command_processor
        
        # Setează modulele pentru test
        server.leonidas_brain = brain
        server.command_processor = processor
        
        result = await detailed_health_check("test_token")
        
        assert result['status'] == 'healthy'
        assert 'brain' in result
        assert 'modules' in result
        
        # Cleanup
        await brain.shutdown()
        
        # Restabilește starea originală
        server.leonidas_brain = original_brain
        server.command_processor = original_processor
    
    @pytest.mark.asyncio
    async def test_survival_probability_no_server(self):
        """Test survival probability când serverul nu e inițializat."""
        from api.routes.health import survival_probability
        import api.server as server
        
        # Salvează starea originală
        original_brain = server.leonidas_brain
        
        # Setează la None pentru test
        server.leonidas_brain = None
        
        result = await survival_probability("test_token")
        
        assert result['status'] == 'initializing'
        assert result['survival_probability'] is None
        
        # Restabilește starea originală
        server.leonidas_brain = original_brain
    
    @pytest.mark.asyncio
    async def test_survival_probability_with_helot(self):
        """Test survival probability cu modul Helot."""
        from api.routes.health import survival_probability
        from api.server import initialize_system
        import api.server as server
        
        # Inițializează sistemul
        config = {'hardware': {'cpu_cores': 4}}
        brain, processor = await initialize_system(config)
        
        # Salvează starea originală
        original_brain = server.leonidas_brain
        
        # Setează brain-ul pentru test
        server.leonidas_brain = brain
        
        result = await survival_probability("test_token")
        
        assert result['status'] == 'ok'
        assert 'survival_probability' in result
        assert 0.0 <= result['survival_probability'] <= 1.0
        
        # Cleanup
        await brain.shutdown()
        
        # Restabilește starea originală
        server.leonidas_brain = original_brain
    
    @pytest.mark.asyncio
    async def test_survival_probability_no_helot(self):
        """Test survival probability fără modul Helot."""
        from api.routes.health import survival_probability
        from core.leonidasbrain import LeondasBrain
        import api.server as server
        
        # Creează un brain fără module Phalanx
        brain = LeondasBrain({})
        
        # Salvează starea originală
        original_brain = server.leonidas_brain
        
        # Setează brain-ul pentru test
        server.leonidas_brain = brain
        
        result = await survival_probability("test_token")
        
        assert result['status'] == 'error'
        assert 'error' in result
        
        # Cleanup
        await brain.shutdown()
        
        # Restabilește starea originală
        server.leonidas_brain = original_brain
