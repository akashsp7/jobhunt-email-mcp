from mcp.server.fastmcp import FastMCP
from .tools.email_tools import EmailTools

mcp = FastMCP("JobHunt Email Intelligence")

email_tools = EmailTools()

@mcp.tool()
def classify_emails(count: int = 50, tags: list[str] = None) -> dict:
    """
    Classify recent emails into categories for job hunting.
    
    Args:
        count: Number of recent emails to classify (default: 50)
        tags: Custom classification tags (default: ["Positive", "Rejection", "Applied-Confirmation", "Spam"])
    
    Returns:
        Dictionary with classification results and email counts
    """
    if tags is None:
        tags = ["Positive", "Rejection", "Applied-Confirmation", "Spam"]
    
    return email_tools.classify_emails(count=count, tags=tags)

@mcp.tool()
def get_important_emails(days: int = 3) -> dict:
    """
    Get important/urgent emails from recent days that need attention.
    
    Args:
        days: Number of days to look back (default: 3)
    
    Returns:
        Dictionary with important emails and their importance scores
    """
    return email_tools.get_important_emails(days=days)

@mcp.tool()
def update_job_tracker() -> dict:
    """
    Update job application tracking based on recent emails.
    Automatically updates application statuses based on email content.
    
    Returns:
        Dictionary with updated job applications and status changes
    """
    return email_tools.update_job_tracker()

@mcp.tool()
def generate_weekly_report() -> dict:
    """
    Generate a comprehensive weekly job hunting progress report.
    Includes application stats, response rates, and recommendations.
    
    Returns:
        Dictionary with weekly progress summary and statistics
    """
    return email_tools.generate_weekly_report()

@mcp.tool()
def extract_email_info(email_id: str) -> dict:
    """
    Extract detailed information from a specific email.
    Analyzes content for company name, position, classification, and importance.
    
    Args:
        email_id: Gmail message ID of the email to analyze
    
    Returns:
        Dictionary with extracted email information and analysis
    """
    return email_tools.extract_email_info(email_id=email_id)

if __name__ == "__main__":
    print("🚀 JobHunt Email Intelligence MCP Server")
    print("📧 5 email intelligence tools available")
    print("✅ Ready for Claude Desktop connection")
    mcp.run(transport="stdio")
