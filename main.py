#!/usr/bin/env python3

from mcp_server.server import mcp

if __name__ == "__main__":
    print("🚀 Starting JobHunt Email Intelligence MCP Server...")
    print("📧 Gmail integration ready")
    print("🔧 5 tools available for Claude Desktop:")
    print("   - classify_emails: Classify emails by job hunt categories")
    print("   - get_important_emails: Find urgent emails needing attention")
    print("   - update_job_tracker: Update job application statuses")
    print("   - generate_weekly_report: Create progress reports")
    print("   - extract_email_info: Analyze specific email content")
    print("✅ Ready for connection...")
    print()
    
    mcp.run(transport="stdio")
