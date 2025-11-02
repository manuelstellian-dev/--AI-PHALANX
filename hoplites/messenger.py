"""
Messenger - Modulul de Comunicații Securizate
Utilizează Spartan Guard pentru criptarea mesajelor
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from loguru import logger


class Messenger:
    """
    Modulul Messenger - Comunicații Securizate ale Falangei.
    Gestionează trimiterea și primirea de mesaje criptate.
    """

    def __init__(self, config: Dict[str, Any], spartan_guard=None):
        """
        Inițializează Messenger.
        
        Args:
            config: Configurația modulului
            spartan_guard: Instanța Spartan Guard pentru criptare
        """
        self.config = config
        self.spartan_guard = spartan_guard
        self.message_queue = []
        self.sent_messages = []
        self.received_messages = []
        logger.info("📨 Messenger initialized - Secure communications ready")

    async def send_secure_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trimite un mesaj securizat.
        
        Args:
            message_data: Date despre mesaj
                {
                    "recipient": "destinatar",
                    "content": "conținut mesaj",
                    "priority": "high" | "normal" | "low",
                    "encrypt": True/False
                }
        
        Returns:
            Rezultatul trimiterii
        """
        recipient = message_data.get('recipient')
        content = message_data.get('content')
        priority = message_data.get('priority', 'normal')
        should_encrypt = message_data.get('encrypt', True)
        
        logger.info(f"📤 Sending message to {recipient} (priority: {priority})")
        
        try:
            # Criptează mesajul dacă este necesar
            if should_encrypt and self.spartan_guard:
                encrypted_content = await self.spartan_guard.encrypt(content)
                content_to_send = encrypted_content
                is_encrypted = True
            else:
                content_to_send = content
                is_encrypted = False
            
            # Creează mesajul
            message = {
                "id": f"msg_{int(time.time() * 1000)}",
                "recipient": recipient,
                "content": content_to_send,
                "encrypted": is_encrypted,
                "priority": priority,
                "timestamp": time.time(),
                "status": "sent"
            }
            
            # Adaugă în lista de mesaje trimise
            self.sent_messages.append(message)
            
            logger.info(f"✅ Message sent successfully (encrypted: {is_encrypted})")
            
            return {
                "success": True,
                "message_id": message['id'],
                "encrypted": is_encrypted,
                "timestamp": message['timestamp']
            }
            
        except Exception as e:
            logger.error(f"❌ Error sending message: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def receive_message(self, encrypted_message: str) -> Dict[str, Any]:
        """
        Primește și decriptează un mesaj.
        
        Args:
            encrypted_message: Mesajul criptat
            
        Returns:
            Mesajul decriptat
        """
        logger.info("📥 Receiving encrypted message...")
        
        try:
            if self.spartan_guard:
                decrypted_content = await self.spartan_guard.decrypt(encrypted_message)
            else:
                logger.warning("⚠️ No Spartan Guard available - cannot decrypt")
                decrypted_content = encrypted_message
            
            # Creează înregistrarea mesajului primit
            message = {
                "id": f"msg_recv_{int(time.time() * 1000)}",
                "content": decrypted_content,
                "timestamp": time.time(),
                "status": "received"
            }
            
            self.received_messages.append(message)
            
            logger.info("✅ Message received and decrypted successfully")
            
            return {
                "success": True,
                "message_id": message['id'],
                "content": decrypted_content,
                "timestamp": message['timestamp']
            }
            
        except Exception as e:
            logger.error(f"❌ Error receiving message: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def queue_message(self, message_data: Dict[str, Any]):
        """
        Adaugă un mesaj în coadă pentru trimitere ulterioară.
        
        Args:
            message_data: Date despre mesaj
        """
        message_data['queued_at'] = time.time()
        self.message_queue.append(message_data)
        logger.info(f"📋 Message queued (queue size: {len(self.message_queue)})")

    async def process_queue(self) -> Dict[str, Any]:
        """
        Procesează toate mesajele din coadă.
        
        Returns:
            Rezultatul procesării
        """
        if not self.message_queue:
            return {
                "success": True,
                "processed": 0,
                "message": "Queue is empty"
            }
        
        logger.info(f"📮 Processing message queue ({len(self.message_queue)} messages)...")
        
        processed = 0
        failed = 0
        
        while self.message_queue:
            message = self.message_queue.pop(0)
            result = await self.send_secure_message(message)
            
            if result.get('success'):
                processed += 1
            else:
                failed += 1
            
            # Pauză scurtă între mesaje
            await asyncio.sleep(0.1)
        
        logger.info(f"✅ Queue processed - Success: {processed}, Failed: {failed}")
        
        return {
            "success": True,
            "processed": processed,
            "failed": failed
        }

    async def get_sent_messages(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Returnează mesajele trimise.
        
        Args:
            limit: Numărul maxim de mesaje de returnat
            
        Returns:
            Lista de mesaje trimise
        """
        return self.sent_messages[-limit:] if self.sent_messages else []

    async def get_received_messages(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Returnează mesajele primite.
        
        Args:
            limit: Numărul maxim de mesaje de returnat
            
        Returns:
            Lista de mesaje primite
        """
        return self.received_messages[-limit:] if self.received_messages else []

    async def broadcast_message(self, recipients: List[str], content: str, priority: str = "normal") -> Dict[str, Any]:
        """
        Trimite un mesaj către multiple destinații.
        
        Args:
            recipients: Lista de destinatari
            content: Conținutul mesajului
            priority: Prioritatea mesajului
            
        Returns:
            Rezultatul broadcast-ului
        """
        logger.info(f"📢 Broadcasting message to {len(recipients)} recipients...")
        
        results = []
        for recipient in recipients:
            result = await self.send_secure_message({
                "recipient": recipient,
                "content": content,
                "priority": priority,
                "encrypt": True
            })
            results.append(result)
        
        successful = sum(1 for r in results if r.get('success'))
        
        logger.info(f"✅ Broadcast complete - {successful}/{len(recipients)} successful")
        
        return {
            "success": True,
            "total": len(recipients),
            "successful": successful,
            "failed": len(recipients) - successful
        }

    async def get_status(self) -> Dict[str, Any]:
        """
        Returnează starea curentă a Messenger.
        
        Returns:
            Dicționar cu starea modulului
        """
        return {
            "module": "Messenger",
            "status": "active",
            "encryption_available": self.spartan_guard is not None,
            "queued_messages": len(self.message_queue),
            "sent_messages": len(self.sent_messages),
            "received_messages": len(self.received_messages)
        }
