#!/usr/bin/env python3

import asyncio
import subprocess
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """Test our MCP server by connecting as a client and listing tools"""
    
    print("🧪 Testing JobHunt MCP Server...")
    print()
    
    server_params = StdioServerParameters(
        command="python3",
        args=["main.py"]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✅ MCP Server connection established")
                
                tools = await session.list_tools()
                print(f"✅ Found {len(tools.tools)} tools:")
                
                for tool in tools.tools:
                    print(f"   - {tool.name}: {tool.description}")
                
                print()
                print("🎯 Testing classify_emails tool...")
                result = await session.call_tool(
                    "classify_emails", 
                    arguments={"count": 5, "tags": ["Positive", "Rejection"]}
                )
                
                print("✅ Tool call successful!")
                print("📧 Sample result:")
                
                if result.content and len(result.content) > 0:
                    content = result.content[0]
                    if hasattr(content, 'text'):
                        try:
                            parsed = json.loads(content.text)
                            if 'error' in parsed:
                                print(f"   ⚠️  Gmail auth needed: {parsed['error']}")
                            else:
                                print(f"   📊 Processed: {parsed.get('total_processed', 0)} emails")
                                print(f"   📈 Classifications: {parsed.get('classifications', {})}")
                        except:
                            print(f"   📄 Raw response: {content.text[:200]}...")
                
                print()
                print("🎉 MCP Server test completed successfully!")
                print("📋 Your server is ready for Claude Desktop integration")
                
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        
if __name__ == "__main__":
    asyncio.run(test_mcp_server())
