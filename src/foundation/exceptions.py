class DigitalFTEError(Exception):
    """Base exception for the agent."""
    pass

class TransientError(DigitalFTEError):
    """Temporary failure (Network, Lock). Retry allowed."""
    pass

class ConfigurationError(DigitalFTEError):
    """Fatal setup error. Stop immediately."""
    pass

class SafetyError(DigitalFTEError):
    """Agent attempted a forbidden action."""
    pass
