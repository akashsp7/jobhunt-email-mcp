EMAIL_CLASSIFICATION_SCHEMA = {
    "name": "classify_emails",
    "description": "Classify recent emails into categories for job hunting",
    "inputSchema": {
        "type": "object",
        "properties": {
            "count": {
                "type": "integer",
                "description": "Number of recent emails to classify",
                "default": 50
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Classification tags to use",
                "default": ["Positive", "Rejection", "Applied-Confirmation", "Spam"]
            }
        }
    }
}

IMPORTANT_EMAILS_SCHEMA = {
    "name": "get_important_emails",
    "description": "Get important emails from recent days based on content analysis",
    "inputSchema": {
        "type": "object",
        "properties": {
            "days": {
                "type": "integer",
                "description": "Number of days to look back",
                "default": 3
            }
        }
    }
}

JOB_TRACKER_SCHEMA = {
    "name": "update_job_tracker",
    "description": "Update job application tracker based on recent emails",
    "inputSchema": {
        "type": "object",
        "properties": {}
    }
}

WEEKLY_REPORT_SCHEMA = {
    "name": "generate_weekly_report",
    "description": "Generate a weekly job hunting progress report",
    "inputSchema": {
        "type": "object",
        "properties": {}
    }
}

EMAIL_INFO_SCHEMA = {
    "name": "extract_email_info",
    "description": "Extract structured information from a specific email",
    "inputSchema": {
        "type": "object",
        "properties": {
            "email_id": {
                "type": "string",
                "description": "Gmail message ID to extract info from"
            }
        },
        "required": ["email_id"]
    }
}

TOOL_SCHEMAS = [
    EMAIL_CLASSIFICATION_SCHEMA,
    IMPORTANT_EMAILS_SCHEMA,
    JOB_TRACKER_SCHEMA,
    WEEKLY_REPORT_SCHEMA,
    EMAIL_INFO_SCHEMA
]
