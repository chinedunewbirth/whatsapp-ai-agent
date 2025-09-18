#!/usr/bin/env python3
"""
Command-line interface for WhatsApp AI Agent
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """CLI entry point for whatsapp-ai-agent command."""
    from src.main import main_sync
    main_sync()

if __name__ == "__main__":
    main()