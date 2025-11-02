"""
PHALANX-EXECUTOR - Executor pentru Execuție Paralelă Reală
Implementare folosind ProcessPoolExecutor pentru paralelism real

Această clasă orchestrează execuția paralelă a task-urilor,
măsoară performanța și calculează metrici folosind Kronos-Arbiter.
"""

from concurrent.futures import ProcessPoolExecutor, as_completed, Future
from dataclasses import dataclass, field
from typing import Callable, List, Any, Dict, Optional, Tuple
import multiprocessing
import time
import os
from loguru import logger

# Fix for Python 3.12+ multiprocessing fork deprecation warning
# Set spawn method to avoid fork() deadlocks in multi-threaded environments
try:
    multiprocessing.set_start_method('spawn', force=False)
except RuntimeError:
    # Method already set, ignore
    pass


@dataclass
class PhalanxConfig:
    """
    Configurație pentru Phalanx Executor.
    
    Attributes:
        max_workers: Numărul maxim de workeri (None = auto-detect)
        chunk_size: Dimensiunea chunk-urilor pentru batch processing
        timeout: Timeout în secunde pentru fiecare task
        auto_detect_cores: Auto-detectează numărul de core-uri disponibile
    """
    max_workers: Optional[int] = None
    chunk_size: int = 10
    timeout: Optional[float] = None
    auto_detect_cores: bool = True
    
    def __post_init__(self):
        """Validează și ajustează configurația după inițializare."""
        if self.auto_detect_cores and self.max_workers is None:
            # Auto-detectează numărul de core-uri
            self.max_workers = multiprocessing.cpu_count()
            logger.info(f"🔍 Auto-detected {self.max_workers} CPU cores")
        
        # Asigură că avem cel puțin 1 worker
        if self.max_workers is not None and self.max_workers < 1:
            self.max_workers = 1
            logger.warning("⚠️ max_workers adjusted to minimum of 1")
        
        # Validează chunk_size
        if self.chunk_size < 1:
            self.chunk_size = 1
            logger.warning("⚠️ chunk_size adjusted to minimum of 1")
    
    def get_effective_workers(self) -> int:
        """Returnează numărul efectiv de workeri."""
        return self.max_workers or 1


