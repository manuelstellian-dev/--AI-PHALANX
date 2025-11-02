"""
TASK-SCHEDULER - Scheduler pentru Task-uri cu Dependențe
Implementează dependency graph cu topological sort pentru
determinarea ordinii optime de execuție a task-urilor paralele.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any, Callable
from collections import defaultdict, deque
from enum import Enum
from loguru import logger


class TaskStatus(str, Enum):
    """Statusuri posibile pentru un task."""
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """
    Reprezentare unui task cu dependențe.
    
    Attributes:
        task_id: Identificator unic pentru task
        func: Funcția de executat
        args: Argumente pentru funcție
        dependencies: Set de task_id-uri de care depinde acest task
        status: Statusul curent al task-ului
        result: Rezultatul execuției (sau None)
        priority: Prioritatea task-ului (mai mare = mai importantă)
    """
    task_id: str
    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    dependencies: Set[str] = field(default_factory=set)
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    priority: int = 0
    
    def is_ready(self, completed_tasks: Set[str]) -> bool:
        """
        Verifică dacă task-ul este gata de execuție.
        
        Args:
            completed_tasks: Set de task-uri deja completate
            
        Returns:
            True dacă toate dependențele sunt satisfăcute
        """
        return self.dependencies.issubset(completed_tasks)
    
    def execute(self) -> Any:
        """
        Execută task-ul.
        
        Returns:
            Rezultatul execuției
            
        Raises:
            Exception: Orice excepție din funcția task-ului
        """
        self.status = TaskStatus.RUNNING
        try:
            self.result = self.func(*self.args, **self.kwargs)
            self.status = TaskStatus.COMPLETED
            logger.debug(f"✅ Task {self.task_id} completed")
            return self.result
        except Exception as e:
            self.status = TaskStatus.FAILED
            logger.error(f"❌ Task {self.task_id} failed: {e}")
            raise


class DependencyGraph:
    """
    Graf de dependențe pentru task-uri.
    
    Implementează topological sort pentru a determina ordinea
    de execuție a task-urilor respectând dependențele.
    """
    
    def __init__(self):
        """Inițializează un graf de dependențe gol."""
        self.tasks: Dict[str, Task] = {}
        self.adjacency_list: Dict[str, List[str]] = defaultdict(list)
        self.reverse_adjacency: Dict[str, List[str]] = defaultdict(list)
        
        logger.debug("🔗 Dependency graph initialized")
    
    def add_task(self, task: Task):
        """
        Adaugă un task în graf.
        
        Args:
            task: Task-ul de adăugat
            
        Raises:
            ValueError: Dacă task_id există deja
        """
        if task.task_id in self.tasks:
            raise ValueError(f"Task {task.task_id} already exists in graph")
        
        self.tasks[task.task_id] = task
        
        # Construiește liste de adiacență
        for dep_id in task.dependencies:
            self.adjacency_list[dep_id].append(task.task_id)
            self.reverse_adjacency[task.task_id].append(dep_id)
        
        # Asigură că task-ul există în adjacency list chiar dacă nu are dependenți
        if task.task_id not in self.adjacency_list:
            self.adjacency_list[task.task_id] = []
        
        logger.debug(f"➕ Added task {task.task_id} with {len(task.dependencies)} dependencies")
    
    def remove_task(self, task_id: str):
        """
        Elimină un task din graf.
        
        Args:
            task_id: ID-ul task-ului de eliminat
        """
        if task_id not in self.tasks:
            logger.warning(f"⚠️ Task {task_id} not found in graph")
            return
        
        # Elimină task-ul
        del self.tasks[task_id]
        
        # Curăță liste de adiacență
        if task_id in self.adjacency_list:
            del self.adjacency_list[task_id]
        
        for deps in self.adjacency_list.values():
            if task_id in deps:
                deps.remove(task_id)
        
        if task_id in self.reverse_adjacency:
            del self.reverse_adjacency[task_id]
        
        logger.debug(f"➖ Removed task {task_id}")
    
    def topological_sort(self) -> List[str]:
        """
        Efectuează sortare topologică folosind algoritmul lui Kahn.
        
        Returns:
            Lista de task_id-uri în ordine topologică
            
        Raises:
            ValueError: Dacă graful conține cicluri
        """
        # Calculează in-degree pentru fiecare nod
        in_degree: Dict[str, int] = defaultdict(int)
        for task_id in self.tasks:
            in_degree[task_id] = len(self.reverse_adjacency.get(task_id, []))
        
        # Queue cu nodurile fără dependențe
        queue = deque([task_id for task_id, deg in in_degree.items() if deg == 0])
        
        sorted_order = []
        
        while queue:
            # Scoate un nod din queue
            current = queue.popleft()
            sorted_order.append(current)
            
            # Reduce in-degree pentru toți dependenții
            for dependent in self.adjacency_list.get(current, []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        # Verifică dacă am procesat toate nodurile
        if len(sorted_order) != len(self.tasks):
            # Există un ciclu în graf
            remaining = set(self.tasks.keys()) - set(sorted_order)
            raise ValueError(f"Dependency graph contains cycle involving tasks: {remaining}")
        
        logger.debug(f"📊 Topological sort: {len(sorted_order)} tasks ordered")
        
        return sorted_order
    
    def get_execution_levels(self) -> List[List[str]]:
        """
        Determină nivelele de execuție paralelă.
        
        Task-urile din același nivel pot fi executate în paralel
        deoarece nu au dependențe între ele.
        
        Returns:
            Lista de liste cu task_id-uri, fiecare sublistă = un nivel de execuție
        """
        levels: List[List[str]] = []
        completed: Set[str] = set()
        
        # Continuă până când toate task-urile sunt procesate
        while len(completed) < len(self.tasks):
            # Găsește toate task-urile ready în acest nivel
            current_level = []
            
            for task_id, task in self.tasks.items():
                if task_id not in completed and task.is_ready(completed):
                    current_level.append(task_id)
            
            if not current_level:
                # Nu mai sunt task-uri ready, dar mai sunt task-uri necompletate
                # Probabil există un ciclu
                remaining = set(self.tasks.keys()) - completed
                raise ValueError(f"Cannot determine execution levels. Remaining tasks: {remaining}")
            
            levels.append(current_level)
            completed.update(current_level)
        
        logger.info(f"🎯 Execution levels determined: {len(levels)} levels")
        for i, level in enumerate(levels):
            logger.debug(f"  Level {i}: {len(level)} tasks - {level}")
        
        return levels
    
    def has_cycle(self) -> bool:
        """
        Verifică dacă graful conține cicluri.
        
        Returns:
            True dacă există cicluri, False altfel
        """
        try:
            self.topological_sort()
            return False
        except ValueError:
            return True
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Obține un task din graf după ID.
        
        Args:
            task_id: ID-ul task-ului
            
        Returns:
            Task-ul sau None dacă nu există
        """
        return self.tasks.get(task_id)
    
    def get_dependencies(self, task_id: str) -> List[str]:
        """
        Obține lista de dependențe pentru un task.
        
        Args:
            task_id: ID-ul task-ului
            
        Returns:
            Lista de task_id-uri de care depinde
        """
        task = self.tasks.get(task_id)
        return list(task.dependencies) if task else []
    
    def get_dependents(self, task_id: str) -> List[str]:
        """
        Obține lista de task-uri care depind de acest task.
        
        Args:
            task_id: ID-ul task-ului
            
        Returns:
            Lista de task_id-uri care depind de acest task
        """
        return self.adjacency_list.get(task_id, [])


