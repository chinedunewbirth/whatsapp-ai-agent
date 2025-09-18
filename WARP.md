# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Create virtual environment (Linux/macOS)  
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode with extras
pip install -e .[dev]
```

### Configuration Setup
```bash
# Generate default config template
python src/config/settings.py

# Copy environment template
cp .env.example .env
# Edit .env with actual API keys and settings

# Copy and edit main config (if using YAML config)
cp config.yaml.example config.yaml
```

### Running the Application
```bash
# Run the bot
python src/main.py

# Alternative if installed as package
whatsapp-ai-agent
```

### Testing and Development
```bash
# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=src

# Run specific test file
pytest tests/test_message_handler.py

# Code formatting and linting
black src/
flake8 src/
mypy src/
```

## Architecture Overview

This is a modular WhatsApp AI chatbot built with Python's asyncio framework. The architecture follows a event-driven pattern with clear separation of concerns:

### Core Components

**Main Application Flow:**
- `main.py` → `bot.py` → `whatsapp_client.py` + `message_handler.py` + `ai_processor.py`

**WhatsAppAIBot (bot.py)** - Central orchestrator that:
- Initializes all components (WhatsApp client, AI processor, message handler)
- Coordinates message flow between components
- Manages bot lifecycle (start/stop/status)
- Handles errors and reconnection logic

**WhatsAppClient (whatsapp_client.py)** - Abstract WhatsApp connection interface supporting:
- Multiple client types: WhatsApp Web, Business API, Unofficial clients
- Event-driven message handling with callback registration
- Connection management and status monitoring
- **Note**: Currently contains placeholder implementations - actual WhatsApp integrations need to be implemented

**MessageHandler (message_handler.py)** - Message processing pipeline that:
- Filters messages based on contact allowlist/blocklist
- Implements rate limiting per contact (configurable messages/hour)
- Handles group message logic (mentions, permissions)
- Processes bot commands (help, status, clear, stop/start)
- Cleans and normalizes message content

**AIProcessor (ai_processor.py)** - AI response generation that:
- Supports multiple AI providers (OpenAI implemented, Anthropic/local planned)
- Maintains conversation context per sender (in-memory, configurable history length)
- Manages system prompts and model parameters
- **Current limitation**: Only OpenAI integration is fully implemented

### Configuration System (config/settings.py)

Hierarchical configuration loading:
1. Default config (if exists)
2. User config.yaml (overrides defaults)
3. Environment-specific config (development_config.yaml, etc.)
4. Environment variables (highest precedence)

Configuration supports both YAML files and environment variables for all settings.

### Key Architectural Patterns

**Event-Driven Messaging**: WhatsApp client uses callback registration for message events, enabling loose coupling between components.

**Async/Await Throughout**: All I/O operations use asyncio for non-blocking execution, allowing handling multiple conversations simultaneously.

**Provider Pattern**: Both AI processing and WhatsApp clients use a provider pattern to support multiple implementations behind a common interface.

**Rate Limiting**: Implemented at the message handler level using in-memory timestamp tracking per sender.

## Development Notes

### WhatsApp Client Implementation Status
The `WhatsAppClient` currently contains placeholder methods. To make this functional, you need to implement one of:
- **WhatsApp Web**: Use libraries like whatsapp-web.js (via subprocess) or selenium
- **Business API**: HTTP API calls to Meta's WhatsApp Business API
- **Unofficial**: Libraries like baileys or similar (risks ToS violations)

### AI Provider Extensions
To add new AI providers:
1. Implement provider methods in `AIProcessor._generate_with_[provider]`
2. Add configuration options in `config/settings.py`
3. Update environment variable handling

### Testing Strategy
- Use `WhatsAppClient.simulate_incoming_message()` for testing message flows
- Mock AI API calls to avoid costs during testing
- Test rate limiting with rapid message simulation

### Configuration Precedence
Environment variables always override config files. Use `.env` for local development and environment variables for deployment.

### Message Flow
```
Incoming WhatsApp Message
→ WhatsAppClient (receives)
→ MessageHandler (filters, processes commands, rate limits)
→ AIProcessor (generates response if needed)
→ WhatsAppClient (sends response)
```

### Conversation Context
- Stored in-memory per sender (lost on restart)
- Configurable history length (default 10 messages)
- For production: implement persistent storage (database/Redis)

### Error Handling
- All major components have try/catch with logging
- Optional error notifications to users (configurable)
- Graceful degradation when AI provider is unavailable

### Security Considerations
- API keys stored in environment variables only
- Contact filtering with allowlist/blocklist support
- Rate limiting prevents abuse
- Be aware of WhatsApp ToS when choosing client implementation