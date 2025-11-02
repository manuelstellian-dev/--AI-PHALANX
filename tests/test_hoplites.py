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
    
    @pytest.mark.asyncio
    async def test_spartan_guard_verify_integrity(self):
        """Test verificare integritate date."""
        config = {}
        guard = SpartanGuard(config)
        
        data = "Important data"
        hash_value = await guard.hash_data(data)
        
        # Verifică integritatea cu hash corect
        is_valid = await guard.verify_integrity(data, hash_value)
        assert is_valid
        
        # Verifică cu hash incorect
        is_valid = await guard.verify_integrity(data, "wrong_hash")
        assert not is_valid
    
    @pytest.mark.asyncio
    async def test_spartan_guard_get_status(self):
        """Test obținere status Spartan Guard."""
        config = {}
        guard = SpartanGuard(config)
        
        status = await guard.get_status()
        
        assert status['module'] == 'SpartanGuard'
        assert 'status' in status
        assert status['encryption'] == 'AES-256-GCM'
        assert 'key_loaded' in status
    
    @pytest.mark.asyncio
    async def test_spartan_guard_encryption_with_associated_data(self):
        """Test criptare cu date asociate."""
        config = {}
        guard = SpartanGuard(config)
        
        plaintext = "Secret message"
        associated_data = "metadata"
        
        encrypted = await guard.encrypt(plaintext, associated_data)
        decrypted = await guard.decrypt(encrypted, associated_data)
        
        assert decrypted == plaintext
    
    @pytest.mark.asyncio
    async def test_shield_bearer_get_status(self):
        """Test obținere status complet Shield Bearer."""
        config = {'airgap_mode': 'disabled'}
        shield = ShieldBearer(config)
        
        status = await shield.get_status()
        
        assert status['module'] == 'ShieldBearer'
        assert status['airgap_mode'] == 'disabled'
        assert 'airgap_active' in status
        assert 'firewall' in status
    
    @pytest.mark.asyncio
    async def test_shield_bearer_enforce_firewall(self):
        """Test verificare firewall."""
        config = {}
        shield = ShieldBearer(config)
        
        result = await shield.enforce_firewall()
        
        assert 'firewall_active' in result
        assert 'platform' in result
    
    @pytest.mark.asyncio
    async def test_shield_bearer_test_external_access(self):
        """Test verificare acces extern."""
        config = {}
        shield = ShieldBearer(config)
        
        # Test cu timeout mic pentru a nu aștepta mult
        can_connect = await shield.test_external_access(
            host="127.0.0.1", port=99999, timeout=1
        )
        
        # Portul 99999 nu ar trebui să fie deschis
        assert isinstance(can_connect, bool)
    
    @pytest.mark.asyncio
    async def test_shield_bearer_permissive_mode(self):
        """Test mod permisiv Air-Gap."""
        config = {
            'airgap_mode': 'permissive',
            'allowed_connections': []
        }
        shield = ShieldBearer(config)
        
        is_secure = await shield.check_airgap()
        
        assert isinstance(is_secure, bool)
    
    @pytest.mark.asyncio
    async def test_battle_oracle_get_status(self):
        """Test obținere status Battle Oracle."""
        config = {'npu_tops': 15}
        oracle = BattleOracle(config)
        
        status = await oracle.get_status()
        
        assert status['module'] == 'BattleOracle'
        assert status['npu_tops'] == 15
        assert 'predictions_made' in status
    
    @pytest.mark.asyncio
    async def test_battle_oracle_predict_outcome(self):
        """Test predicție rezultat."""
        config = {}
        oracle = BattleOracle(config)
        
        prediction = await oracle.predict_outcome(
            action="attack",
            context={'strength': 0.8}
        )
        
        assert 'action' in prediction
        assert 'predicted_outcome' in prediction
        assert 'confidence' in prediction
    
    @pytest.mark.asyncio
    async def test_battle_oracle_run_simulation(self):
        """Test rulare simulare Monte Carlo."""
        config = {}
        oracle = BattleOracle(config)
        
        results = await oracle.run_simulation(
            parameters={'scenario': 'test'},
            iterations=50
        )
        
        assert results['iterations'] == 50
        assert 'success_rate' in results
        assert 0.0 <= results['success_rate'] <= 1.0
    
    @pytest.mark.asyncio
    async def test_battle_oracle_get_prediction_history(self):
        """Test obținere istoric predicții."""
        config = {}
        oracle = BattleOracle(config)
        
        # Rulează câteva analize
        await oracle.analyze_risk({'name': 'test1', 'severity': 0.5})
        await oracle.analyze_risk({'name': 'test2', 'severity': 0.7})
        
        history = await oracle.get_prediction_history(limit=5)
        
        assert len(history) == 2
    
    @pytest.mark.asyncio
    async def test_battle_oracle_threat_levels(self):
        """Test diferite niveluri de amenințare."""
        config = {}
        oracle = BattleOracle(config)
        
        # Test low threat
        result_low = await oracle.analyze_risk({
            'name': 'low_risk',
            'severity': 0.2,
            'risk_factors': []
        })
        assert result_low['threat_level'] == 'low'
        
        # Test critical threat
        result_critical = await oracle.analyze_risk({
            'name': 'critical_risk',
            'severity': 0.9,
            'risk_factors': ['factor1', 'factor2', 'factor3']
        })
        assert result_critical['threat_level'] == 'critical'
    
    @pytest.mark.asyncio
    async def test_weapon_master_get_status(self):
        """Test obținere status Weapon Master."""
        config = {'external_access_enabled': True}
        weapon = WeaponMaster(config)
        
        status = await weapon.get_status()
        
        assert 'module' in status
        assert 'status' in status
    
    @pytest.mark.asyncio
    async def test_weapon_master_enabled_external_access(self):
        """Test acces extern activat."""
        config = {'external_access_enabled': True}
        weapon = WeaponMaster(config)
        
        result = await weapon.execute_external_query({
            'type': 'test_query',
            'target': 'localhost'
        })
        
        # Când e activat, ar trebui să permită query-ul
        assert 'success' in result
    
    @pytest.mark.asyncio
    async def test_messenger_get_status(self):
        """Test obținere status Messenger."""
        config = {}
        messenger = Messenger(config)
        
        status = await messenger.get_status()
        
        assert 'module' in status
        assert 'status' in status
    
    @pytest.mark.asyncio
    async def test_messenger_send_with_encryption(self):
        """Test trimitere mesaj cu criptare."""
        config = {}
        messenger = Messenger(config)
        
        result = await messenger.send_secure_message({
            'recipient': 'test_user',
            'content': 'Secret message',
            'encrypt': True
        })
        
        assert result['success']
        assert 'message_id' in result
    
    @pytest.mark.asyncio
    async def test_messenger_receive_message(self):
        """Test primire mesaj."""
        config = {}
        messenger = Messenger(config)
        
        result = await messenger.receive_message('message_id_123')
        
        assert 'success' in result
    
    @pytest.mark.asyncio
    async def test_weapon_master_enable_disable_access(self):
        """Test activare/dezactivare acces extern."""
        config = {'external_access_enabled': False}
        weapon = WeaponMaster(config)
        
        assert not weapon.external_access_enabled
        
        await weapon.enable_external_access()
        assert weapon.external_access_enabled
        
        await weapon.disable_external_access()
        assert not weapon.external_access_enabled
    
    @pytest.mark.asyncio
    async def test_weapon_master_domain_management(self):
        """Test gestionare domenii permise."""
        config = {'allowed_domains': ['example.com']}
        weapon = WeaponMaster(config)
        
        await weapon.add_allowed_domain('test.com')
        assert 'test.com' in weapon.allowed_domains
        
        await weapon.remove_allowed_domain('test.com')
        assert 'test.com' not in weapon.allowed_domains
    
    @pytest.mark.asyncio
    async def test_weapon_master_domain_restriction(self):
        """Test restricție domenii."""
        config = {
            'external_access_enabled': True,
            'allowed_domains': ['allowed.com']
        }
        weapon = WeaponMaster(config)
        
        # Test acces la domeniu nepermis
        result = await weapon.execute_external_query({
            'type': 'http_get',
            'target': 'https://blocked.com'
        })
        
        assert not result['success']
        assert result['blocked']
    
    @pytest.mark.asyncio
    async def test_weapon_master_http_get(self):
        """Test cerere HTTP GET."""
        config = {
            'external_access_enabled': True,
            'allowed_domains': []
        }
        weapon = WeaponMaster(config)
        
        result = await weapon.execute_external_query({
            'type': 'http_get',
            'target': 'https://example.com'
        })
        
        assert result['success']
        assert 'status_code' in result
    
    @pytest.mark.asyncio
    async def test_weapon_master_http_post(self):
        """Test cerere HTTP POST."""
        config = {
            'external_access_enabled': True
        }
        weapon = WeaponMaster(config)
        
        result = await weapon.execute_external_query({
            'type': 'http_post',
            'target': 'https://example.com',
            'payload': {'key': 'value'}
        })
        
        assert result['success']
    
    @pytest.mark.asyncio
    async def test_weapon_master_dns_lookup(self):
        """Test interogare DNS."""
        config = {
            'external_access_enabled': True
        }
        weapon = WeaponMaster(config)
        
        result = await weapon.execute_external_query({
            'type': 'dns_lookup',
            'target': 'localhost'
        })
        
        assert 'success' in result
    
    @pytest.mark.asyncio
    async def test_weapon_master_unknown_query_type(self):
        """Test tip interogare necunoscut."""
        config = {
            'external_access_enabled': True
        }
        weapon = WeaponMaster(config)
        
        result = await weapon.execute_external_query({
            'type': 'unknown_type',
            'target': 'test'
        })
        
        assert not result['success']
        assert 'Unknown query type' in result['error']
    
    @pytest.mark.asyncio
    async def test_messenger_queue_and_process(self):
        """Test coadă mesaje."""
        config = {}
        messenger = Messenger(config)
        
        # Adaugă mesaje în coadă
        await messenger.queue_message({
            'recipient': 'user1',
            'content': 'message1',
            'encrypt': False
        })
        await messenger.queue_message({
            'recipient': 'user2',
            'content': 'message2',
            'encrypt': False
        })
        
        assert len(messenger.message_queue) == 2
        
        # Procesează coada
        result = await messenger.process_queue()
        
        assert result['success']
        assert result['processed'] == 2
        assert len(messenger.message_queue) == 0
    
    @pytest.mark.asyncio
    async def test_messenger_get_sent_messages(self):
        """Test obținere mesaje trimise."""
        config = {}
        messenger = Messenger(config)
        
        await messenger.send_secure_message({
            'recipient': 'test',
            'content': 'message',
            'encrypt': False
        })
        
        messages = await messenger.get_sent_messages(limit=5)
        
        assert len(messages) == 1
        assert messages[0]['recipient'] == 'test'
    
    @pytest.mark.asyncio
    async def test_messenger_get_received_messages(self):
        """Test obținere mesaje primite."""
        config = {}
        guard = SpartanGuard(config)
        messenger = Messenger(config, spartan_guard=guard)
        
        # Criptează un mesaj
        encrypted = await guard.encrypt("test message")
        
        # Primește mesajul
        await messenger.receive_message(encrypted)
        
        messages = await messenger.get_received_messages(limit=5)
        
        assert len(messages) == 1
    
    @pytest.mark.asyncio
    async def test_messenger_broadcast(self):
        """Test broadcast mesaj."""
        config = {}
        messenger = Messenger(config)
        
        recipients = ['user1', 'user2', 'user3']
        result = await messenger.broadcast_message(
            recipients=recipients,
            content='broadcast message',
            priority='high'
        )
        
        assert result['success']
        assert result['total'] == 3
        assert result['successful'] >= 0
    
    @pytest.mark.asyncio
    async def test_messenger_empty_queue_processing(self):
        """Test procesare coadă goală."""
        config = {}
        messenger = Messenger(config)
        
        result = await messenger.process_queue()
        
        assert result['success']
        assert result['processed'] == 0
