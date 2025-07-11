from airdocs.utils import get_readme_content


def test_get_readme_content():
    content = get_readme_content()
    assert isinstance(content, str)
    assert len(content) > 0, "README content should not be empty"
