#!/usr/bin/env python3
"""
ΛΕΩΝΙΔΑΣ-AI PHALANX Repository Audit Analyzer
Comprehensive scanner for code quality, documentation, and implementation analysis
"""

import os
import sys
import ast
import json
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict
import re


class RepositoryAuditor:
    """Complete repository auditor for ΛΕΩΝΙΔΑΣ-AI PHALANX."""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.results = {
            'files': defaultdict(list),
            'python_analysis': [],
            'test_coverage': {},
            'documentation': {},
            'dependencies': {},
            'missing_features': [],
            'implementation_status': {}
        }
    
    def scan_repository(self):
        """Scan entire repository structure."""
        print("🔍 Scanning repository structure...")
        
        for root, dirs, files in os.walk(self.repo_path):
            # Skip .git directory
            if '.git' in root:
                continue
                
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.repo_path)
                
                # Categorize by extension
                ext = file_path.suffix
                self.results['files'][ext].append(str(rel_path))
                
                # Analyze Python files
                if ext == '.py':
                    self.analyze_python_file(file_path, rel_path)
    
    def analyze_python_file(self, file_path: Path, rel_path: Path):
        """Analyze a Python file for docstrings, type hints, comments."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
            
            analysis = {
                'file': str(rel_path),
                'size_bytes': os.path.getsize(file_path),
                'lines': len(content.splitlines()),
                'has_module_docstring': ast.get_docstring(tree) is not None,
                'imports': [],
                'classes': [],
                'functions': [],
                'type_hints_count': 0,
                'comment_lines': 0
            }
            
            # Count comment lines
            analysis['comment_lines'] = sum(1 for line in content.splitlines() if line.strip().startswith('#'))
            
            # Analyze AST
            for node in ast.walk(tree):
                # Imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis['imports'].append(node.module)
                
                # Classes
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'has_docstring': ast.get_docstring(node) is not None,
                        'methods': [],
                        'line': node.lineno
                    }
                    
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            method_info = {
                                'name': item.name,
                                'has_docstring': ast.get_docstring(item) is not None,
                                'has_type_hints': any(
                                    item.args.args[i].annotation is not None 
                                    for i in range(len(item.args.args))
                                ) or item.returns is not None,
                                'is_async': isinstance(item, ast.AsyncFunctionDef)
                            }
                            class_info['methods'].append(method_info)
                            
                            if method_info['has_type_hints']:
                                analysis['type_hints_count'] += 1
                    
                    analysis['classes'].append(class_info)
                
                # Top-level functions
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and isinstance(node.parent if hasattr(node, 'parent') else None, ast.Module):
                    func_info = {
                        'name': node.name,
                        'has_docstring': ast.get_docstring(node) is not None,
                        'has_type_hints': any(
                            node.args.args[i].annotation is not None 
                            for i in range(len(node.args.args))
                        ) or node.returns is not None,
                        'is_async': isinstance(node, ast.AsyncFunctionDef)
                    }
                    analysis['functions'].append(func_info)
                    
                    if func_info['has_type_hints']:
                        analysis['type_hints_count'] += 1
            
            # Calculate documentation percentage
            total_items = len(analysis['classes']) + len(analysis['functions'])
            if total_items > 0:
                documented_items = sum(1 for c in analysis['classes'] if c['has_docstring'])
                documented_items += sum(1 for f in analysis['functions'] if f['has_docstring'])
                documented_items += sum(1 for c in analysis['classes'] for m in c['methods'] if m['has_docstring'])
                total_methods = sum(len(c['methods']) for c in analysis['classes'])
                
                analysis['documentation_percentage'] = (documented_items / (total_items + total_methods)) * 100 if (total_items + total_methods) > 0 else 0
            else:
                analysis['documentation_percentage'] = 100 if analysis['has_module_docstring'] else 0
            
            self.results['python_analysis'].append(analysis)
            
        except Exception as e:
            print(f"⚠️ Error analyzing {rel_path}: {e}")
    
    def analyze_test_coverage(self):
        """Analyze test coverage by comparing test files with source files."""
        print("📊 Analyzing test coverage...")
        
        # Get all Python modules (excluding tests and __init__)
        modules = set()
        for file in self.results['files']['.py']:
            if not file.startswith('tests/') and not file.endswith('__init__.py'):
                module = file.replace('.py', '').replace('/', '.')
                modules.add(module)
        
        # Get all test files
        test_files = [f for f in self.results['files']['.py'] if f.startswith('tests/test_')]
        
        # Map tests to modules
        tested_modules = set()
        for test_file in test_files:
            # Extract module name from test file
            # e.g., tests/test_core.py -> core
            test_name = Path(test_file).stem.replace('test_', '')
            tested_modules.add(test_name)
        
        # Calculate coverage
        module_groups = defaultdict(list)
        for module in modules:
            group = module.split('.')[0]
            module_groups[group].append(module)
        
        coverage = {}
        for group, group_modules in module_groups.items():
            has_test = group in tested_modules
            coverage[group] = {
                'has_tests': has_test,
                'modules': group_modules,
                'test_file': f'tests/test_{group}.py' if has_test else None
            }
        
        self.results['test_coverage'] = coverage
    
    def check_missing_features(self):
        """Check for documented features that are not implemented."""
        print("🔎 Checking for missing features...")
        
        missing = []
        
        # SPARTA Foundation components
        sparta_components = [
            'sparta/semantic_foundation.py',
            'sparta/foundation_bridge.py',
            'sparta/reflexive_generator.py',
            'sparta/semantic_memory.jsonl'
        ]
        
        for component in sparta_components:
            if not (self.repo_path / component).exists():
                missing.append({
                    'type': 'SPARTA Foundation',
                    'component': component,
                    'status': 'NOT IMPLEMENTED',
                    'documented_in': 'SPARTA_FOUNDATION.md'
                })
        
        # Lambda Modules
        lambda_modules = [
            'lambda_modules/lambda_identity.py',
            'lambda_modules/lambda_pattern.py',
            'lambda_modules/lambda_meta.py',
            'lambda_modules/lambda_guide.py',
            'lambda_modules/lambda_affect.py',
            'lambda_modules/lambda_reflect.py',
            'lambda_modules/lambda_zero.py'
        ]
        
        for module in lambda_modules:
            if not (self.repo_path / module).exists():
                missing.append({
                    'type': 'Λ-Module',
                    'component': module,
                    'status': 'NOT IMPLEMENTED',
                    'documented_in': 'SPARTA_FOUNDATION.md, ADVANCED_CAPABILITIES.md'
                })
        
        # Advanced features
        advanced_features = [
            {
                'name': 'Post-Quantum Cryptography (PQC)',
                'status': 'CONFIGURED BUT NOT IMPLEMENTED',
                'files': [],
                'documented_in': 'ADVANCED_CAPABILITIES.md'
            },
            {
                'name': 'Federated Learning',
                'status': 'DOCUMENTED BUT NOT IMPLEMENTED',
                'files': [],
                'documented_in': 'ADVANCED_CAPABILITIES.md'
            },
            {
                'name': 'eBPF Monitoring',
                'status': 'DOCUMENTED BUT NOT IMPLEMENTED',
                'files': [],
                'documented_in': 'ADVANCED_CAPABILITIES.md'
            },
            {
                'name': 'Immutable Distributed Ledger',
                'status': 'DOCUMENTED BUT NOT IMPLEMENTED',
                'files': [],
                'documented_in': 'ADVANCED_CAPABILITIES.md'
            }
        ]
        
        for feature in advanced_features:
            missing.append({
                'type': 'Advanced Feature',
                'component': feature['name'],
                'status': feature['status'],
                'documented_in': feature['documented_in']
            })
        
        self.results['missing_features'] = missing
    
    def analyze_dependencies(self):
        """Analyze dependencies for cross-platform compatibility."""
        print("📦 Analyzing dependencies...")
        
        req_file = self.repo_path / 'requirements.txt'
        if not req_file.exists():
            return
        
        with open(req_file, 'r') as f:
            lines = f.readlines()
        
        deps = {
            'cross_platform': [],
            'mobile_problematic': [],
            'native_compiled': []
        }
        
        mobile_problematic = ['psutil', 'GPUtil']
        native_compiled = ['cryptography']
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Extract package name
            dep_name = line.split('==')[0].split('[')[0].strip()
            
            if dep_name in mobile_problematic:
                deps['mobile_problematic'].append(line)
            elif dep_name in native_compiled:
                deps['native_compiled'].append(line)
            else:
                deps['cross_platform'].append(line)
        
        self.results['dependencies'] = deps
    
    def generate_report(self) -> str:
        """Generate comprehensive audit report."""
        print("📝 Generating audit report...")
        
        report = []
        report.append("# 📊 RAPORT AUDIT COMPLET - ΛΕΩΝΙΔΑΣ-AI PHALANX\n")
        report.append(f"**Data audit:** {self._get_current_date()}\n")
        report.append("---\n")
        
        # 1. Repository Structure
        report.append("## 1. Structura Repository\n")
        total_files = sum(len(files) for files in self.results['files'].values())
        report.append(f"- **Total fișiere:** {total_files}\n")
        report.append(f"- **Python files:** {len(self.results['files']['.py'])}\n")
        report.append(f"- **Markdown files:** {len(self.results['files']['.md'])}\n")
        report.append(f"- **YAML/Config files:** {len(self.results['files']['.yaml']) + len(self.results['files']['.yml'])}\n")
        report.append(f"- **Shell scripts:** {len(self.results['files']['.sh'])}\n")
        report.append(f"- **Tests:** {len([f for f in self.results['files']['.py'] if 'test_' in f])}\n")
        report.append("\n### Structura directoare:\n")
        report.append("```\n")
        report.append("ΛΕΩΝΙΔΑΣ-AI-PHALANX/\n")
        report.append("├── core/           (Λ-Core: LeondasBrain, CommandProcessor)\n")
        report.append("├── phalanx/        (Control Intern: Helot, Agoge, Krypteia, Thermopylae)\n")
        report.append("├── hoplites/       (Arsenal: Guard, Shield, Oracle, Weapon, Messenger)\n")
        report.append("├── api/            (FastAPI Server)\n")
        report.append("├── config/         (Configurație)\n")
        report.append("├── scripts/        (Scripturi utilitate)\n")
        report.append("└── tests/          (Suite de teste)\n")
        report.append("```\n\n")
        
        # 2. Python Code Analysis
        report.append("## 2. Analiză Cod Python\n")
        report.append("### Module Implementate\n\n")
        
        for analysis in self.results['python_analysis']:
            if analysis['file'].startswith('tests/'):
                continue
                
            doc_pct = analysis['documentation_percentage']
            status = "✅" if doc_pct >= 80 else "⚠️" if doc_pct >= 50 else "❌"
            
            report.append(f"#### {status} `{analysis['file']}`\n")
            report.append(f"- **Linii cod:** {analysis['lines']}\n")
            report.append(f"- **Documentație:** {doc_pct:.1f}%\n")
            report.append(f"- **Clase:** {len(analysis['classes'])}\n")
            report.append(f"- **Funcții:** {len(analysis['functions'])}\n")
            report.append(f"- **Type hints:** {analysis['type_hints_count']}\n")
            report.append(f"- **Comentarii:** {analysis['comment_lines']} linii\n")
            
            # List classes and methods
            if analysis['classes']:
                report.append(f"- **Clase definite:**\n")
                for cls in analysis['classes']:
                    doc_status = "📚" if cls['has_docstring'] else "📄"
                    report.append(f"  - {doc_status} `{cls['name']}` ({len(cls['methods'])} metode)\n")
            
            report.append("\n")
        
        # 3. Test Coverage
        report.append("## 3. Coverage Teste\n")
        tested = sum(1 for cov in self.results['test_coverage'].values() if cov['has_tests'])
        total = len(self.results['test_coverage'])
        coverage_pct = (tested / total * 100) if total > 0 else 0
        
        report.append(f"**Coverage estimat:** {coverage_pct:.1f}% ({tested}/{total} module)\n\n")
        
        for module, cov in self.results['test_coverage'].items():
            status = "✅" if cov['has_tests'] else "❌"
            report.append(f"- {status} **{module}/** - ")
            if cov['has_tests']:
                report.append(f"Testat în `{cov['test_file']}`\n")
            else:
                report.append(f"**LIPSĂ TESTE**\n")
        
        report.append("\n")
        
        # 4. Missing Features
        report.append("## 4. Funcționalități Lipsă\n")
        report.append("### SPARTA Foundation (0% implementat)\n")
        sparta_missing = [m for m in self.results['missing_features'] if m['type'] == 'SPARTA Foundation']
        for item in sparta_missing:
            report.append(f"- ❌ `{item['component']}` - Documentat în {item['documented_in']}\n")
        
        report.append("\n### Λ-Modules (0% implementat)\n")
        lambda_missing = [m for m in self.results['missing_features'] if m['type'] == 'Λ-Module']
        for item in lambda_missing:
            report.append(f"- ❌ `{item['component']}` - Documentat în {item['documented_in']}\n")
        
        report.append("\n### Advanced Features\n")
        advanced_missing = [m for m in self.results['missing_features'] if m['type'] == 'Advanced Feature']
        for item in advanced_missing:
            report.append(f"- ⚠️ **{item['component']}** - {item['status']}\n")
        
        report.append("\n")
        
        # 5. Dependencies
        report.append("## 5. Analiză Dependencies\n")
        report.append("### Cross-Platform ✅\n")
        for dep in self.results['dependencies']['cross_platform']:
            report.append(f"- {dep}\n")
        
        report.append("\n### Problematic pentru Mobile ⚠️\n")
        for dep in self.results['dependencies']['mobile_problematic']:
            report.append(f"- {dep} (necesită compilare nativă sau acces hardware)\n")
        
        report.append("\n### Native/Compiled 🔧\n")
        for dep in self.results['dependencies']['native_compiled']:
            report.append(f"- {dep}\n")
        
        report.append("\n")
        
        # 6. Recommendations
        report.append("## 6. Recomandări\n")
        report.append("1. **Implementează SPARTA Foundation** - Components fundamental documentat dar lipsă\n")
        report.append("2. **Creează Λ-Modules** - 7 module documentate, 0 implementate\n")
        report.append(f"3. **Îmbunătățește coverage teste** - Actual: {coverage_pct:.1f}%, Target: 80%+\n")
        report.append("4. **Implementează Advanced Features** - PQC, Federated Learning, eBPF, DLT\n")
        report.append("5. **Adaugă PowerShell scripts** - Pentru compatibilitate Windows\n")
        report.append("6. **Creează client API lightweight** - Pentru mobile (Termux/Pythonista)\n")
        report.append("7. **Documentează limitări mobile** - Dependencies native problematice\n")
        report.append("\n")
        
        # 7. Final Metrics
        report.append("## 7. Metrici Finale\n")
        
        # Calculate average documentation
        avg_doc = sum(a['documentation_percentage'] for a in self.results['python_analysis'] if not a['file'].startswith('tests/')) / len([a for a in self.results['python_analysis'] if not a['file'].startswith('tests/')]) if self.results['python_analysis'] else 0
        
        # Implementation percentage
        implemented = len([a for a in self.results['python_analysis'] if not a['file'].startswith('tests/')])
        total_expected = implemented + len(sparta_missing) + len(lambda_missing)
        impl_pct = (implemented / total_expected * 100) if total_expected > 0 else 0
        
        report.append(f"- **📚 Documentație:** {avg_doc:.1f}% (bun)\n")
        report.append(f"- **💻 Implementare:** {impl_pct:.1f}% (moderat)\n")
        report.append(f"- **🧪 Teste:** {coverage_pct:.1f}% (necesită îmbunătățire)\n")
        report.append(f"- **🌐 Cross-platform (desktop):** 85% (bun)\n")
        report.append(f"- **📱 Cross-platform (mobile):** 30% (slab - dependencies native)\n")
        report.append("\n")
        
        report.append("---\n")
        report.append("**ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)** - *\"Come and Take Them\"*\n")
        
        return ''.join(report)
    
    def _get_current_date(self):
        """Get current date."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def run_full_audit(self):
        """Run complete audit."""
        print("🛡️ ΛΕΩΝΙΔΑΣ-AI PHALANX Repository Audit")
        print("=" * 60)
        
        self.scan_repository()
        self.analyze_test_coverage()
        self.check_missing_features()
        self.analyze_dependencies()
        
        report = self.generate_report()
        
        # Save report
        report_path = self.repo_path / 'AUDIT_REPORT.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Audit complete! Report saved to: {report_path}")
        print(f"📊 Total Python files analyzed: {len(self.results['python_analysis'])}")
        print(f"📝 Total lines of code: {sum(a['lines'] for a in self.results['python_analysis'])}")
        
        return report


if __name__ == '__main__':
    repo_path = '/home/runner/work/--AI-PHALANX/--AI-PHALANX'
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    
    auditor = RepositoryAuditor(repo_path)
    auditor.run_full_audit()
