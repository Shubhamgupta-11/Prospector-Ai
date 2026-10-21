#!/usr/bin/env python3
"""
Quick setup validator for Prospector AI
Run this to check if everything is configured correctly
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print("✅ Python version OK:", f"{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("❌ Python version too old:", f"{version.major}.{version.minor}.{version.micro}")
        print("   Need Python 3.10 or higher")
        return False

def check_dependencies():
    """Check if key dependencies are installed"""
    required = [
        'fastapi',
        'uvicorn', 
        'streamlit',
        'langchain',
        'langchain_openai',
        'bs4',
        'aiohttp',
        'tavily',
        'pydantic',
        'dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            if package == 'bs4':
                __import__('bs4')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} packages. Install with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has keys"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("   Copy .env.example to .env and add your API keys")
        return False
    
    print("✅ .env file exists")
    
    # Check if API keys are configured
    with open(env_path) as f:
        content = f.read()
    
    has_openai = 'OPENAI_API_KEY=' in content
    has_tavily = 'TAVILY_API_KEY=' in content
    
    # Check if they're not just placeholders
    openai_configured = has_openai and 'your_' not in content.split('OPENAI_API_KEY=')[1].split('\n')[0]
    tavily_configured = has_tavily and 'your_' not in content.split('TAVILY_API_KEY=')[1].split('\n')[0]
    
    if openai_configured:
        print("✅ OPENAI_API_KEY configured")
    else:
        print("⚠️  OPENAI_API_KEY not configured (REQUIRED)")
        print("   Get one from: https://platform.openai.com/api-keys")
    
    if tavily_configured:
        print("✅ TAVILY_API_KEY configured")
    else:
        print("⚠️  TAVILY_API_KEY not configured (optional but recommended)")
        print("   Get one from: https://tavily.com")
    
    return openai_configured

def check_project_structure():
    """Check if all required files exist"""
    required_files = [
        'app/main.py',
        'app/agents/research_agent.py',
        'app/api/research.py',
        'app/models/research.py',
        'app/scrapers/web_scraper.py',
        'frontend/app.py',
        'requirements.txt',
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("🔍 PROSPECTOR AI - SETUP VALIDATOR")
    print("=" * 60)
    print()
    
    print("📌 Checking Python version...")
    python_ok = check_python_version()
    print()
    
    print("📦 Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    print("🔑 Checking environment configuration...")
    env_ok = check_env_file()
    print()
    
    print("📁 Checking project structure...")
    structure_ok = check_project_structure()
    print()
    
    print("=" * 60)
    if python_ok and deps_ok and env_ok and structure_ok:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("🚀 You're ready to start:")
        print("   1. Run: uvicorn app.main:app --reload")
        print("   2. Run: streamlit run frontend/app.py")
        print("   3. Open: http://localhost:8501")
        print()
        print("Or just double-click:")
        print("   - start_backend.bat")
        print("   - start_frontend.bat")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print()
        print("Fix the issues above, then run this script again:")
        print("   python check_setup.py")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
