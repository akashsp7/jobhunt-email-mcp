import os

# Gmail API Configuration
GMAIL_CREDENTIALS_FILE = os.getenv(
    'GMAIL_CREDENTIALS_FILE', 
    'client_secret_530571396736-jh5id4kn03ej7s1m5krca8di91m0iua4.apps.googleusercontent.com.json'
)

GMAIL_TOKEN_FILE = os.getenv('GMAIL_TOKEN_FILE', 'token.pickle')

# Database Configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', 'jobhunt.db')

# MCP Server Configuration
MCP_SERVER_NAME = "jobhunt-email"
MCP_SERVER_VERSION = "1.0.0"

# Email Classification Settings
DEFAULT_EMAIL_COUNT = 50
DEFAULT_LOOKBACK_DAYS = 7
IMPORTANCE_THRESHOLD = 7

# Job Application Tracking
DEFAULT_TAGS = ["Positive", "Rejection", "Applied-Confirmation", "Spam"]

# AI Integration (for future use)
LLAMA_API_ENDPOINT = os.getenv('LLAMA_API_ENDPOINT', '')
NEBIUS_API_KEY = os.getenv('NEBIUS_API_KEY', '')
HYPERBOLIC_API_KEY = os.getenv('HYPERBOLIC_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
