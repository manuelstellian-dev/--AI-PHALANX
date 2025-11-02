"""
Metrics Routes
Expune metrici Prometheus pentru monitorizare
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any
from loguru import logger
import api.server as server
import time

router = APIRouter()


# Cache pentru metrici (refresh la fiecare 5 secunde)
_metrics_cache = {}
_last_update = 0


async def get_metrics() -> Dict[str, Any]:
    """
    Colectează metrici de la toate modulele.
    
    Returns:
        Dicționar cu metrici
    """
    global _metrics_cache, _last_update
    
    current_time = time.time()
    
    # Folosește cache-ul dacă este recent
    if current_time - _last_update < 5:
        return _metrics_cache
    
    metrics = {
        "timestamp": current_time,
        "system": "ΛΕΩΝΙΔΑΣ-AI PHALANX",
        "uptime": current_time - server.app.state.get('start_time', current_time) if hasattr(server.app, 'state') else 0
    }
    
    if server.leonidas_brain:
        # Metrici de la Λ-Core
        brain_status = server.leonidas_brain.get_status()
        metrics["lambda_tas"] = brain_status.get("lambda_tas", 1.0)
        
        modules = server.leonidas_brain.modules
        
        # Metrici de la Helot
        if 'phalanx' in modules and 'helot' in modules['phalanx']:
            helot = modules['phalanx']['helot']
            resources = await helot.monitor_resources()
            metrics["survival_probability"] = helot.survival_probability
            metrics["cpu_percent"] = resources.get("cpu_percent", 0)
            metrics["memory_percent"] = resources.get("memory_percent", 0)
            metrics["disk_percent"] = resources.get("disk_percent", 0)
        
        # Metrici de la Agoge
        if 'phalanx' in modules and 'agoge' in modules['phalanx']:
            agoge = modules['phalanx']['agoge']
            metrics["adaptation_factor"] = await agoge.get_adaptation_factor()
            metrics["training_cycles"] = agoge.training_cycles_completed
        
        # Metrici de la Krypteia
        if 'phalanx' in modules and 'krypteia' in modules['phalanx']:
            krypteia = modules['phalanx']['krypteia']
            threat_assessment = await krypteia.get_threat_assessment()
            metrics["threat_level"] = threat_assessment.get("threat_level", "unknown")
            metrics["threats_detected"] = threat_assessment.get("threats_detected", 0)
        
        # Metrici de la Battle Oracle
        if 'hoplites' in modules and 'oracle' in modules['hoplites']:
            oracle = modules['hoplites']['oracle']
            metrics["predictions_made"] = len(oracle.prediction_history)
        
        # Metrici de la Messenger
        if 'hoplites' in modules and 'messenger' in modules['hoplites']:
            messenger = modules['hoplites']['messenger']
            metrics["messages_sent"] = len(messenger.sent_messages)
            metrics["messages_received"] = len(messenger.received_messages)
            metrics["messages_queued"] = len(messenger.message_queue)
    
    _metrics_cache = metrics
    _last_update = current_time
    
    return metrics


@router.get("/metrics")
async def get_prometheus_metrics(token: str = Depends(server.verify_token)) -> str:
    """
    Returnează metrici în format Prometheus (necesită autentificare).
    
    Returns:
        Metrici în format Prometheus
    """
    metrics = await get_metrics()
    
    # Formatează metricile în format Prometheus
    prometheus_output = []
    
    prometheus_output.append("# HELP leonidas_survival_probability Probabilitatea de supraviețuire a sistemului")
    prometheus_output.append("# TYPE leonidas_survival_probability gauge")
    prometheus_output.append(f"leonidas_survival_probability {metrics.get('survival_probability', 0)}")
    
    prometheus_output.append("# HELP leonidas_cpu_percent Utilizarea CPU (%)")
    prometheus_output.append("# TYPE leonidas_cpu_percent gauge")
    prometheus_output.append(f"leonidas_cpu_percent {metrics.get('cpu_percent', 0)}")
    
    prometheus_output.append("# HELP leonidas_memory_percent Utilizarea memoriei (%)")
    prometheus_output.append("# TYPE leonidas_memory_percent gauge")
    prometheus_output.append(f"leonidas_memory_percent {metrics.get('memory_percent', 0)}")
    
    prometheus_output.append("# HELP leonidas_lambda_tas Timpul Autonom Spartan (Λ-TAS)")
    prometheus_output.append("# TYPE leonidas_lambda_tas gauge")
    prometheus_output.append(f"leonidas_lambda_tas {metrics.get('lambda_tas', 1.0)}")
    
    prometheus_output.append("# HELP leonidas_adaptation_factor Factorul de adaptare din Agoge")
    prometheus_output.append("# TYPE leonidas_adaptation_factor gauge")
    prometheus_output.append(f"leonidas_adaptation_factor {metrics.get('adaptation_factor', 1.0)}")
    
    prometheus_output.append("# HELP leonidas_threats_detected Număr de amenințări detectate")
    prometheus_output.append("# TYPE leonidas_threats_detected counter")
    prometheus_output.append(f"leonidas_threats_detected {metrics.get('threats_detected', 0)}")
    
    prometheus_output.append("# HELP leonidas_messages_sent Număr de mesaje trimise")
    prometheus_output.append("# TYPE leonidas_messages_sent counter")
    prometheus_output.append(f"leonidas_messages_sent {metrics.get('messages_sent', 0)}")
    
    return "\n".join(prometheus_output)


@router.get("/metrics/json")
async def get_json_metrics(token: str = Depends(server.verify_token)) -> Dict[str, Any]:
    """
    Returnează metrici în format JSON (necesită autentificare).
    
    Returns:
        Metrici în format JSON
    """
    return await get_metrics()
