from air.utils import compute_page_path


def test_compute_page_path_returns_root_for_index_endpoint() -> None:
    actual_path = compute_page_path(endpoint_name="index")
    assert actual_path == "/"


def test_compute_page_path_handles_multiple_underscores() -> None:
    actual_path = compute_page_path(endpoint_name="user_profile_settings")
    assert actual_path == "/user-profile-settings"


def test_compute_page_path_handles_single_word_endpoint() -> None:
    actual_path = compute_page_path(endpoint_name="home")
    assert actual_path == "/home"


def test_compute_page_path_with_forward_slash_separator() -> None:
    actual_path = compute_page_path(endpoint_name="api_users", separator="/")
    assert actual_path == "/api/users"


def test_compute_page_path_handles_empty_string() -> None:
    actual_path = compute_page_path(endpoint_name="")
    assert actual_path == "/"
