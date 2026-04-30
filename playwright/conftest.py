import pytest
from playwright.sync_api import Playwright, APIRequestContext


BASE_URL = "http://localhost:8080"


@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> APIRequestContext:
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context
    context.dispose()
