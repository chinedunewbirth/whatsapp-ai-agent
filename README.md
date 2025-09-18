# WhatsApp AI Agent 🤖💬

An intelligent WhatsApp bot that uses AI to automatically respond to messages. Built with Python and supports multiple AI providers including OpenAI GPT, Anthropic Claude, and local models.

## ✨ Features

- **AI-Powered Responses**: Intelligent message processing using state-of-the-art AI models
- **Multiple AI Providers**: Support for OpenAI GPT, Anthropic Claude, and local models
- **WhatsApp Integration**: Multiple connection methods (WhatsApp Web, Business API, unofficial clients)
- **Smart Message Handling**: Rate limiting, contact filtering, command processing
- **Group Support**: Configurable group message handling with mention detection
- **Conversation Memory**: Maintains conversation context for natural interactions
- **Extensible Architecture**: Modular design for easy customization and extension

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- WhatsApp account
- AI provider API key (OpenAI, Anthropic, or local model setup)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/chinedunewbirth/whatsapp-ai-agent.git
   cd whatsapp-ai-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\\Scripts\\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration**
   ```bash
   # Create configuration from template
   python src/config/settings.py
   
   # Copy and edit the configuration file
   cp config.yaml.example config.yaml
   # Edit config.yaml with your settings
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

### Configuration

Edit `config.yaml` or set environment variables:

#### Required Settings

```yaml
ai:
  provider: "openai"  # Options: openai, anthropic, local
  api_key: "your_openai_api_key_here"
  model: "gpt-3.5-turbo"

whatsapp:
  client_type: "web"  # Options: web, business_api, unofficial
```

#### Environment Variables

```bash
# AI Configuration
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
AI_MODEL=gpt-3.5-turbo

# WhatsApp Configuration  
WHATSAPP_CLIENT_TYPE=web

# Bot Behavior
RESPOND_TO_GROUPS=false
RATE_LIMIT_ENABLED=true
MAX_MESSAGES_PER_HOUR=30
```

### Running the Bot

```bash
# Run the bot
python src/main.py

# Or if installed as package
whatsapp-ai-agent
```

## 📚 Documentation

### Project Structure

```
whatsapp-ai-agent/
├── src/
│   ├── main.py              # Main application entry point
│   ├── bot.py               # Core bot logic
│   ├── ai_processor.py      # AI response generation
│   ├── message_handler.py   # Message processing and filtering
│   ├── whatsapp_client.py   # WhatsApp connection interface
│   └── config/
│       └── settings.py      # Configuration management
├── config/                  # Configuration files
├── docs/                    # Additional documentation
├── tests/                   # Unit tests
├── logs/                    # Log files
├── requirements.txt         # Python dependencies
├── config.yaml             # Main configuration file
├── .env                    # Environment variables
└── README.md               # This file
```

### Configuration Options

#### AI Settings

- `provider`: AI provider to use (`openai`, `anthropic`, `local`)
- `model`: AI model name (e.g., `gpt-3.5-turbo`, `claude-3-sonnet`)
- `api_key`: API key for the chosen provider
- `max_tokens`: Maximum tokens in AI response
- `temperature`: Response creativity (0.0-1.0)
- `system_prompt`: System prompt to guide AI behavior

#### WhatsApp Settings

- `client_type`: Connection method (`web`, `business_api`, `unofficial`)
- `session_path`: Path to store WhatsApp session data
- `business_api_token`: Token for WhatsApp Business API
- `phone_number_id`: Phone number ID for Business API

#### Message Handling

- `respond_to_groups`: Enable/disable group message responses
- `require_mention_in_groups`: Require bot mention in groups
- `rate_limit_enabled`: Enable rate limiting per contact
- `max_messages_per_hour`: Maximum messages per contact per hour
- `allowed_contacts`: Whitelist of allowed contacts (empty = all allowed)
- `blocked_contacts`: List of blocked contacts

### Commands

The bot supports these built-in commands:

- `help` - Show help message with available commands
- `status` - Check bot status
- `clear` - Clear conversation history
- `stop` - Stop responding to messages
- `start` - Resume responding to messages

### WhatsApp Integration Options

#### 1. WhatsApp Web (Recommended for development)

Uses browser automation to connect to WhatsApp Web.

```yaml
whatsapp:
  client_type: "web"
  session_path: "./session"
```

#### 2. WhatsApp Business API (Recommended for production)

Official WhatsApp Business API integration.

```yaml
whatsapp:
  client_type: "business_api"
  business_api_token: "your_business_api_token"
  phone_number_id: "your_phone_number_id"
```

#### 3. Unofficial Clients

Third-party WhatsApp clients (use at your own risk).

```yaml
whatsapp:
  client_type: "unofficial"
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=src

# Run specific test file
pytest tests/test_message_handler.py
```

## 🔧 Development

### Setting up Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Set up pre-commit hooks
pre-commit install

# Run code formatting
black src/
flake8 src/

# Type checking
mypy src/
```

### Adding New AI Providers

1. Implement the provider in `ai_processor.py`
2. Add configuration options in `settings.py`
3. Update the README with setup instructions

### Adding New WhatsApp Clients

1. Implement the client interface in `whatsapp_client.py`
2. Add client-specific configuration options
3. Test thoroughly before production use

## 🚨 Important Notes

### Security

- Keep your API keys secure and never commit them to version control
- Use environment variables or secure configuration files
- Consider implementing webhook authentication for Business API
- Be cautious with unofficial WhatsApp clients (potential ToS violations)

### Rate Limiting

- WhatsApp has rate limits - respect them to avoid account suspension
- The bot includes built-in rate limiting per contact
- Monitor your usage and adjust limits accordingly

### Legal Considerations

- Ensure compliance with WhatsApp's Terms of Service
- Consider privacy implications when storing conversation data
- Implement appropriate data retention policies
- Be transparent with users about bot automation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/whatsapp-ai-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/whatsapp-ai-agent/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/whatsapp-ai-agent/wiki)

## 🙏 Acknowledgments

- OpenAI for their excellent GPT models
- Anthropic for Claude AI
- The WhatsApp Web.js community
- All contributors and supporters of this project

## ⚠️ Disclaimer

This bot is for educational and development purposes. Use responsibly and in accordance with WhatsApp's Terms of Service. The developers are not responsible for any misuse or violations of platform policies.

---

**Made with ❤️ for the open source community**