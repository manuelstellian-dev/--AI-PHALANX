"""
Regression tests for the system-integrity remediation.

Each test pins a defect found during the forensic audit so it cannot
silently return: configuration wiring, authentication, key loading,
Thermopylae safety, air-gap/allowlist checks, metrics format, Λ-TAS
interconnection, Amdahl bound, and the SPARTA runtime/API.
"""

import os
import tempfile

import pytest
import yaml
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from httpx import AsyncClient

import api.server as server
from api.server import (
    DEFAULT_AUTH_TOKEN,
    REPO_ROOT,
    app,
    get_expected_token,
    get_section,
    initialize_system,
    load_master_key_hex,
    verify_token,
)
from control.kronos_arbiter import KronosArbiter
from core.commandprocessor import CommandProcessor
from core.leonidasbrain import LeondasBrain
from hoplites.shieldbearer import ShieldBearer
from hoplites.weaponmaster import WeaponMaster
from phalanx.helot import HelotModule
from phalanx.thermopylae import ThermopylaeModule
from sparta import SemanticFoundation, get_runtime


def _settings() -> dict:
    with open(os.path.join(REPO_ROOT, 'config', 'settings.yaml'), encoding='utf-8') as f:
        return yaml.safe_load(f)


# ============================================================================
# Configuration wiring
# ============================================================================

class TestConfigWiring:
    """Modules must receive their own settings.yaml section."""

    def test_get_section_nested(self):
        cfg = {'phalanx': {'helot': {'x': 1}}}
        assert get_section(cfg, 'phalanx', 'helot') == {'x': 1}

    def test_get_section_falls_back_to_flat_config(self):
        cfg = {'survival_threshold': 0.5}
        assert get_section(cfg, 'phalanx', 'thermopylae') is cfg

    @pytest.mark.asyncio
    async def test_settings_sections_reach_modules(self):
        cfg = _settings()
        cfg['phalanx']['thermopylae']['survival_threshold'] = 0.42
        cfg['phalanx']['helot']['resource_thresholds']['cpu_critical'] = 12.5
        cfg['hoplites']['shield_bearer']['airgap_mode'] = 'permissive'
        cfg['hoplites']['weapon_master']['allowed_domains'] = ['example.com']

        brain, processor = await initialize_system(cfg)
        try:
            phalanx = brain.modules['phalanx']
            hoplites = brain.modules['hoplites']
            assert phalanx['thermopylae'].critical_threshold == 0.42
            assert phalanx['thermopylae'].consecutive_breaches_required == 3
            assert phalanx['helot'].resource_thresholds['cpu_critical'] == 12.5
            assert hoplites['shield'].airgap_mode == 'permissive'
            assert hoplites['weapon'].allowed_domains == ['example.com']
            # Λ-Core is connected to the CommandProcessor (factor U)
            assert brain.command_processor is processor
            # SPARTA is available to the CommandProcessor
            assert 'sparta' in processor.modules
        finally:
            await phalanx['krypteia'].stop_monitoring()
            await brain.shutdown()


# ============================================================================
# Authentication
# ============================================================================

class TestAuthentication:
    """Token resolution and verification."""

    def test_token_priority(self, monkeypatch):
        monkeypatch.delenv('SPARTA_AUTH_TOKEN', raising=False)
        assert get_expected_token({}) == DEFAULT_AUTH_TOKEN
        assert get_expected_token({'auth_token': 'root'}) == 'root'
        assert get_expected_token({'auth': {'auth_token': 'nested'}, 'auth_token': 'root'}) == 'nested'
        monkeypatch.setenv('SPARTA_AUTH_TOKEN', 'env')
        assert get_expected_token({'auth': {'auth_token': 'nested'}}) == 'env'

    def test_settings_yaml_token_is_honoured(self, monkeypatch):
        monkeypatch.delenv('SPARTA_AUTH_TOKEN', raising=False)
        monkeypatch.setattr(server, 'config', {'auth': {'auth_token': 'from-yaml'}})

        ok = HTTPAuthorizationCredentials(scheme='Bearer', credentials='from-yaml')
        assert verify_token(ok) == 'from-yaml'

        bad = HTTPAuthorizationCredentials(scheme='Bearer', credentials=DEFAULT_AUTH_TOKEN)
        with pytest.raises(HTTPException) as exc_info:
            verify_token(bad)
        assert exc_info.value.status_code == 401


# ============================================================================
# Master key loading (spartan_keys.yaml)
# ============================================================================

