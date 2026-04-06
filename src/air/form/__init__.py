"""AirForm: Display and Validation of HTML forms. Powered by pydantic.

Pro-tip: Always validate incoming data."""

from air.form.main import (
    AirForm as AirForm,
    SafeHTML as SafeHTML,
    default_form_widget as default_form_widget,
    errors_to_dict as errors_to_dict,
    get_user_error_message as get_user_error_message,
    label_for_field as label_for_field,
    pydantic_type_to_html_type as pydantic_type_to_html_type,
)
from air.form.styles import default_css as default_css

__all__ = [
    "AirForm",
    "SafeHTML",
    "default_css",
    "default_form_widget",
    "errors_to_dict",
    "get_user_error_message",
    "label_for_field",
    "pydantic_type_to_html_type",
]
