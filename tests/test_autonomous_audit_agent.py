"""
Tests for the Autonomous Audit Agent documentation guard.

The agent's completion metric is a file-length heuristic (BACKLOG B-01), so it
must never overwrite documents that hold verified, hand-maintained status.
"""

from autonomous_audit_agent import (
    AUTHORITATIVE_MARKER,
    AutonomousAuditAgent,
    FeatureStatus,
)


def _agent(repo, **kwargs) -> AutonomousAuditAgent:
    agent = AutonomousAuditAgent(str(repo), **kwargs)
    agent.scan_results['overall'] = {'total_components': 10, 'implemented': 7, 'percentage': 70.0}
    agent.scan_results['categories'] = {
        'Core System': FeatureStatus('Core System', 3, 3, 0, 0, 100.0),
    }
    return agent


def _readme(repo, body: str):
    path = repo / 'README.md'
    path.write_text(body, encoding='utf-8')
    return path


def test_authoritative_readme_is_not_overwritten(tmp_path):
    original = f"# Title\n\n## Implementation Status\n\n{AUTHORITATIVE_MARKER}\nVerified.\n"
    path = _readme(tmp_path, original)

    _agent(tmp_path)._update_readme()

    assert path.read_text(encoding='utf-8') == original


def test_force_doc_update_overrides_guard(tmp_path):
    path = _readme(tmp_path, f"# Title\n\n## Implementation Status\n\n{AUTHORITATIVE_MARKER}\nVerified.\n")

    _agent(tmp_path, force_doc_update=True)._update_readme()

    content = path.read_text(encoding='utf-8')
    assert "**Overall Progress:** 70.0% (7/10 components)" in content
    assert "Verified." not in content


def test_unmarked_readme_is_updated(tmp_path):
    path = _readme(tmp_path, "# Title\n\n## Implementation Status\n\nold\n\n## Next\n\nkept\n")

    _agent(tmp_path)._update_readme()

    content = path.read_text(encoding='utf-8')
    assert "**Overall Progress:** 70.0%" in content
    assert "## Next\n\nkept" in content
    assert "\nold\n" not in content


def test_authoritative_master_plan_is_not_overwritten(tmp_path):
    original = f"# Plan\n\n{AUTHORITATIVE_MARKER}\n"
    path = tmp_path / 'TEMPORAL_COMPRESSION_MASTER_PLAN.md'
    path.write_text(original, encoding='utf-8')

    _agent(tmp_path)._update_master_plan()

    assert path.read_text(encoding='utf-8') == original


def test_repository_docs_carry_the_marker():
    """The real README and master plan are protected from the heuristic."""
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    for name in ('README.md', 'TEMPORAL_COMPRESSION_MASTER_PLAN.md'):
        assert AUTHORITATIVE_MARKER in (root / name).read_text(encoding='utf-8'), name