class TaskScheduler:
    """
    Scheduler pentru task-uri cu dependențe.
    
    Orchestrează execuția task-urilor în ordine corectă,
    respectând dependențele și maximizând paralelismul.
    """
    
    def __init__(self):
        """Inițializează scheduler-ul."""
        self.graph = DependencyGraph()
        self.completed_tasks: Set[str] = set()
        self.failed_tasks: Set[str] = set()
        
        logger.info("📅 Task scheduler initialized")
    
    def add_task(
        self,
        task_id: str,
        func: Callable,
        args: tuple = (),
        kwargs: dict = None,
        dependencies: Set[str] = None,
        priority: int = 0
    ):
        """
        Adaugă un task pentru scheduling.
        
        Args:
            task_id: Identificator unic pentru task
            func: Funcția de executat
            args: Argumente pentru funcție
            kwargs: Argumente cu nume pentru funcție
            dependencies: Set de task_id-uri de care depinde
            priority: Prioritatea task-ului
        """
        task = Task(
            task_id=task_id,
            func=func,
            args=args,
            kwargs=kwargs or {},
            dependencies=dependencies or set(),
            priority=priority
        )
        
        self.graph.add_task(task)
    
    def get_execution_plan(self) -> List[List[str]]:
        """
        Calculează planul de execuție cu nivele paralele.
        
        Returns:
            Lista de nivele, fiecare nivel conține task-uri care pot rula în paralel
        """
        return self.graph.get_execution_levels()
    
    def execute_sequential(self) -> Dict[str, Any]:
        """
        Execută toate task-urile secvențial în ordine topologică.
        
        Returns:
            Dicționar cu rezultatele task-urilor (task_id -> result)
        """
        logger.info("🚀 Starting sequential execution")
        
        sorted_tasks = self.graph.topological_sort()
        results = {}
        
        for task_id in sorted_tasks:
            task = self.graph.get_task(task_id)
            if not task:
                continue
            
            try:
                result = task.execute()
                results[task_id] = result
                self.completed_tasks.add(task_id)
            except Exception as e:
                logger.error(f"❌ Task {task_id} failed: {e}")
                self.failed_tasks.add(task_id)
                results[task_id] = None
        
        logger.info(f"✅ Sequential execution complete: {len(self.completed_tasks)} completed, {len(self.failed_tasks)} failed")
        
        return results
    
    def get_ready_tasks(self) -> List[Task]:
        """
        Obține toate task-urile care sunt ready pentru execuție.
        
        Returns:
            Lista de task-uri ready
        """
        ready = []
        
        for task_id, task in self.graph.tasks.items():
            if task_id not in self.completed_tasks and task_id not in self.failed_tasks:
                if task.is_ready(self.completed_tasks):
                    ready.append(task)
        
        # Sortează după prioritate (descrescător)
        ready.sort(key=lambda t: t.priority, reverse=True)
        
        return ready
    
    def mark_completed(self, task_id: str):
        """
        Marchează un task ca fiind completat.
        
        Args:
            task_id: ID-ul task-ului completat
        """
        self.completed_tasks.add(task_id)
        task = self.graph.get_task(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
    
    def mark_failed(self, task_id: str):
        """
        Marchează un task ca fiind eșuat.
        
        Args:
            task_id: ID-ul task-ului eșuat
        """
        self.failed_tasks.add(task_id)
        task = self.graph.get_task(task_id)
        if task:
            task.status = TaskStatus.FAILED
    
    def reset(self):
        """Resetează scheduler-ul."""
        self.completed_tasks.clear()
        self.failed_tasks.clear()
        
        # Resetează statusul tuturor task-urilor
        for task in self.graph.tasks.values():
            task.status = TaskStatus.PENDING
            task.result = None
        
        logger.info("🔄 Scheduler reset")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Returnează statistici despre task-uri.
        
        Returns:
            Dicționar cu statistici
        """
        total_tasks = len(self.graph.tasks)
        
        return {
            'total_tasks': total_tasks,
            'completed': len(self.completed_tasks),
            'failed': len(self.failed_tasks),
            'pending': total_tasks - len(self.completed_tasks) - len(self.failed_tasks),
            'has_cycle': self.graph.has_cycle(),
            'execution_levels': len(self.graph.get_execution_levels()) if not self.graph.has_cycle() else None
        }
