from playwright.sync_api import APIRequestContext


class TestIdentityProvider:
    """Tests for Identity Provider endpoints."""

    def test_sign_in(self, api_context: APIRequestContext):
        """Sign In - POST /ip/v1/signin"""
        response = api_context.post(
            "/ip/v1/signin",
            data={
                "name": "Juanma10",
                "email": "jmcordoba@gmail.com",
                "password": "Aa12345678.",
                "password2": "Aa12345678.",
            },
        )
        assert response.status == 201
        body = response.json()
        assert "token" in body
        assert "email" in body
        assert "user_uuid" in body

    # def test_login(self, api_context: APIRequestContext):
    #     """Login - POST /ip/v1/login"""
    #     response = api_context.post(
    #         "/ip/v1/login",
    #         form={
    #             "email": "jmcordoba@gmail.com",
    #             "password": "Aa12345678.",
    #         },
    #     )
    #     assert response.ok

    def test_logout(self, api_context: APIRequestContext):
        """Logout - POST /ip/v1/logout"""
        response = api_context.post(
            "/ip/v1/logout",
            form={
                "email": "jmcordoba@gmail.com",
                "password": "Aa12345678.",
            },
        )
        assert response.ok

    # def test_change_password(self, api_context: APIRequestContext):
    #     """Change Password - POST /ip/v1/change_password"""
    #     response = api_context.post(
    #         "/ip/v1/change_password",
    #         data={
    #             "current_password": "hola_caracola.100",
    #             "new_password": "Hola_caracola.100",
    #             "new_password2": "Hola_caracola.100",
    #         },
    #     )
    #     assert response.status == 200
    #     body = response.json()
    #     assert "user_uuid" in body

    # def test_validate_token(self, api_context: APIRequestContext):
    #     """Validate Token - GET /ip/v1/validate"""
    #     response = api_context.get(
    #         "/ip/v1/validate",
    #         params={
    #             "uuid": "test-uuid",
    #             "token": "test-token",
    #         },
    #     )
    #     assert response.status == 200
    #     body = response.json()
    #     assert "user_uuid" in body

    def test_get_all_users(self, api_context: APIRequestContext):
        """All Users - GET /ip/v1/users"""
        response = api_context.get("/ip/v1/users")
        assert response.ok

    def test_get_user_by_id(self, api_context: APIRequestContext):
        """User by Id - GET /ip/v1/user/:id"""
        response = api_context.get("/ip/v1/user/1")
        assert response.ok

    # def test_get_me(self, api_context: APIRequestContext):
    #     """Me - GET /ip/v1/me"""
    #     response = api_context.get("/ip/v1/me")
    #     assert response.ok

    def test_delete_me(self, api_context: APIRequestContext):
        """Me - DELETE /ip/v1/me"""
        response = api_context.delete("/ip/v1/me")
        assert response.ok

    # def test_delete_user_by_id(self, api_context: APIRequestContext):
    #     """User by Id - DELETE /ip/v1/user/:id"""
    #     response = api_context.delete("/ip/v1/user/1")
    #     assert response.ok

    # def test_delete_all_users(self, api_context: APIRequestContext):
    #     """All Users - DELETE /ip/v1/users"""
    #     response = api_context.delete("/ip/v1/users")
    #     assert response.status == 400
    #     body = response.json()
    #     assert "message" in body
