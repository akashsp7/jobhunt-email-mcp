# JobHunt Email Intelligence - MCP Server Setup Guide

## 🎯 What This Does
Transform Claude Desktop into your job hunting command center with direct Gmail integration. Automatically classify emails, track applications, and get intelligent insights.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /path/to/project
pip install -r requirements.txt
```

### 2. Gmail Authentication Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json` to project root
6. Run once for initial auth: `python -c "from mcp_server.core import GmailClient; GmailClient()"`

### 3. Test MCP Server
```bash
python test_mcp_server.py
```
You should see "MCP Server test completed successfully!"

### 4. Configure Claude Desktop

#### For macOS:
Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

#### For Windows:
Edit: `%APPDATA%/Claude/claude_desktop_config.json`

#### For Linux:
Edit: `~/.config/claude/claude_desktop_config.json`

Add this configuration:
```json
{
  "mcpServers": {
    "jobhunt-email-intelligence": {
      "command": "python3",
      "args": ["/FULL/PATH/TO/YOUR/PROJECT/main.py"],
      "env": {
        "PATH": "/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

**Important**: Replace `/FULL/PATH/TO/YOUR/PROJECT/` with your actual project path!

### 5. Restart Claude Desktop
Close and reopen Claude Desktop. You should see the 🔧 tool icon appear.

## 📧 Usage Examples

Once connected, you can ask Claude:

### Email Classification
> "Claude, classify my last 50 emails into job hunting categories"

### Important Email Check  
> "Any important emails from the last 3 days I should know about?"

### Job Tracker Update
> "Update my job application tracker based on recent emails"

### Weekly Progress Report
> "Generate my weekly job hunting report"

### Email Analysis
> "Analyze email ID abc123xyz for company and position details"

## 🔧 Available Tools

1. **classify_emails**: Sort emails by Positive, Rejection, Applied-Confirmation, Spam
2. **get_important_emails**: Find urgent emails needing immediate attention  
3. **update_job_tracker**: Auto-update job application statuses from emails
4. **generate_weekly_report**: Create comprehensive progress reports
5. **extract_email_info**: Extract company, position, and other details from specific emails

## 🐛 Troubleshooting

### "Gmail authentication failed"
- Ensure `credentials.json` is in project root
- Run initial authentication: `python -c "from mcp_server.core import GmailClient; GmailClient()"`
- Check that Gmail API is enabled in Google Cloud Console

### "Connection failed" in Claude Desktop
- Verify the path in `claude_desktop_config.json` is absolute and correct
- Check that `python` command works from terminal
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### "Tool not found"
- Restart Claude Desktop after configuration changes
- Check that the 🔧 icon appears in Claude Desktop interface
- Test with: `python test_mcp_server.py`

## 📝 Development Notes

- Server runs via stdio transport (stdin/stdout)
- All email data processed locally for privacy
- Gmail OAuth tokens stored in `token.pickle`
- Database stored in `emails.db` (SQLite)

## 🛡️ Privacy & Security

- All processing happens locally on your machine
- No email data sent to external servers (except Gmail API)
- OAuth tokens encrypted and stored locally
- Database contains only metadata and classifications

---

**Need help?** Check the troubleshooting section or test with `python test_mcp_server.py`
