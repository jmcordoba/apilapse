from playwright.sync_api import APIRequestContext


class TestRequests:
    """Tests for Requests endpoints."""

    request_uuid: str = ""

    def test_create_request(self, api_context: APIRequestContext):
        """Create Request - POST /requests/v1/request"""
        response = api_context.post(
            "/requests/v1/request",
            data={
                "active": False,
                "periodicity": "daily",
                "name": "test",
                "url": "https://www.juanmacordoba.com/as",
                "method": "GET",
                "headers": "",
                "user_agent": "",
                "authentication": "None",
                "credentials": "blablabla",
                "body": "",
                "tags": "juanmacordoba",
            },
        )
        assert response.status == 201
        body = response.json()
        assert "request_uuid" in body
        TestRequests.request_uuid = body["request_uuid"]

    def test_update_request(self, api_context: APIRequestContext):
        """Update Request - PUT /requests/v1/request/:id"""
        response = api_context.put(
            f"/requests/v1/request/{TestRequests.request_uuid}",
            data={
                "active": True,
                "periodicity": "daily",
                "name": "test",
                "url": "https://www.juanmacordoba.com/as",
                "method": "POST",
                "headers": "",
                "user_agent": "",
                "authentication": "None",
                "credentials": "blibuyyulibli",
                "body": "",
                "tags": "juanmacordobaaaa",
            },
        )
        assert response.ok

    def test_get_request_by_id(self, api_context: APIRequestContext):
        """Request by Id - GET /requests/v1/request/:id"""
        response = api_context.get(
            f"/requests/v1/request/{TestRequests.request_uuid}"
        )
        assert response.ok

    def test_get_all_requests(self, api_context: APIRequestContext):
        """All Requests - GET /requests/v1/all"""
        response = api_context.get("/requests/v1/all")
        assert response.ok

    def test_delete_request_by_id(self, api_context: APIRequestContext):
        """Delete by Id - DELETE /requests/v1/request/:id"""
        response = api_context.delete(
            f"/requests/v1/request/{TestRequests.request_uuid}"
        )
        assert response.ok