class PhalanxExecutor:
    """
    Phalanx Executor: Orchestrare pentru execuție paralelă reală.
    
    Folosește ProcessPoolExecutor pentru paralelism adevărat (nu threading)
    și măsoară performanța execuției paralele vs. secvențiale.
    """
    
    def __init__(self, config: Optional[PhalanxConfig] = None):
        """
        Inițializează Phalanx Executor.
        
        Args:
            config: Configurație pentru executor (sau None pentru defaults)
        """
        self.config = config or PhalanxConfig()
        self.execution_count = 0
        self.total_speedup = 0.0
        self.execution_history: List[Dict[str, Any]] = []
        
        logger.info(f"⚔️ Phalanx Executor initialized with {self.config.get_effective_workers()} workers")
    
    def execute_tasks(
        self,
        func: Callable,
        tasks: List[Any],
        use_parallel: bool = True,
        measure_sequential: bool = False
    ) -> Tuple[List[Any], Dict[str, float]]:
        """
        Execută task-uri în paralel sau secvențial.
        
        Args:
            func: Funcția de aplicat fiecărui task
            tasks: Lista de task-uri (argumente pentru funcție)
            use_parallel: True pentru execuție paralelă, False pentru secvențială
            measure_sequential: True pentru a măsura și timpul secvențial (pentru comparație)
            
        Returns:
            Tuple (rezultate, metrici) unde metrici conține timpi și speedup
        """
        if not tasks:
            logger.warning("⚠️ No tasks to execute")
            return [], {'t_parallel': 0.0, 't_sequential': 0.0, 'speedup': 1.0}
        
        logger.info(f"🚀 Executing {len(tasks)} tasks, parallel={use_parallel}")
        
        # Execuție paralelă
        if use_parallel:
            results, t_parallel = self._execute_parallel(func, tasks)
        else:
            results, t_parallel = self._execute_sequential(func, tasks)
        
        # Măsoară și timpul secvențial pentru comparație
        t_sequential = 0.0
        if measure_sequential and use_parallel:
            _, t_sequential = self._execute_sequential(func, tasks)
            logger.info(f"📊 Sequential time measured: {t_sequential:.3f}s for comparison")
        elif not use_parallel:
            t_sequential = t_parallel
        
        # Calculează metrici
        speedup = t_sequential / t_parallel if t_parallel > 0 and t_sequential > 0 else 1.0
        
        metrici = {
            't_parallel': t_parallel,
            't_sequential': t_sequential,
            'speedup': speedup,
            'n_tasks': len(tasks),
            'n_workers': self.config.get_effective_workers()
        }
        
        # Actualizează statistici
        self.execution_count += 1
        if speedup > 0:
            self.total_speedup += speedup
        
        # Salvează în istoric
        self.execution_history.append({
            'timestamp': time.time(),
            'n_tasks': len(tasks),
            'parallel': use_parallel,
            **metrici
        })
        
        logger.info(f"✅ Execution complete: {len(results)} results, speedup={speedup:.2f}x")
        
        return results, metrici
    
    def _execute_parallel(
        self,
        func: Callable,
        tasks: List[Any]
    ) -> Tuple[List[Any], float]:
        """
        Execută task-uri în paralel folosind ProcessPoolExecutor.
        
        Args:
            func: Funcția de aplicat
            tasks: Lista de task-uri
            
        Returns:
            Tuple (rezultate, timp_executie)
        """
        start_time = time.time()
        results = []
        
        with ProcessPoolExecutor(max_workers=self.config.max_workers) as executor:
            # Submit toate task-urile
            future_to_task = {
                executor.submit(func, task): task 
                for task in tasks
            }
            
            # Colectează rezultatele pe măsură ce se completează
            for future in as_completed(future_to_task, timeout=self.config.timeout):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    task = future_to_task[future]
                    logger.error(f"❌ Task failed: {task}, error: {e}")
                    results.append(None)  # Placeholder pentru task-ul eșuat
        
        elapsed_time = time.time() - start_time
        logger.debug(f"⚡ Parallel execution: {elapsed_time:.3f}s")
        
        return results, elapsed_time
    
    def _execute_sequential(
        self,
        func: Callable,
        tasks: List[Any]
    ) -> Tuple[List[Any], float]:
        """
        Execută task-uri secvențial (pentru comparație).
        
        Args:
            func: Funcția de aplicat
            tasks: Lista de task-uri
            
        Returns:
            Tuple (rezultate, timp_executie)
        """
        start_time = time.time()
        results = []
        
        for task in tasks:
            try:
                result = func(task)
                results.append(result)
            except Exception as e:
                logger.error(f"❌ Task failed: {task}, error: {e}")
                results.append(None)
        
        elapsed_time = time.time() - start_time
        logger.debug(f"🐌 Sequential execution: {elapsed_time:.3f}s")
        
        return results, elapsed_time
    
    def map_parallel(
        self,
        func: Callable,
        iterable: List[Any],
        chunksize: Optional[int] = None
    ) -> List[Any]:
        """
        Map paralel similar cu Pool.map() dar folosind ProcessPoolExecutor.
        
        Args:
            func: Funcția de aplicat
            iterable: Iterabil cu argumente
            chunksize: Dimensiunea chunk-urilor (sau None pentru default)
            
        Returns:
            Lista cu rezultate în ordinea originală
        """
        chunksize = chunksize or self.config.chunk_size
        
        logger.info(f"🗺️ Mapping {len(iterable)} items with chunksize={chunksize}")
        
        start_time = time.time()
        
        with ProcessPoolExecutor(max_workers=self.config.max_workers) as executor:
            results = list(executor.map(func, iterable, chunksize=chunksize))
        
        elapsed_time = time.time() - start_time
        logger.info(f"✅ Map complete in {elapsed_time:.3f}s")
        
        return results
    
    def submit_task(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Future:
        """
        Submit un singur task asincron.
        
        Args:
            func: Funcția de executat
            *args: Argumente poziționale
            **kwargs: Argumente cu nume
            
        Returns:
            Future object pentru task
        """
        executor = ProcessPoolExecutor(max_workers=self.config.max_workers)
        future = executor.submit(func, *args, **kwargs)
        
        logger.debug(f"📤 Task submitted: {func.__name__}")
        
        return future
    
    def batch_execute(
        self,
        func: Callable,
        tasks: List[Any],
        batch_size: int = 100
    ) -> List[Any]:
        """
        Execută task-uri în batch-uri pentru a evita overhead-ul excesiv.
        
        Args:
            func: Funcția de aplicat
            tasks: Lista de task-uri
            batch_size: Dimensiunea fiecărui batch
            
        Returns:
            Lista cu rezultate
        """
        if not tasks:
            return []
        
        logger.info(f"📦 Batch execution: {len(tasks)} tasks in batches of {batch_size}")
        
        all_results = []
        
        # Împarte în batch-uri
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            logger.debug(f"Processing batch {i // batch_size + 1}: {len(batch)} tasks")
            
            results, _ = self.execute_tasks(func, batch, use_parallel=True)
            all_results.extend(results)
        
        logger.info(f"✅ Batch execution complete: {len(all_results)} results")
        
        return all_results
    
    def get_average_speedup(self) -> float:
        """
        Calculează speedup-ul mediu din toate execuțiile.
        
        Returns:
            Speedup-ul mediu
        """
        if self.execution_count == 0:
            return 1.0
        
        return self.total_speedup / self.execution_count
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Returnează statistici despre execuțiile efectuate.
        
        Returns:
            Dicționar cu statistici
        """
        if not self.execution_history:
            return {
                'executions': 0,
                'avg_speedup': 1.0,
                'total_tasks': 0
            }
        
        parallel_executions = [h for h in self.execution_history if h['parallel']]
        
        stats = {
            'executions': len(self.execution_history),
            'parallel_executions': len(parallel_executions),
            'sequential_executions': len(self.execution_history) - len(parallel_executions),
            'total_tasks': sum(h['n_tasks'] for h in self.execution_history),
            'avg_speedup': self.get_average_speedup(),
            'max_speedup': max((h['speedup'] for h in parallel_executions), default=1.0),
            'min_speedup': min((h['speedup'] for h in parallel_executions), default=1.0),
            'configured_workers': self.config.get_effective_workers()
        }
        
        return stats
    
    def reset_statistics(self):
        """Resetează toate statisticile."""
        self.execution_count = 0
        self.total_speedup = 0.0
        self.execution_history.clear()
        logger.info("🔄 Statistics reset")
    
    def benchmark(
        self,
        func: Callable,
        tasks: List[Any],
        iterations: int = 3
    ) -> Dict[str, Any]:
        """
        Benchmarkează execuția paralelă vs secvențială pentru un set de task-uri.
        
        Args:
            func: Funcția de benchmarcat
            tasks: Lista de task-uri
            iterations: Număr de iterații pentru fiecare metodă
            
        Returns:
            Dicționar cu rezultate benchmark
        """
        logger.info(f"🏁 Starting benchmark with {len(tasks)} tasks, {iterations} iterations")
        
        # Benchmark secvențial
        sequential_times = []
        for i in range(iterations):
            _, t_seq = self._execute_sequential(func, tasks)
            sequential_times.append(t_seq)
            logger.debug(f"Sequential iteration {i+1}: {t_seq:.3f}s")
        
        # Benchmark paralel
        parallel_times = []
        for i in range(iterations):
            _, t_par = self._execute_parallel(func, tasks)
            parallel_times.append(t_par)
            logger.debug(f"Parallel iteration {i+1}: {t_par:.3f}s")
        
        # Calculează statistici
        avg_seq = sum(sequential_times) / len(sequential_times)
        avg_par = sum(parallel_times) / len(parallel_times)
        speedup = avg_seq / avg_par if avg_par > 0 else 1.0
        
        benchmark_results = {
            'n_tasks': len(tasks),
            'iterations': iterations,
            'sequential': {
                'avg': avg_seq,
                'min': min(sequential_times),
                'max': max(sequential_times),
                'times': sequential_times
            },
            'parallel': {
                'avg': avg_par,
                'min': min(parallel_times),
                'max': max(parallel_times),
                'times': parallel_times
            },
            'speedup': speedup,
            'efficiency': speedup / self.config.get_effective_workers()
        }
        
        logger.info(f"🏆 Benchmark complete: Speedup={speedup:.2f}x, Efficiency={benchmark_results['efficiency']:.2%}")
        
        return benchmark_results
