#!/usr/bin/env python3

import os
import sys

def check_requirements():
    required_files = [
        'gmail_api.py',
        'main.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    credentials_found = False
    for file in os.listdir('.'):
        if file.startswith('client_secret_') and file.endswith('.json'):
            credentials_found = True
            break
    
    if not credentials_found:
        print("❌ No Google credentials file found")
        return False
    
    print("✅ All required files present")
    return True

def test_imports():
    try:
        from gmail_api import GmailAPI
        from main import JobHuntMCPServer
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_basic_test():
    try:
        from test_gmail import test_gmail_connection
        print("\n🔧 Testing Gmail connection...")
        success = test_gmail_connection()
        return success
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    print("🚀 JobHunt Email MCP Server - Quick Start")
    print("=" * 50)
    
    if not check_requirements():
        sys.exit(1)
    
    if not test_imports():
        print("\n💡 Try: pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n🔧 Running basic connectivity test...")
    if run_basic_test():
        print("\n✅ Setup complete! Ready to launch MCP server")
        print("\n🚀 To start the server: python main.py")
    else:
        print("\n❌ Setup incomplete. Check your Gmail API credentials.")

if __name__ == "__main__":
    main()
