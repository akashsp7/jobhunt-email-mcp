from .server import mcp
from .tools import EmailTools
from .core import GmailClient, EmailClassifier, EmailStorage, JobTracker
from . import config

__all__ = [
    'mcp',
    'EmailTools', 
    'GmailClient', 
    'EmailClassifier', 
    'EmailStorage', 
    'JobTracker',
    'config'
]

__version__ = "1.0.0"
