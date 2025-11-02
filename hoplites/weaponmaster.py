"""
Weapon Master - Gestionează Interacțiunea Externă Controlată
Permite interogări web doar dacă external_access_enabled este true
"""

import asyncio
from typing import Dict, Any, Optional
from loguru import logger


class WeaponMaster:
    """
    Modulul Weapon Master - Interacțiune Externă Controlată.
    Gestionează accesul la resurse externe, activat doar când este permis.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Inițializează Weapon Master.
        
        Args:
            config: Configurația de acces extern
        """
        self.config = config
        self.external_access_enabled = config.get('external_access_enabled', False)
        self.allowed_domains = config.get('allowed_domains', [])
        self.request_count = 0
        
        if self.external_access_enabled:
            logger.warning("⚠️ Weapon Master initialized - EXTERNAL ACCESS ENABLED")
        else:
            logger.info("🗡️ Weapon Master initialized - External access DISABLED")

    async def execute_external_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execută o interogare externă (de exemplu, web scraping, API call).
        
        Args:
            query: Detalii despre interogare
                {
                    "type": "http_get" | "http_post" | "dns_lookup",
                    "target": "url sau domeniu",
                    "payload": {...}
                }
        
        Returns:
            Rezultatul interogării
        """
        if not self.external_access_enabled:
            logger.warning("🚫 External access attempt blocked - access disabled")
            return {
                "success": False,
                "error": "External access is disabled",
                "blocked": True
            }
        
        query_type = query.get('type')
        target = query.get('target')
        
        # Verifică dacă domeniul este permis
        if not self._is_domain_allowed(target):
            logger.warning(f"🚫 Access to {target} blocked - domain not in allowlist")
            return {
                "success": False,
                "error": f"Domain {target} not in allowlist",
                "blocked": True
            }
        
        logger.info(f"🗡️ Executing external query: {query_type} to {target}")
        
        try:
            if query_type == "http_get":
                result = await self._execute_http_get(target)
            elif query_type == "http_post":
                result = await self._execute_http_post(target, query.get('payload', {}))
            elif query_type == "dns_lookup":
                result = await self._execute_dns_lookup(target)
            else:
                result = {
                    "success": False,
                    "error": f"Unknown query type: {query_type}"
                }
            
            self.request_count += 1
            return result
            
        except Exception as e:
            logger.error(f"❌ External query error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _execute_http_get(self, url: str) -> Dict[str, Any]:
        """
        Execută o cerere HTTP GET.
        
        Args:
            url: URL-ul de interogat
            
        Returns:
            Rezultatul cererii
        """
        # Placeholder - în producție ar folosi aiohttp sau similar
        logger.info(f"📡 HTTP GET: {url}")
        await asyncio.sleep(0.1)  # Simulare latență rețea
        
        return {
            "success": True,
            "status_code": 200,
            "data": "Simulated response data",
            "note": "This is a placeholder - implement with aiohttp in production"
        }

    async def _execute_http_post(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execută o cerere HTTP POST.
        
        Args:
            url: URL-ul de interogat
            payload: Datele de trimis
            
        Returns:
            Rezultatul cererii
        """
        logger.info(f"📡 HTTP POST: {url}")
        await asyncio.sleep(0.1)
        
        return {
            "success": True,
            "status_code": 200,
            "data": "Simulated POST response",
            "note": "This is a placeholder - implement with aiohttp in production"
        }

    async def _execute_dns_lookup(self, domain: str) -> Dict[str, Any]:
        """
        Execută o interogare DNS.
        
        Args:
            domain: Domeniul de rezolvat
            
        Returns:
            Rezultatul interogării DNS
        """
        import socket
        
        logger.info(f"🔍 DNS lookup: {domain}")
        
        try:
            ip_addresses = socket.gethostbyname_ex(domain)[2]
            return {
                "success": True,
                "domain": domain,
                "ip_addresses": ip_addresses
            }
        except socket.gaierror as e:
            return {
                "success": False,
                "error": f"DNS lookup failed: {e}"
            }

    def _is_domain_allowed(self, target: str) -> bool:
        """
        Verifică dacă un domeniu este în lista de permise.
        
        Args:
            target: URL sau domeniu de verificat
            
        Returns:
            True dacă este permis
        """
        # Dacă nu există restricții, permite tot
        if not self.allowed_domains:
            return True
        
        # Extrage domeniul din URL
        if target.startswith('http'):
            from urllib.parse import urlparse
            domain = urlparse(target).netloc
        else:
            domain = target
        
        # Verifică dacă domeniul este în lista permisă
        return any(allowed in domain for allowed in self.allowed_domains)

    async def enable_external_access(self):
        """
        Activează accesul extern (PERICOL!).
        """
        self.external_access_enabled = True
        logger.warning("⚠️ EXTERNAL ACCESS ENABLED - Air-Gap compromised!")

    async def disable_external_access(self):
        """
        Dezactivează accesul extern.
        """
        self.external_access_enabled = False
        logger.info("🛡️ External access disabled - Air-Gap restored")

    async def add_allowed_domain(self, domain: str):
        """
        Adaugă un domeniu în lista permisă.
        
        Args:
            domain: Domeniul de adăugat
        """
        if domain not in self.allowed_domains:
            self.allowed_domains.append(domain)
            logger.info(f"✅ Domain added to allowlist: {domain}")

    async def remove_allowed_domain(self, domain: str):
        """
        Elimină un domeniu din lista permisă.
        
        Args:
            domain: Domeniul de eliminat
        """
        if domain in self.allowed_domains:
            self.allowed_domains.remove(domain)
            logger.info(f"🗑️ Domain removed from allowlist: {domain}")

    async def get_status(self) -> Dict[str, Any]:
        """
        Returnează starea curentă a Weapon Master.
        
        Returns:
            Dicționar cu starea modulului
        """
        return {
            "module": "WeaponMaster",
            "status": "active",
            "external_access_enabled": self.external_access_enabled,
            "allowed_domains": self.allowed_domains,
            "request_count": self.request_count,
            "warning": "External access compromises Air-Gap security" if self.external_access_enabled else None
        }
