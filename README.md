# JobHunt Email Intelligence - MCP Server

**mcp-server-track**

## 🎯 Project Overview
An MCP server that transforms Claude Desktop into a job hunting command center with direct email integration capabilities. Intelligently classifies job-related emails, tracks applications, and provides actionable insights.

## ✨ Features
- **Smart Email Classification**: Positive, Rejection, Applied-Confirmation, Spam
- **Priority Email Detection**: Identifies urgent job-related communications  
- **Job Application Tracking**: Auto-updates application statuses from emails
- **Weekly Progress Reports**: Analytics and recommendations for job hunt optimization
- **Information Extraction**: Parses company names, positions, and key details

## 🚀 Quick Start

### 1. Installation
```bash
git clone [repository]
cd jobhunt-email-mcp
pip install -r requirements.txt
```

### 2. Gmail Setup
1. Enable Gmail API in Google Cloud Console
2. Download OAuth credentials as `client_secret_*.json`
3. Run authentication flow on first use

### 3. Run MCP Server
```bash
python main.py
```

### 4. Test Components (Optional)
```bash
python test_components.py
```

### 5. Web Interface (Optional)
```bash
python gradio_interface.py
```

## 🔧 Claude Desktop Integration

### MCP Configuration
Add to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "jobhunt-email": {
      "command": "python",
      "args": ["/path/to/jobhunt-email-mcp/main.py"],
      "env": {}
    }
  }
}
```

### Available Tools in Claude
1. **classify_emails** - Classify recent emails by category
2. **get_important_emails** - Find urgent job-related emails
3. **update_job_tracker** - Update application status tracking
4. **generate_weekly_report** - Create progress analytics
5. **extract_email_info** - Parse specific email details

## 📂 Project Structure
```
mcp_server/
├── core/                    # Core business logic
│   ├── gmail_client.py     # Gmail API integration
│   ├── email_classifier.py # Email classification logic
│   ├── storage.py          # Database operations
│   └── job_tracker.py      # Job application tracking
├── tools/                   # MCP tool definitions
│   ├── email_tools.py      # Tool implementations
│   └── schemas.py          # JSON schemas for tools
├── server.py               # Main MCP server
└── config.py               # Configuration settings

backup/                      # Original files
├── main_original.py        # Original monolithic implementation
└── gmail_api_original.py   # Original Gmail integration

main.py                     # MCP server entry point
gradio_interface.py         # Web testing interface
test_components.py          # Component validation
requirements.txt            # Dependencies
```

## 💡 Usage Examples with Claude

### Email Classification
```
Claude, please classify my last 100 emails into job hunting categories
```

### Priority Check
```
Claude, any important emails from the last 3 days?
```

### Progress Tracking
```
Claude, update my job tracker and show me this week's progress
```

## 🔧 Technical Details

### Technology Stack
- **MCP Protocol**: Model Context Protocol for Claude integration
- **Gmail API**: OAuth 2.0 authentication and email access
- **SQLite**: Persistent storage for classifications and tracking
- **Python**: Core implementation with asyncio for MCP server

### Database Schema
- **emails**: id, subject, sender, date, classification, importance, content
- **job_applications**: company, position, status, dates, email references

### Classification Logic
- **Positive**: Interview invites, offers, next round notifications
- **Rejection**: Auto-rejections and decline notifications  
- **Applied-Confirmation**: Application received confirmations
- **Spam**: Marketing emails and irrelevant content

## 🚧 Development Status
- ✅ Core MCP server implementation
- ✅ Gmail API integration working
- ✅ Email classification system
- ✅ Job tracking functionality
- ✅ Database persistence
- 🔄 Llama 3.2 AI integration (planned)
- 🔄 Advanced extraction features (planned)

## 📊 Next Steps
1. Test Claude Desktop integration
2. Add Llama 3.2 for improved classification
3. Enhance information extraction
4. Deploy to Hugging Face Spaces
5. Create demo video

## 🐛 Troubleshooting

### Gmail Authentication Issues
```bash
rm token.pickle
python test_components.py
```

### MCP Connection Problems
- Check Claude Desktop MCP configuration
- Verify main.py path is absolute
- Check for port conflicts

### Database Issues
```bash
rm jobhunt.db
python test_components.py
```

## 🏆 Hackathon Submission
- **Track**: MCP Server/Tool Track
- **Demo**: Coming soon
- **Deploy**: Hugging Face Spaces ready
- **Status**: Core functionality complete

---

**Built for Agents & MCP Hackathon (June 2-10, 2025)**
