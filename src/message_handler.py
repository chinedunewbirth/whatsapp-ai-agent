"""
Message Handler Module
Processes incoming WhatsApp messages and determines response strategy.
"""

import logging
import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


class MessageHandler:
    """Handles message processing and filtering."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize message handler."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Message filtering configuration
        self.allowed_contacts = set(config.get('allowed_contacts', []))
        self.blocked_contacts = set(config.get('blocked_contacts', []))
        self.respond_to_groups = config.get('respond_to_groups', False)
        self.require_mention = config.get('require_mention_in_groups', True)
        
        # Rate limiting
        self.rate_limit_enabled = config.get('rate_limit_enabled', True)
        self.max_messages_per_hour = config.get('max_messages_per_hour', 30)
        self.message_timestamps = {}
        
        # Command patterns
        self.command_patterns = {
            'help': r'^(?:help|\/help|\?help)$',
            'status': r'^(?:status|\/status)$',
            'clear': r'^(?:clear|\/clear|reset)$',
            'stop': r'^(?:stop|\/stop|pause)$',
            'start': r'^(?:start|\/start|resume)$'
        }
        
        # Bot mention patterns
        self.mention_patterns = [
            r'@bot',
            r'hey bot',
            r'hi bot',
            r'^bot[,:\s]',
            config.get('bot_name', 'AI Assistant').lower()
        ]
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming message and determine response strategy."""
        try:
            sender = message.get('from', '')
            content = message.get('body', '').strip()
            is_group = message.get('isGroupMsg', False)
            message_type = message.get('type', 'text')
            
            self.logger.info(f"Processing message from {sender}: {content[:50]}...")
            
            # Initialize response data
            response_data = {
                'content': content,
                'sender': sender,
                'is_group': is_group,
                'message_type': message_type,
                'should_respond': False,
                'response_type': 'text',
                'context': {},
                'timestamp': datetime.now().isoformat()
            }
            
            # Skip non-text messages for now
            if message_type != 'text':
                self.logger.info(f"Skipping non-text message type: {message_type}")
                return response_data
            
            # Check if sender is blocked
            if self._is_blocked_contact(sender):
                self.logger.info(f"Message from blocked contact: {sender}")
                return response_data
            
            # Check if sender is allowed (if whitelist is enabled)
            if self.allowed_contacts and not self._is_allowed_contact(sender):
                self.logger.info(f"Message from non-allowed contact: {sender}")
                return response_data
            
            # Handle group messages
            if is_group:
                if not self.respond_to_groups:
                    self.logger.info("Group messages disabled")
                    return response_data
                
                if self.require_mention and not self._is_bot_mentioned(content):
                    self.logger.info("Bot not mentioned in group message")
                    return response_data
            
            # Check rate limiting
            if not self._check_rate_limit(sender):
                self.logger.warning(f"Rate limit exceeded for {sender}")
                response_data['should_respond'] = True
                response_data['content'] = "You're sending messages too quickly. Please wait a moment before sending another message."
                return response_data
            
            # Process commands
            command_result = await self._process_command(content, sender)
            if command_result:
                response_data.update(command_result)
                response_data['should_respond'] = True
                return response_data
            
            # Clean message content
            cleaned_content = self._clean_message_content(content, is_group)
            response_data['content'] = cleaned_content
            
            # Add context information
            response_data['context'] = {
                'is_group': is_group,
                'sender': sender,
                'original_message': content,
                'cleaned_message': cleaned_content,
                'timestamp': datetime.now().isoformat()
            }
            
            # Determine if we should respond
            response_data['should_respond'] = True
            
            return response_data
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return {
                'content': '',
                'should_respond': False,
                'error': str(e)
            }
    
    def _is_blocked_contact(self, sender: str) -> bool:
        """Check if contact is blocked."""
        return sender in self.blocked_contacts
    
    def _is_allowed_contact(self, sender: str) -> bool:
        """Check if contact is allowed (when whitelist is used)."""
        return not self.allowed_contacts or sender in self.allowed_contacts
    
    def _is_bot_mentioned(self, content: str) -> bool:
        """Check if bot is mentioned in the message."""
        content_lower = content.lower()
        return any(re.search(pattern, content_lower) for pattern in self.mention_patterns)
    
    def _check_rate_limit(self, sender: str) -> bool:
        """Check if sender has exceeded rate limit."""
        if not self.rate_limit_enabled:
            return True
        
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        
        # Initialize sender's message history
        if sender not in self.message_timestamps:
            self.message_timestamps[sender] = []
        
        # Remove old timestamps
        self.message_timestamps[sender] = [
            timestamp for timestamp in self.message_timestamps[sender]
            if timestamp > hour_ago
        ]
        
        # Check if rate limit is exceeded
        if len(self.message_timestamps[sender]) >= self.max_messages_per_hour:
            return False
        
        # Add current timestamp
        self.message_timestamps[sender].append(now)
        return True
    
    async def _process_command(self, content: str, sender: str) -> Optional[Dict[str, Any]]:
        """Process bot commands."""
        content_lower = content.lower().strip()
        
        for command, pattern in self.command_patterns.items():
            if re.match(pattern, content_lower):
                self.logger.info(f"Processing command: {command} from {sender}")
                return await self._handle_command(command, sender)
        
        return None
    
    async def _handle_command(self, command: str, sender: str) -> Dict[str, Any]:
        """Handle specific commands."""
        if command == 'help':
            return {
                'content': self._get_help_message(),
                'response_type': 'text'
            }
        
        elif command == 'status':
            return {
                'content': "I'm online and ready to help! 🤖",
                'response_type': 'text'
            }
        
        elif command == 'clear':
            # This would typically clear conversation history
            return {
                'content': "Conversation history cleared! 🧹",
                'response_type': 'text',
                'clear_history': True
            }
        
        elif command == 'stop':
            # Add sender to temporary ignore list
            return {
                'content': "I'll stop responding to your messages. Send 'start' to resume.",
                'response_type': 'text',
                'action': 'pause'
            }
        
        elif command == 'start':
            # Remove sender from ignore list
            return {
                'content': "I'm back! How can I help you?",
                'response_type': 'text',
                'action': 'resume'
            }
        
        return {'content': "Unknown command.", 'response_type': 'text'}
    
    def _clean_message_content(self, content: str, is_group: bool) -> str:
        """Clean and normalize message content."""
        cleaned = content.strip()
        
        # Remove bot mentions in group messages
        if is_group:
            for pattern in self.mention_patterns:
                cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE).strip()
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        return cleaned
    
    def _get_help_message(self) -> str:
        """Get help message with available commands."""
        return (
            "🤖 *AI Assistant Help*\\n\\n"
            "*Available Commands:*\\n"
            "• `help` - Show this help message\\n"
            "• `status` - Check bot status\\n"
            "• `clear` - Clear conversation history\\n"
            "• `stop` - Stop responding to your messages\\n"
            "• `start` - Resume responding\\n\\n"
            "*Just send me any message and I'll try to help!*"
        )
    
    def add_blocked_contact(self, contact: str):
        """Add contact to blocked list."""
        self.blocked_contacts.add(contact)
        self.logger.info(f"Added {contact} to blocked contacts")
    
    def remove_blocked_contact(self, contact: str):
        """Remove contact from blocked list."""
        self.blocked_contacts.discard(contact)
        self.logger.info(f"Removed {contact} from blocked contacts")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get message handler statistics."""
        return {
            'blocked_contacts': len(self.blocked_contacts),
            'allowed_contacts': len(self.allowed_contacts),
            'rate_limited_contacts': len(self.message_timestamps),
            'total_message_history': sum(len(timestamps) for timestamps in self.message_timestamps.values())
        }