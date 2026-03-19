"""Display and Validation of HTML forms. Powered by pydantic.

Re-exports from the airform package. AirForm validation, rendering,
and request handling all live in airform. Air adds nothing on top.

Pro-tip: Always validate incoming data."""

from airform import (
    AirForm as AirForm,
    default_form_widget as default_form_widget,
    errors_to_dict as errors_to_dict,
    get_user_error_message as get_user_error_message,
    label_for_field as label_for_field,
    pydantic_type_to_html_type as pydantic_type_to_html_type,
)
