"""
Tests pentru modulele Hoplites (Guard, Shield, Oracle, Weapon, Messenger)
"""

import pytest
import asyncio
from hoplites.spartanguard import SpartanGuard
from hoplites.shieldbearer import ShieldBearer
from hoplites.battleoracle import BattleOracle
from hoplites.weaponmaster import WeaponMaster
from hoplites.messenger import Messenger


class TestSpartanGuard:
    """Test suite pentru Spartan Guard."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test inițializare Spartan Guard."""
        config = {}
        guard = SpartanGuard(config)
        assert guard is not None
    
    @pytest.mark.asyncio
    async def test_encryption_decryption(self):
        """Test criptare/decriptare."""
        config = {}
        guard = SpartanGuard(config)
        
        plaintext = "Test message for encryption"
        encrypted = await guard.encrypt(plaintext)
        decrypted = await guard.decrypt(encrypted)
        
        assert decrypted == plaintext
    
    @pytest.mark.asyncio
    async def test_hash_data(self):
        """Test hash-uire date."""
        config = {}
        guard = SpartanGuard(config)
        
        data = "test data"
        hash1 = await guard.hash_data(data)
        hash2 = await guard.hash_data(data)
        
        assert hash1 == hash2  # Hash-ul trebuie să fie consistent


class TestShieldBearer:
    """Test suite pentru Shield Bearer."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test inițializare Shield Bearer."""
        config = {'airgap_mode': 'strict'}
        shield = ShieldBearer(config)
        assert shield is not None
        assert shield.airgap_mode == 'strict'
    
    @pytest.mark.asyncio
    async def test_check_airgap(self):
        """Test verificare Air-Gap."""
        config = {'airgap_mode': 'disabled'}
        shield = ShieldBearer(config)
        
        result = await shield.check_airgap()
        assert isinstance(result, bool)


class TestBattleOracle:
    """Test suite pentru Battle Oracle."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test inițializare Battle Oracle."""
        config = {'npu_tops': 50}
        oracle = BattleOracle(config)
        assert oracle is not None
        assert oracle.npu_tops == 50
    
    @pytest.mark.asyncio
    async def test_analyze_risk(self):
        """Test analiză risc."""
        config = {}
        oracle = BattleOracle(config)
        
        scenario = {
            'name': 'Test Scenario',
            'risk_factors': ['factor1', 'factor2'],
            'severity': 0.5
        }
        
        result = await oracle.analyze_risk(scenario)
        
        assert 'threat_level' in result
        assert 'success_probability' in result
        assert 'recommended_action' in result


class TestWeaponMaster:
    """Test suite pentru Weapon Master."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test inițializare Weapon Master."""
        config = {'external_access_enabled': False}
        weapon = WeaponMaster(config)
        assert weapon is not None
        assert not weapon.external_access_enabled
    
    @pytest.mark.asyncio
    async def test_blocked_external_access(self):
        """Test blocare acces extern."""
        config = {'external_access_enabled': False}
        weapon = WeaponMaster(config)
        
        result = await weapon.execute_external_query({
            'type': 'http_get',
            'target': 'https://example.com'
        })
        
        assert not result['success']
        assert result['blocked']


class TestMessenger:
    """Test suite pentru Messenger."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test inițializare Messenger."""
        config = {}
        messenger = Messenger(config)
        assert messenger is not None
    
    @pytest.mark.asyncio
    async def test_send_message_without_encryption(self):
        """Test trimitere mesaj fără criptare."""
        config = {}
        messenger = Messenger(config)
        
        result = await messenger.send_secure_message({
            'recipient': 'test_user',
            'content': 'Test message',
            'encrypt': False
        })
        
        assert result['success']
        assert 'message_id' in result
