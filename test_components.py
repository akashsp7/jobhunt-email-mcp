#!/usr/bin/env python3
"""
Test script for JobHunt Email Intelligence MCP Server
Quick validation that all components work
"""

import sys
import traceback
from mcp_server.core import GmailClient, EmailClassifier, EmailStorage, JobTracker

def test_components():
    """Test individual components"""
    print("🧪 Testing JobHunt MCP Server Components...")
    
    try:
        # Test Storage
        print("📁 Testing EmailStorage...")
        storage = EmailStorage()
        print("✅ EmailStorage initialized")
        
        # Test Classifier
        print("🔍 Testing EmailClassifier...")
        classifier = EmailClassifier()
        test_email = {
            "subject": "Interview invitation from Google",
            "body": "We'd like to schedule an interview",
            "from": "recruiter@google.com"
        }
        classification = classifier.classify_single_email(test_email)
        print(f"✅ EmailClassifier working - classified as: {classification}")
        
        # Test Job Tracker
        print("📊 Testing JobTracker...")
        job_tracker = JobTracker(storage, classifier)
        print("✅ JobTracker initialized")
        
        # Test Gmail Client (will require auth)
        print("📧 Testing GmailClient (may require authentication)...")
        try:
            gmail_client = GmailClient()
            print("✅ GmailClient authentication successful")
        except Exception as e:
            print(f"⚠️  GmailClient auth needed: {e}")
        
        print("\n🎉 All core components working!")
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        traceback.print_exc()
        return False

def test_mcp_tools():
    """Test MCP tools integration"""
    print("\n🔧 Testing MCP Tools...")
    
    try:
        from mcp_server.tools import EmailTools, TOOL_SCHEMAS
        
        print(f"📋 Found {len(TOOL_SCHEMAS)} tool schemas")
        for schema in TOOL_SCHEMAS:
            print(f"   - {schema['name']}: {schema['description']}")
        
        email_tools = EmailTools()
        print("✅ EmailTools initialized")
        
        print("\n🎉 MCP Tools ready!")
        return True
        
    except Exception as e:
        print(f"❌ MCP Tools test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 JobHunt Email Intelligence - Component Tests\n")
    
    components_ok = test_components()
    tools_ok = test_mcp_tools()
    
    if components_ok and tools_ok:
        print("\n✨ All tests passed! Ready to run MCP server.")
        print("Next step: python main.py")
    else:
        print("\n💥 Some tests failed. Check errors above.")
        sys.exit(1)
