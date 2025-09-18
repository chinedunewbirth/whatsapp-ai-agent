"""
AI Processor Module
Handles AI response generation and conversation context.
"""

import logging
import openai
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class AIProcessor:
    """AI processor for generating intelligent responses."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize AI processor."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # AI configuration
        self.model = config.get('model', 'gpt-3.5-turbo')
        self.max_tokens = config.get('max_tokens', 1000)
        self.temperature = config.get('temperature', 0.7)
        
        # System prompt
        self.system_prompt = config.get('system_prompt', 
            "You are a helpful AI assistant responding to WhatsApp messages. "
            "Be concise, friendly, and helpful in your responses."
        )
        
        # Conversation context storage (in production, use a database)
        self.conversation_history = {}
        self.max_history_length = config.get('max_history_length', 10)
        
        # Initialize OpenAI (if using OpenAI)
        if config.get('provider') == 'openai':
            openai.api_key = config.get('api_key')
    
    async def generate_response(self, message: str, context: Dict[str, Any], sender: str) -> Optional[str]:
        """Generate AI response to a message."""
        try:
            self.logger.info(f"Generating AI response for sender: {sender}")
            
            # Get conversation history
            conversation = self._get_conversation_history(sender)
            
            # Add current message to conversation
            conversation.append({
                'role': 'user',
                'content': message,
                'timestamp': datetime.now().isoformat()
            })
            
            # Generate response based on provider
            response = await self._generate_with_provider(conversation, context)
            
            if response:
                # Add AI response to conversation history
                conversation.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Update conversation history
                self._update_conversation_history(sender, conversation)
                
                return response
                
        except Exception as e:
            self.logger.error(f"Error generating AI response: {e}")
            return None
    
    async def _generate_with_provider(self, conversation: List[Dict], context: Dict[str, Any]) -> Optional[str]:
        """Generate response with configured AI provider."""
        provider = self.config.get('provider', 'openai')
        
        if provider == 'openai':
            return await self._generate_with_openai(conversation, context)
        elif provider == 'anthropic':
            return await self._generate_with_anthropic(conversation, context)
        elif provider == 'local':
            return await self._generate_with_local_model(conversation, context)
        else:
            self.logger.error(f"Unknown AI provider: {provider}")
            return None
    
    async def _generate_with_openai(self, conversation: List[Dict], context: Dict[str, Any]) -> Optional[str]:
        """Generate response using OpenAI API."""
        try:
            # Prepare messages for OpenAI
            messages = [{'role': 'system', 'content': self.system_prompt}]
            
            # Add conversation history (excluding timestamp for API)
            for msg in conversation[-self.max_history_length:]:
                messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
            
            # Make API call
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stop=None
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            return None
    
    async def _generate_with_anthropic(self, conversation: List[Dict], context: Dict[str, Any]) -> Optional[str]:
        """Generate response using Anthropic Claude API."""
        # TODO: Implement Anthropic Claude integration
        self.logger.warning("Anthropic provider not yet implemented")
        return "Sorry, I'm not available right now. Please try again later."
    
    async def _generate_with_local_model(self, conversation: List[Dict], context: Dict[str, Any]) -> Optional[str]:
        """Generate response using local model."""
        # TODO: Implement local model integration (e.g., using Ollama)
        self.logger.warning("Local model provider not yet implemented")
        return "Hello! I'm running on a local model. How can I help you?"
    
    def _get_conversation_history(self, sender: str) -> List[Dict]:
        """Get conversation history for a sender."""
        return self.conversation_history.get(sender, [])
    
    def _update_conversation_history(self, sender: str, conversation: List[Dict]):
        """Update conversation history for a sender."""
        # Keep only the most recent messages
        if len(conversation) > self.max_history_length:
            conversation = conversation[-self.max_history_length:]
        
        self.conversation_history[sender] = conversation
    
    def clear_conversation_history(self, sender: Optional[str] = None):
        """Clear conversation history."""
        if sender:
            self.conversation_history.pop(sender, None)
            self.logger.info(f"Cleared conversation history for {sender}")
        else:
            self.conversation_history.clear()
            self.logger.info("Cleared all conversation history")
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get conversation statistics."""
        total_conversations = len(self.conversation_history)
        total_messages = sum(len(conv) for conv in self.conversation_history.values())
        
        return {
            'total_conversations': total_conversations,
            'total_messages': total_messages,
            'active_conversations': [sender for sender, conv in self.conversation_history.items() if len(conv) > 0]
        }