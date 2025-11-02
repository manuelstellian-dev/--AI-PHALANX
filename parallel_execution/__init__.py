"""
Parallel Execution Module for ΛΕΩΝΙΔΑΣ-AI PHALANX
Modul pentru execuție paralelă reală folosind ProcessPoolExecutor
"""

from .phalanx_executor import PhalanxExecutor, PhalanxConfig
from .task_scheduler import TaskScheduler, DependencyGraph, Task

__all__ = [
    'PhalanxExecutor',
    'PhalanxConfig',
    'TaskScheduler',
    'DependencyGraph',
    'Task'
]
