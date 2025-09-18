#!/usr/bin/env python3
"""
Setup script for WhatsApp AI Agent
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements from requirements.txt
requirements = []
requirements_path = this_directory / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f.readlines() 
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="whatsapp-ai-agent",
    version="0.1.0",
    author="Chinedu Chukwuemeka Mazi",
    author_email="chinedumazigtv@gmail.com",
    description="AI-powered WhatsApp bot for automated message responses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chinedunewbirth/whatsapp-ai-agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.9.0",
            "flake8>=6.1.0",
            "mypy>=1.6.0",
        ],
        "web": [
            "selenium>=4.15.0",
        ],
        "database": [
            "sqlalchemy>=2.0.0",
            "aiosqlite>=0.19.0",
        ],
        "redis": [
            "redis>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "whatsapp-ai-agent=main:main_sync",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)