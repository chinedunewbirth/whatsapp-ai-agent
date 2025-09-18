"""
WhatsApp AI Bot Core Module
Handles WhatsApp message processing and AI responses.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from message_handler import MessageHandler
from ai_processor import AIProcessor
from whatsapp_client import WhatsAppClient


class WhatsAppAIBot:
    """Main WhatsApp AI Bot class."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the WhatsApp AI bot."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.whatsapp_client = WhatsAppClient(config.get('whatsapp', {}))
        self.ai_processor = AIProcessor(config.get('ai', {}))
        self.message_handler = MessageHandler(config.get('messaging', {}))
        
        # Bot state
        self.is_running = False
        self.start_time = None
        
    async def start(self):
        """Start the WhatsApp AI bot."""
        self.logger.info("Initializing WhatsApp AI Bot...")
        
        try:
            # Initialize WhatsApp client
            await self.whatsapp_client.initialize()
            
            # Set up message event handlers
            self.whatsapp_client.on_message(self._handle_message)
            self.whatsapp_client.on_status_update(self._handle_status_update)
            
            self.is_running = True
            self.start_time = datetime.now()
            
            self.logger.info("WhatsApp AI Bot started successfully!")
            
            # Keep the bot running
            while self.is_running:
                await asyncio.sleep(1)
                
        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
            await self.stop()
            raise
    
    async def stop(self):
        """Stop the WhatsApp AI bot."""
        self.logger.info("Stopping WhatsApp AI Bot...")
        
        self.is_running = False
        
        if self.whatsapp_client:
            await self.whatsapp_client.disconnect()
            
        self.logger.info("WhatsApp AI Bot stopped.")
    
    async def _handle_message(self, message: Dict[str, Any]):
        """Handle incoming WhatsApp messages."""
        try:
            self.logger.info(f"Received message from {message.get('from')}: {message.get('body', '')[:50]}...")
            
            # Process the message
            processed_message = await self.message_handler.process_message(message)
            
            if processed_message.get('should_respond', False):
                # Generate AI response
                ai_response = await self.ai_processor.generate_response(
                    message=processed_message.get('content'),
                    context=processed_message.get('context', {}),
                    sender=message.get('from')
                )
                
                if ai_response:
                    # Send response back
                    await self.whatsapp_client.send_message(
                        to=message.get('from'),
                        message=ai_response
                    )
                    
                    self.logger.info(f"Sent AI response to {message.get('from')}")
                    
        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
            
            # Send error message if configured
            if self.config.get('messaging', {}).get('send_error_notifications', False):
                await self.whatsapp_client.send_message(
                    to=message.get('from'),
                    message="Sorry, I encountered an error processing your message. Please try again later."
                )
    
    async def _handle_status_update(self, status: Dict[str, Any]):
        """Handle WhatsApp connection status updates."""
        self.logger.info(f"WhatsApp status update: {status.get('status')}")
        
        if status.get('status') == 'disconnected':
            self.logger.warning("WhatsApp client disconnected. Attempting to reconnect...")
            # You could add reconnection logic here
    
    def get_status(self) -> Dict[str, Any]:
        """Get bot status information."""
        uptime = datetime.now() - self.start_time if self.start_time else None
        
        return {
            'running': self.is_running,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'uptime_seconds': uptime.total_seconds() if uptime else None,
            'whatsapp_connected': self.whatsapp_client.is_connected() if self.whatsapp_client else False
        }