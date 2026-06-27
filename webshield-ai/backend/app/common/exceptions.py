class WebShieldError(Exception):
    """Base exception for application-specific failures."""


class ValidationError(WebShieldError):
    """Raised when incoming payloads fail custom validation."""


class StorageError(WebShieldError):
    """Raised when persistence or file storage fails."""


class ProviderError(WebShieldError):
    """Raised when a model provider cannot return a prediction."""
