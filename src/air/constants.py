"""Shared constants used across multiple Air modules.

Module-specific constants (like DEFAULT_TAGS in applications.py
or LOG_CONFIG in cli.py) are kept with their consumers for locality.
"""

from importlib.metadata import version as get_version

# Version
AIR_VERSION = get_version("air")

# Configuration defaults
DEFAULT_TITLE = "Air"
DEFAULT_SWAGGER_URL = "/_swagger"
DEFAULT_REDOC_URL = "/_redoc"

# Brand voice
ATTRIBUTION = "Crafted with care by Two Scoops authors pydanny and audreyfeldroy"
