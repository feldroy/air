"""AirForm: Display and Validation of HTML forms. Powered by pydantic.

Pro-tip: Always validate incoming data."""

from air.form.csrf import configure_csrf_secret as configure_csrf_secret
from air.form.main import (
    AirForm as AirForm,
    SafeHTML as SafeHTML,
    default_form_widget as default_form_widget,
    errors_to_dict as errors_to_dict,
    get_user_error_message as get_user_error_message,
    label_for_field as label_for_field,
    pydantic_type_to_html_type as pydantic_type_to_html_type,
    require_csrf as require_csrf,
)
from air.form.styles import default_css as default_css

__all__ = [
    "AirForm",
    "SafeHTML",
    "configure_csrf_secret",
    "default_css",
    "default_form_widget",
    "errors_to_dict",
    "get_user_error_message",
    "label_for_field",
    "pydantic_type_to_html_type",
    "require_csrf",
]
