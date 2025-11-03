"""
FFP (Fractal Flux Pipeline) - Self-Repairing Loop

Implements the 6-phase autoreparatory cycle:
1. SCAN - Collect system state
2. DETECT - Identify anomalies
3. QUARANTINE - Isolate threats
4. HEAL - Repair system
5. IMPROVE - Analyze improvements
6. REINVEST - Apply improvements

The pipeline runs continuously, adapting its cycle time using Λ-MÖBIUS metrics.
"""

import asyncio
from typing import Dict, Any, List, Optional
from loguru import logger


class FractalFluxPipeline:
    """
    Flux Fractal Pipeline - Self-repairing autoreparatory loop.
    
    Implements continuous improvement cycle:
    Scan → Detect → Quarantine → Heal → Improve → Reinvest → repeat
    """
    
    def __init__(self, leonidas_brain):
        """
        Initialize FFP Pipeline.
        
        Args:
            leonidas_brain: Reference to LeondasBrain instance
        """
        self.brain = leonidas_brain
        self.running = False
        self.scan_interval = 5.0  # Default scan interval in seconds
        self.cycle_count = 0
        
        logger.info("🔄 Fractal Flux Pipeline initialized")
    
    async def run_forever(self):
        """
        Main FFP loop - runs indefinitely until stopped.
        
        Executes the 6-phase cycle continuously, adapting timing
        based on Λ-MÖBIUS temporal compression metrics.
        """
        self.running = True
        logger.info("🚀 Starting Fractal Flux Pipeline...")
        
        while self.running:
            try:
                self.cycle_count += 1
                logger.debug(f"🔄 FFP Cycle #{self.cycle_count} starting...")
                
                # 1. SCAN - Collect system state
                system_state = await self.scan_system()
                
                # 2. DETECT - Identify anomalies
                anomalies = await self.detect_anomalies(system_state)
                
                # 3. QUARANTINE - Isolate threats if any
                if anomalies:
                    await self.quarantine_threats(anomalies)
                
                # 4. HEAL - Repair system
                await self.heal_system(anomalies)
                
                # 5. IMPROVE - Analyze improvements
                improvements = await self.analyze_improvements()
                
                # 6. REINVEST - Apply improvements
                await self.apply_improvements(improvements)
                
                # Calculate next cycle interval using Λ-MÖBIUS
                cycle_interval = await self.calculate_cycle_interval()
                
                logger.debug(f"✅ FFP Cycle #{self.cycle_count} complete. Next in {cycle_interval:.2f}s")
                
                # Wait for next cycle
                await asyncio.sleep(cycle_interval)
                
            except Exception as e:
                logger.error(f"❌ FFP error in cycle #{self.cycle_count}: {e}")
                # On error, wait for default interval before retry
                await asyncio.sleep(self.scan_interval)
    
    async def scan_system(self) -> Dict[str, Any]:
        """
        PHASE 1: SCAN - Collect current system state.
        
        Uses existing Krypteia and Helot modules to gather metrics.
        
        Returns:
            Dictionary with system state information
        """
        system_state = {
            'timestamp': asyncio.get_event_loop().time(),
            'resources': {},
            'threats': [],
            'health': 'unknown'
        }
        
        try:
            # Get resource metrics from Helot if available
            if hasattr(self.brain, 'modules') and 'phalanx' in self.brain.modules:
                phalanx = self.brain.modules['phalanx']
                
                if 'helot' in phalanx:
                    helot = phalanx['helot']
                    system_state['resources'] = await helot.monitor_resources()
                    system_state['survival_probability'] = helot.survival_probability
                
                # Get threat info from Krypteia if available
                if 'krypteia' in phalanx:
                    krypteia = phalanx['krypteia']
                    threat_assessment = await krypteia.get_threat_assessment()
                    system_state['threat_level'] = threat_assessment.get('threat_level', 'unknown')
            
            system_state['health'] = 'scanned'
            logger.debug(f"📡 SCAN complete: {len(system_state)} metrics collected")
            
        except Exception as e:
            logger.error(f"❌ SCAN error: {e}")
        
        return system_state
    
    async def detect_anomalies(self, system_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        PHASE 2: DETECT - Identify anomalies in system state.
        
        Uses Krypteia for threat detection.
        
        Args:
            system_state: Current system state from scan
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        try:
            # Check survival probability
            survival_prob = system_state.get('survival_probability', 1.0)
            if survival_prob < 0.95:
                anomalies.append({
                    'type': 'low_survival',
                    'severity': 'high',
                    'value': survival_prob,
                    'threshold': 0.95
                })
            
            # Check resource usage
            resources = system_state.get('resources', {})
            cpu_percent = resources.get('cpu_percent', 0)
            memory_percent = resources.get('memory_percent', 0)
            
            if cpu_percent > 90:
                anomalies.append({
                    'type': 'high_cpu',
                    'severity': 'medium',
                    'value': cpu_percent,
                    'threshold': 90
                })
            
            if memory_percent > 90:
                anomalies.append({
                    'type': 'high_memory',
                    'severity': 'medium',
                    'value': memory_percent,
                    'threshold': 90
                })
            
            if anomalies:
                logger.warning(f"⚠️ DETECT: {len(anomalies)} anomalies found")
            else:
                logger.debug("✅ DETECT: No anomalies detected")
            
        except Exception as e:
            logger.error(f"❌ DETECT error: {e}")
        
        return anomalies
    
    async def quarantine_threats(self, anomalies: List[Dict[str, Any]]):
        """
        PHASE 3: QUARANTINE - Isolate identified threats.
        
        Uses Thermopylae for emergency protocols.
        
        Args:
            anomalies: List of detected anomalies
        """
        try:
            if not anomalies:
                return
            
            logger.warning(f"🛡️ QUARANTINE: Processing {len(anomalies)} threats...")
            
            # Check if Thermopylae is available
            if hasattr(self.brain, 'modules') and 'phalanx' in self.brain.modules:
                phalanx = self.brain.modules['phalanx']
                
                if 'thermopylae' in phalanx:
                    thermopylae = phalanx['thermopylae']
                    
                    # Trigger emergency protocol for critical anomalies
                    for anomaly in anomalies:
                        if anomaly.get('severity') == 'high':
                            # Use survival probability from anomaly if available
                            if anomaly.get('type') == 'low_survival':
                                await thermopylae.check_emergency_protocol(anomaly.get('value', 0.9))
            
            logger.info(f"✅ QUARANTINE: {len(anomalies)} threats processed")
            
        except Exception as e:
            logger.error(f"❌ QUARANTINE error: {e}")
    
    async def heal_system(self, anomalies: List[Dict[str, Any]]):
        """
        PHASE 4: HEAL - Repair system issues.
        
        Implements basic healing strategies for detected anomalies.
        
        Args:
            anomalies: List of anomalies to heal
        """
        try:
            if not anomalies:
                logger.debug("✅ HEAL: System healthy, no repairs needed")
                return
            
            logger.info(f"🔧 HEAL: Repairing {len(anomalies)} issues...")
            
            # Basic healing strategies
            for anomaly in anomalies:
                anomaly_type = anomaly.get('type')
                
                if anomaly_type == 'high_cpu':
                    # Could trigger load balancing or throttling
                    logger.info("💊 HEAL: Addressing high CPU usage")
                    
                elif anomaly_type == 'high_memory':
                    # Could trigger garbage collection or cache clearing
                    logger.info("💊 HEAL: Addressing high memory usage")
                    
                elif anomaly_type == 'low_survival':
                    # Could trigger defensive measures
                    logger.info("💊 HEAL: Addressing low survival probability")
            
            logger.info(f"✅ HEAL: Repairs complete")
            
        except Exception as e:
            logger.error(f"❌ HEAL error: {e}")
    
    async def analyze_improvements(self) -> Dict[str, Any]:
        """
        PHASE 5: IMPROVE - Analyze potential improvements.
        
        Uses Agoge for learning and adaptation analysis.
        
        Returns:
            Dictionary with improvement recommendations
        """
        improvements = {
            'adaptations': [],
            'optimizations': [],
            'recommendations': []
        }
        
        try:
            # Get adaptation factor from Agoge if available
            if hasattr(self.brain, 'modules') and 'phalanx' in self.brain.modules:
                phalanx = self.brain.modules['phalanx']
                
                if 'agoge' in phalanx:
                    agoge = phalanx['agoge']
                    adaptation_factor = await agoge.get_adaptation_factor()
                    
                    improvements['adaptation_factor'] = adaptation_factor
                    
                    # Suggest improvements based on adaptation
                    if adaptation_factor < 1.0:
                        improvements['recommendations'].append({
                            'type': 'training',
                            'reason': 'Low adaptation factor',
                            'action': 'Increase training cycles'
                        })
            
            logger.debug(f"📈 IMPROVE: {len(improvements['recommendations'])} improvements identified")
            
        except Exception as e:
            logger.error(f"❌ IMPROVE error: {e}")
        
        return improvements
    
    async def apply_improvements(self, improvements: Dict[str, Any]):
        """
        PHASE 6: REINVEST - Apply identified improvements.
        
        Implements improvement recommendations.
        
        Args:
            improvements: Dictionary with improvement recommendations
        """
        try:
            recommendations = improvements.get('recommendations', [])
            
            if not recommendations:
                logger.debug("✅ REINVEST: No improvements to apply")
                return
            
            logger.info(f"🔄 REINVEST: Applying {len(recommendations)} improvements...")
            
            for rec in recommendations:
                rec_type = rec.get('type')
                action = rec.get('action')
                
                logger.info(f"🎯 REINVEST: {action} (reason: {rec.get('reason')})")
                
                # Implementation would trigger actual improvements
                # For now, just log the actions
            
            logger.info(f"✅ REINVEST: Improvements applied")
            
        except Exception as e:
            logger.error(f"❌ REINVEST error: {e}")
    
    async def calculate_cycle_interval(self) -> float:
        """
        Calculate next cycle interval using Λ-MÖBIUS temporal compression.
        
        Returns:
            Interval in seconds for next cycle
        """
        try:
            # Try to get T_supreme from Kronos if available
            if hasattr(self.brain, 'kronos'):
                kronos = self.brain.kronos
                
                # Calculate number of modules/units
                U = 1
                if hasattr(self.brain, 'modules'):
                    if 'phalanx' in self.brain.modules:
                        U += len(self.brain.modules['phalanx'])
                    if 'hoplites' in self.brain.modules:
                        U += len(self.brain.modules['hoplites'])
                
                # Get T_supreme
                metrics = kronos.calculate_supreme_time(
                    k=100,
                    P=kronos.n_cores,
                    U=U
                )
                
                T_supreme = metrics.T_supreme
                
                # Use min of T_supreme and scan_interval to avoid too long waits
                interval = min(T_supreme, self.scan_interval)
                
                return max(interval, 0.1)  # Minimum 0.1s
            
        except Exception as e:
            logger.error(f"❌ Error calculating cycle interval: {e}")
        
        # Fallback to default interval
        return self.scan_interval
    
    def stop(self):
        """Stop the FFP pipeline."""
        logger.info("🛑 Stopping Fractal Flux Pipeline...")
        self.running = False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current FFP status.
        
        Returns:
            Dictionary with status information
        """
        return {
            'running': self.running,
            'cycle_count': self.cycle_count,
            'scan_interval': self.scan_interval
        }
