"""
Shield Bearer - Modulul de Apărare și Air-Gap
Verifică și impune izolarea rețelei (Air-Gap)
"""

import socket
import subprocess
from typing import Dict, Any
from loguru import logger


class ShieldBearer:
    """
    Modulul Shield Bearer - Apărarea Activă a Falangei.
    Verifică și impune izolarea rețelei (Air-Gap) și protecția firewall.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Inițializează Shield Bearer.
        
        Args:
            config: Configurația de securitate
        """
        self.config = config
        self.airgap_mode = config.get('airgap_mode', 'strict')
        self.allowed_connections = config.get('allowed_connections', [])
        logger.info(f"🛡️ Shield Bearer initialized - Air-Gap mode: {self.airgap_mode}")

    async def check_airgap(self) -> bool:
        """
        Verifică dacă Air-Gap-ul este activ.
        
        Returns:
            True dacă Air-Gap-ul este activ
        """
        if self.airgap_mode == 'disabled':
            logger.info("🌐 Air-Gap disabled - network access allowed")
            return False
        
        # Verifică conexiuni active
        active_connections = await self._check_network_connections()
        
        if self.airgap_mode == 'strict':
            # În modul strict, nici o conexiune externă nu este permisă
            if active_connections:
                logger.warning(f"⚠️ Air-Gap violation: {len(active_connections)} active connections detected")
                return False
            logger.info("✅ Air-Gap active - no external connections")
            return True
        
        elif self.airgap_mode == 'permissive':
            # În modul permisiv, doar conexiunile permise sunt acceptate
            unauthorized = [conn for conn in active_connections 
                          if conn not in self.allowed_connections]
            if unauthorized:
                logger.warning(f"⚠️ Unauthorized connections: {len(unauthorized)}")
                return False
            return True
        
        return True

    async def _check_network_connections(self) -> list:
        """
        Verifică conexiunile de rețea active.
        
        Returns:
            Lista de conexiuni active
        """
        connections = []
        
        try:
            # Utilizează psutil pentru a obține conexiunile (dacă este disponibil)
            import psutil
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED':
                    connections.append({
                        'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None
                    })
        except ImportError:
            logger.warning("⚠️ psutil not available - limited connection monitoring")
        except Exception as e:
            logger.error(f"❌ Error checking connections: {e}")
        
        return connections

    async def enforce_firewall(self) -> Dict[str, Any]:
        """
        Verifică și raportează starea firewall-ului.
        
        Returns:
            Starea firewall-ului
        """
        logger.info("🔥 Checking firewall status...")
        
        result = {
            "firewall_active": False,
            "rules_configured": False,
            "platform": None
        }
        
        try:
            # Detectează platforma
            import platform
            result['platform'] = platform.system()
            
            # Verifică firewall specific platformei
            if result['platform'] == 'Linux':
                result = await self._check_iptables()
            elif result['platform'] == 'Windows':
                result = await self._check_windows_firewall()
            else:
                logger.warning(f"⚠️ Firewall check not implemented for {result['platform']}")
        
        except Exception as e:
            logger.error(f"❌ Error checking firewall: {e}")
        
        return result

    async def _check_iptables(self) -> Dict[str, Any]:
        """
        Verifică iptables pe Linux.
        
        Returns:
            Starea iptables
        """
        try:
            result = subprocess.run(['iptables', '-L'], capture_output=True, text=True, timeout=5)
            return {
                "firewall_active": result.returncode == 0,
                "rules_configured": len(result.stdout) > 100,
                "platform": "Linux"
            }
        except Exception as e:
            logger.debug(f"iptables check failed: {e}")
            return {"firewall_active": False, "platform": "Linux"}

    async def _check_windows_firewall(self) -> Dict[str, Any]:
        """
        Verifică Windows Firewall.
        
        Returns:
            Starea Windows Firewall
        """
        try:
            result = subprocess.run(
                ['netsh', 'advfirewall', 'show', 'allprofiles'],
                capture_output=True, text=True, timeout=5
            )
            return {
                "firewall_active": result.returncode == 0 and 'ON' in result.stdout,
                "rules_configured": True,
                "platform": "Windows"
            }
        except Exception as e:
            logger.debug(f"Windows firewall check failed: {e}")
            return {"firewall_active": False, "platform": "Windows"}

    async def test_external_access(self, host: str = "8.8.8.8", port: int = 53, timeout: int = 2) -> bool:
        """
        Testează dacă accesul extern este posibil.
        
        Args:
            host: Host-ul de testat
            port: Port-ul de testat
            timeout: Timeout în secunde
            
        Returns:
            True dacă conexiunea este posibilă
        """
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            
            can_connect = result == 0
            if can_connect:
                logger.warning(f"⚠️ External access possible to {host}:{port}")
            else:
                logger.info(f"✅ External access blocked to {host}:{port}")
            
            return can_connect
            
        except Exception as e:
            logger.debug(f"External access test error: {e}")
            return False
        finally:
            if sock:
                sock.close()

    async def get_status(self) -> Dict[str, Any]:
        """
        Returnează starea curentă a Shield Bearer.
        
        Returns:
            Dicționar cu starea modulului
        """
        airgap_active = await self.check_airgap()
        firewall_status = await self.enforce_firewall()
        
        return {
            "module": "ShieldBearer",
            "status": "active",
            "airgap_mode": self.airgap_mode,
            "airgap_active": airgap_active,
            "firewall": firewall_status
        }
