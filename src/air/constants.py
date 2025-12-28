"""Air framework constants shared across modules."""

from importlib.metadata import version as get_version

# Version
AIR_VERSION = get_version("air")

# OpenAPI documentation URL defaults
DEFAULT_SWAGGER_URL = "/_swagger"
DEFAULT_REDOC_URL = "/_redoc"
