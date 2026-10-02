"""
Mnemosyne Measures - facts recomputed from the repository.

CURRENT_STATE.md declares facts as `- **measure:** name = value`. The
validator recomputes each one here; a mismatch is a synchronization error,
so the memory can never silently drift away from the code.

Measures are cheap and deterministic (no test run, no model training).
"""

import ast
import glob
import json
import os
import re
import subprocess
from functools import lru_cache
from typing import Callable, Dict, List

from mnemosyne.graph import REPO_ROOT


@lru_cache(maxsize=4)
def tracked_files(root: str = REPO_ROOT) -> tuple:
    """Repository files: git-tracked plus new untracked, minus ignored."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=root, capture_output=True, text=True, check=True,
        ).stdout
        files = [f for f in out.splitlines() if f and os.path.exists(os.path.join(root, f))]
    except (OSError, subprocess.CalledProcessError):
        files = []
        for base, dirs, names in os.walk(root):
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'models', 'data', 'logs'}]
            files += [os.path.relpath(os.path.join(base, n), root) for n in names]
    return tuple(sorted(set(files)))


def _sparta_foundation(root: str):
    from sparta.semantic_foundation import SemanticFoundation
    foundation = SemanticFoundation()
    foundation.load_memory(os.path.join(root, 'sparta', 'semantic_memory.jsonl'))
    return foundation


def _concepts_on_disk(root: str) -> int:
    with open(os.path.join(root, 'sparta', 'semantic_memory.jsonl'), encoding='utf-8') as f:
        return sum(1 for line in f if line.strip())


def _test_functions(root: str) -> int:
    count = 0
    for path in glob.glob(os.path.join(root, 'tests', 'test_*.py')):
        with open(path, encoding='utf-8') as f:
            tree = ast.parse(f.read())
        count += sum(1 for node in ast.walk(tree)
                     if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                     and node.name.startswith('test_'))
    return count


def _api_routes(root: str) -> int:
    count = 0
    for path in glob.glob(os.path.join(root, 'api', '**', '*.py'), recursive=True):
        with open(path, encoding='utf-8') as f:
            count += len(re.findall(r'^@(?:router|app)\.(?:get|post|put|delete|patch)\(', f.read(), re.M))
    return count


def _count_ext(root: str, ext: str) -> int:
    return sum(1 for f in tracked_files(root) if f.endswith(ext))


def _settings_leaf_keys(root: str) -> int:
    import yaml
    with open(os.path.join(root, 'config', 'settings.yaml'), encoding='utf-8') as f:
        cfg = yaml.safe_load(f)

    def leaves(d):
        return sum(leaves(v) if isinstance(v, dict) else 1 for v in d.values())
    return leaves(cfg)


def _packages(root: str) -> str:
    pkgs = sorted(os.path.dirname(p) for p in glob.glob(os.path.join(root, '*', '__init__.py'))
                  if not os.path.basename(os.path.dirname(p)).startswith(('tests', '.')))
    return ",".join(os.path.basename(p) for p in pkgs)


def _requirement_names(root: str) -> List[str]:
    names = []
    with open(os.path.join(root, 'requirements.txt'), encoding='utf-8') as f:
        for line in f:
            line = line.split('#')[0].strip()
            if line:
                names.append(re.split(r'[<>=\[ ]', line)[0].lower())
    return names


MEASURES: Dict[str, Callable[[str], object]] = {
    "sparta.concepts_on_disk": _concepts_on_disk,
    "sparta.concepts_active": lambda r: len(_sparta_foundation(r).concepts),
    "sparta.concepts_quarantined": lambda r: len(_sparta_foundation(r).quarantined),
    "sparta.domains_active": lambda r: len(_sparta_foundation(r).domains),
    "sparta.dangling_references": lambda r: _sparta_foundation(r).get_integrity_report()['dangling_reference_count'],
    "api.routes": _api_routes,
    "tests.functions": _test_functions,
    "tests.modules": lambda r: len(glob.glob(os.path.join(r, 'tests', 'test_*.py'))),
    "repo.files": lambda r: len(tracked_files(r)),
    "repo.python_files": lambda r: _count_ext(r, '.py'),
    "repo.markdown_files": lambda r: _count_ext(r, '.md'),
    "repo.shell_scripts": lambda r: _count_ext(r, '.sh'),
    "repo.packages": _packages,
    "config.settings_leaf_keys": _settings_leaf_keys,
    "deps.external_ml_runtime": lambda r: ",".join(
        n for n in _requirement_names(r) if n in {"torch", "sentence-transformers", "transformers",
                                                  "tensorflow", "openai", "anthropic"}) or "none",
    "deps.requirements": lambda r: len(_requirement_names(r)),
}


def measure(name: str, root: str = REPO_ROOT) -> str:
    """
    Compute a named fact.

    Args:
        name: Measure name (see MEASURES)
        root: Repository root

    Returns:
        Value rendered as text (for comparison with the declared value)

    Raises:
        KeyError: Unknown measure
    """
    value = MEASURES[name](root)
    return json.dumps(value) if isinstance(value, (list, dict)) else str(value)
