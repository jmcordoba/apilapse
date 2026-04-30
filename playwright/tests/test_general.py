from playwright.sync_api import APIRequestContext


class TestGeneral:
    """Tests for 01 - General endpoints."""

    def test_hello(self, api_context: APIRequestContext):
        """01 Hello - GET /hello"""
        response = api_context.get("/hello")
        assert response.ok

    def test_status(self, api_context: APIRequestContext):
        """02 Status - GET /health/v1/status"""
        response = api_context.get("/health/v1/status")
        assert response.ok
