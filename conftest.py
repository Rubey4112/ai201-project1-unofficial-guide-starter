import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--show-chunks",
        action="store_true",
        default=False,
        help="Print each chunk's text content during chunk_document tests",
    )


@pytest.fixture
def show_chunks(request):
    return request.config.getoption("--show-chunks")