class TestMasterKeyLoading:
    """generate_keys.py output must actually be consumed."""

    def _cfg(self, base):
        return {'phalanx': {'thermopylae': {'base_path': base, 'keys_path': '/keys.yaml'}}}

    def test_loads_generated_key(self):
        key_hex = 'ab' * 32
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, 'keys.yaml'), 'w') as f:
                yaml.safe_dump({'MASTER_AES_KEY_HEX': key_hex}, f)
            assert load_master_key_hex(self._cfg(tmp)) == key_hex

    def test_ignores_template_placeholder_and_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            assert load_master_key_hex(self._cfg(tmp)) is None
            with open(os.path.join(tmp, 'keys.yaml'), 'w') as f:
                yaml.safe_dump({'MASTER_AES_KEY_HEX': 'REPLACE_WITH_GENERATED_KEY'}, f)
            assert load_master_key_hex(self._cfg(tmp)) is None

    @pytest.mark.asyncio
    async def test_spartan_guard_uses_master_key(self):
        key_hex = 'cd' * 32
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, 'keys.yaml'), 'w') as f:
                yaml.safe_dump({'MASTER_AES_KEY_HEX': key_hex}, f)
            cfg = self._cfg(tmp)
            cfg['hardware'] = {'cpu_cores': 2}

            brain, _ = await initialize_system(cfg)
            try:
                guard = brain.modules['hoplites']['guard']
                assert guard.master_key == bytes.fromhex(key_hex)
            finally:
                await brain.modules['phalanx']['krypteia'].stop_monitoring()
                await brain.shutdown()


# ============================================================================
# Thermopylae safety
# ============================================================================

