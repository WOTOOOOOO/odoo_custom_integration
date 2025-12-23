import os

class Config:
    """
    Central configuration for the RS.ge Integration module.
    Reads from environment variables with sensible defaults.
    """
    
    # RS.ge API Configuration
    RS_GE_BASE_URL = os.getenv('RS_GE_BASE_URL', 'http://localhost:8000')
    RS_GE_TIMEOUT = int(os.getenv('RS_GE_TIMEOUT', '10'))
    
    # Signing Configuration
    # In a real app, this might be a path to a certificate file
    RS_GE_SIGNING_KEY = os.getenv('RS_GE_SIGNING_KEY', 'mock_key')

    # Feature Flags
    RS_GE_ENABLE_LOGGING = os.getenv('RS_GE_ENABLE_LOGGING', 'True').lower() == 'true'
