#!/usr/bin/env python3
"""
WhatsApp AI Agent - Main Application
Entry point for the WhatsApp AI agent bot.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path

from bot import WhatsAppAIBot
from config.settings import load_config


def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/whatsapp_ai_agent.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logging.info(f"Received signal {signum}. Shutting down gracefully...")
    sys.exit(0)


async def main():
    """Main application entry point."""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Load configuration
    config = load_config()
    
    # Setup logging
    setup_logging(config.get('log_level', 'INFO'))
    
    logger = logging.getLogger(__name__)
    logger.info("Starting WhatsApp AI Agent...")
    
    try:
        # Initialize and start the bot
        bot = WhatsAppAIBot(config)
        await bot.start()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)


def main_sync():
    """Synchronous entry point for setuptools console_scripts."""
    asyncio.run(main())


if __name__ == "__main__":
    main_sync()