class TestThermopylaeSafety:
    """Destruction requires a sustained breach and targets the real paths."""

    @pytest.mark.asyncio
    async def test_requires_consecutive_breaches(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = ThermopylaeModule({
                'thermopylae_armed': True,
                'consecutive_breaches_required': 3,
                'base_path': tmp,
            })
            await t.check_emergency_protocol(0.90)
            await t.check_emergency_protocol(0.90)
            assert not t.protocol_activated
            await t.check_emergency_protocol(0.90)
            assert t.protocol_activated

    @pytest.mark.asyncio
    async def test_recovery_resets_breach_counter(self):
        t = ThermopylaeModule({'thermopylae_armed': True, 'consecutive_breaches_required': 2})
        await t.check_emergency_protocol(0.90)
        await t.check_emergency_protocol(0.99)
        assert t.consecutive_breaches == 0
        await t.check_emergency_protocol(0.90)
        assert not t.protocol_activated

    def test_default_base_path_is_repo_root(self):
        assert ThermopylaeModule({})._base_path() == REPO_ROOT
        assert ThermopylaeModule({'base_path': ''})._base_path() == REPO_ROOT

    @pytest.mark.asyncio
    async def test_destroys_every_configured_vault_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('vault', 'encrypted_vault'):
                os.makedirs(os.path.join(tmp, 'data', name))
            t = ThermopylaeModule({
                'base_path': tmp,
                'vault_path': ['/data/vault', '/data/encrypted_vault'],
            })
            await t._destroy_encrypted_vault()
            assert not os.path.exists(os.path.join(tmp, 'data', 'vault'))
            assert not os.path.exists(os.path.join(tmp, 'data', 'encrypted_vault'))

    def test_thermopylae_targets_the_vault_storage(self):
        cfg = _settings()
        vault_dir = '/' + cfg['vault']['storage_path'].strip('/')
        assert vault_dir in cfg['phalanx']['thermopylae']['vault_path']


# ============================================================================
# Hoplites: air-gap and allowlist
# ============================================================================

class TestShieldBearerAirGap:
    """Loopback traffic is not a violation; permissive allowlist works."""

    @pytest.mark.asyncio
    async def test_loopback_does_not_break_strict_airgap(self, monkeypatch):
        shield = ShieldBearer({'airgap_mode': 'strict'})

        async def connections():
            return [
                {'local': '127.0.0.1:7300', 'remote': '127.0.0.1:51000'},
                {'local': '[::1]:7300', 'remote': '::1:51001'},
                {'local': '0.0.0.0:7300', 'remote': None},
            ]
        monkeypatch.setattr(shield, '_check_network_connections', connections)
        assert await shield.check_airgap() is True

    @pytest.mark.asyncio
    async def test_external_connection_breaks_strict_airgap(self, monkeypatch):
        shield = ShieldBearer({'airgap_mode': 'strict'})

        async def connections():
            return [{'local': '10.0.0.2:5000', 'remote': '8.8.8.8:53'}]
        monkeypatch.setattr(shield, '_check_network_connections', connections)
        assert await shield.check_airgap() is False

    @pytest.mark.asyncio
    async def test_permissive_allowlist_matches_strings(self, monkeypatch):
        shield = ShieldBearer({'airgap_mode': 'permissive',
                               'allowed_connections': ['10.1.1.1', '10.2.2.2:443']})

        async def allowed():
            return [{'local': 'a', 'remote': '10.1.1.1:22'},
                    {'local': 'b', 'remote': '10.2.2.2:443'}]
        monkeypatch.setattr(shield, '_check_network_connections', allowed)
        assert await shield.check_airgap() is True

        async def unknown():
            return [{'local': 'c', 'remote': '10.9.9.9:22'}]
        monkeypatch.setattr(shield, '_check_network_connections', unknown)
        assert await shield.check_airgap() is False


class TestWeaponMasterAllowlist:
    """Allowlist is exact-or-subdomain, never substring."""

    @pytest.mark.parametrize('target,allowed', [
        ('https://example.com/path', True),
        ('https://api.example.com', True),
        ('https://EXAMPLE.com:8443/x', True),
        ('example.com', True),
        ('https://evil-example.com', False),
        ('https://example.com.evil.io', False),
        ('https://notexample.com', False),
    ])
    def test_domain_matching(self, target, allowed):
        weapon = WeaponMaster({'external_access_enabled': True, 'allowed_domains': ['example.com']})
        assert weapon._is_domain_allowed(target) is allowed


# ============================================================================
# Metrics
# ============================================================================

class TestPrometheusMetrics:
    """/metrics must be Prometheus text, not a JSON-encoded string."""

    @pytest.mark.asyncio
    async def test_metrics_is_plain_text(self):
        headers = {'Authorization': f'Bearer {get_expected_token()}'}
        async with AsyncClient(app=app, base_url='http://test', headers=headers) as client:
            response = await client.get('/api/v1/metrics')
        assert response.status_code == 200
        assert response.headers['content-type'].startswith('text/plain')
        assert response.text.startswith('# HELP leonidas_survival_probability')
        assert response.text.endswith('\n')

    @pytest.mark.asyncio
    async def test_lifespan_sets_uptime_origin_and_runs_ffp(self):
        original = (server.leonidas_brain, server.command_processor, server.config)
        try:
            async with server.lifespan(app):
                assert isinstance(app.state.start_time, float)
                assert server.leonidas_brain.ffp is not None
            # FFP is stopped on shutdown
            assert server.leonidas_brain.ffp.running is False
        finally:
            server.leonidas_brain, server.command_processor, server.config = original


# ============================================================================
# Λ-Core interconnection
# ============================================================================

class TestLambdaTasInterconnection:
    """Λ-TAS uses Helot's measured P and the CommandProcessor's U."""

    @pytest.mark.asyncio
    async def test_helot_records_parallelism(self):
        helot = HelotModule({})
        resources = await helot.monitor_resources()
        assert helot.last_resources is resources
        assert resources['parallelism_factor'] >= 1.0

    def test_brain_uses_helot_p_and_processor_u(self):
        brain = LeondasBrain({'hardware': {'cpu_cores': 4}, 'current_workload': 0.5})
        # Without measurements: configuration fallbacks
        assert brain._current_parallelism() == 4
        assert brain._current_workload() == 0.5

        class MeasuredHelot:
            last_resources = {'parallelism_factor': 7.25}
        brain.modules['phalanx'] = {'helot': MeasuredHelot()}

        processor = CommandProcessor({})
        processor.active_tasks = 3
        brain.command_processor = processor

        assert brain._current_parallelism() == 7.25
        assert brain._current_workload() == processor.calculate_universe_expansion_factor()


# ============================================================================
# Kronos-Arbiter: Amdahl bound
# ============================================================================

class TestKronosAmdahlBound:
    """amdahl_fraction caps the achievable speedup."""

    def test_amdahl_fraction_caps_speedup(self):
        kronos = KronosArbiter(n_cores=8)
        bound = kronos.calculate_amdahl_aristeia(0.5, 8)
        metrics = kronos.calculate_metrikos(10.0, theta=1.0, lambda_balance=1.0,
                                            eta_overhead=1.0, amdahl_fraction=0.5)
        assert metrics.speedup == pytest.approx(bound)
        assert metrics.speedup < 8

    def test_full_parallel_fraction_unchanged(self):
        kronos = KronosArbiter(n_cores=4)
        metrics = kronos.calculate_metrikos(10.0)
        expected = 4 * kronos.default_theta * kronos.default_lambda * kronos.default_eta
        assert metrics.speedup == pytest.approx(expected)


# ============================================================================
# SPARTA runtime, API and command
# ============================================================================

class TestSpartaIntegration:
    """SPARTA is reachable from the API and the CommandProcessor."""

    def test_runtime_is_shared_and_loaded(self):
        runtime = get_runtime()
        assert runtime is get_runtime()
        assert len(runtime.foundation.concepts) == 420
        assert len(runtime.foundation.quarantined) == 80

    def test_known_query_is_grounded(self):
        result = get_runtime().query("What is energy conservation?")
        assert 'energy_conservation' in result['sources']
        assert result['confidence'] >= 0.95
        assert result['epistemic_status']['status'] in ('KNOWN', 'PARTIAL')

    def test_dangling_reference_report(self):
        foundation = SemanticFoundation()
        base = {k: '' for k in ('subdomain', 'topic', 'definition', 'formal_statement',
                                'source', 'reflex_tag', 'verification', 'uncertainty')}
        base.update({'domain': 'Test', 'confidence': 0.9, 'examples': [],
                     'counterexamples': [], 'applications': []})
        foundation.add_concept({**base, 'id': 'a', 'relations': ['b', 'ghost'], 'prerequisites': ['phantom']})
        foundation.add_concept({**base, 'id': 'b', 'relations': ['a'], 'prerequisites': []})

        assert foundation.find_dangling_references() == {
            'a': {'relations': ['ghost'], 'prerequisites': ['phantom']}
        }
        report = foundation.get_integrity_report()
        assert report['dangling_reference_count'] == 2
        assert report['healthy'] is False

    def test_placeholders_never_answer_as_verified(self):
        """Template placeholders must not be served as [VERIFIED] knowledge."""
        runtime = get_runtime()
        for query in ('epistemic concept concerning knowledge justification belief',
                      'mode of knowledge epistemological approach',
                      'universal principle applicable across domains and contexts'):
            result = runtime.query(query)
            assert not any(s in runtime.foundation.quarantined for s in result['sources']), query
            assert 'Epistemic Concept 1' not in result['response']
    
    def test_placeholder_detection_rules(self):
        foundation = SemanticFoundation()
        base = {k: '' for k in ('subdomain', 'topic', 'formal_statement', 'source', 'reflex_tag',
                                'verification', 'uncertainty')}
        base.update({'domain': 'Test', 'confidence': 0.9, 'examples': [], 'counterexamples': [],
                     'applications': [], 'relations': [], 'prerequisites': []})
        for i in range(1, 4):
            foundation.add_concept({**base, 'id': f'filler_{i:02d}', 'definition': f'Filler concept {i} about things'})
        # Two numbered concepts with distinct definitions are real knowledge
        foundation.add_concept({**base, 'id': 'law_01', 'definition': 'First law of motion'})
        foundation.add_concept({**base, 'id': 'law_02', 'definition': 'Second law: F = m a'})
        
        assert foundation.find_placeholder_concepts() == ['filler_01', 'filler_02', 'filler_03']
        assert foundation.quarantine_placeholder_concepts() == 3
        assert set(foundation.concepts) == {'law_01', 'law_02'}
        assert foundation.get_integrity_report()['quarantined_placeholders'] == 3
    
    @pytest.mark.asyncio
    async def test_sparta_api_requires_auth(self):
        async with AsyncClient(app=app, base_url='http://test') as client:
            response = await client.post('/api/v1/sparta/query', json={'query': 'entropy'})
        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_sparta_api_endpoints(self):
        headers = {'Authorization': f'Bearer {get_expected_token()}'}
        async with AsyncClient(app=app, base_url='http://test', headers=headers) as client:
            query = await client.post('/api/v1/sparta/query',
                                      json={'query': 'What is energy conservation?'})
            concept = await client.get('/api/v1/sparta/concept/entropy')
            missing = await client.get('/api/v1/sparta/concept/does_not_exist')
            stats = await client.get('/api/v1/sparta/stats')
            integrity = await client.get('/api/v1/sparta/integrity')
            empty = await client.post('/api/v1/sparta/query', json={'query': ''})

        assert query.status_code == 200
        assert 'energy_conservation' in query.json()['sources']
        assert concept.status_code == 200 and concept.json()['id'] == 'entropy'
        assert missing.status_code == 404
        assert stats.json()['total_concepts'] == 420
        assert 'dangling_reference_count' in integrity.json()
        assert empty.status_code == 422

    @pytest.mark.asyncio
    async def test_sparta_query_command(self):
        processor = CommandProcessor({'sparta': get_runtime()})
        ok = await processor.process_command({'type': 'sparta_query',
                                              'payload': {'query': 'What is entropy?'}})
        assert ok['success'] is True
        assert 'entropy' in ok['result']['sources']

        missing_query = await processor.process_command({'type': 'sparta_query', 'payload': {}})
        assert missing_query['success'] is False

        unavailable = await CommandProcessor({}).process_command(
            {'type': 'sparta_query', 'payload': {'query': 'x'}})
        assert unavailable['success'] is False
