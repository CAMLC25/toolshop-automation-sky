"""User API tests."""
import pytest


# ---------------------------------------------------------------- B2.4b
@pytest.mark.api
def test_user_register_empty_body_returns_422_with_field_errors(api):
    """Goal: server-side validation for empty registration body.
    Precondition: none.
    Expected: 422 status and error lists for 'email' and 'password'."""
    response = api.post("/users/register", data={})
    assert response.status == 422, response.text()
    errors = response.json()
    assert "email" in errors and "password" in errors, errors


# ---------------------------------------------------------------- B2.5a
@pytest.mark.api
def test_user_profile_with_token_returns_own_email(api, auth_headers, test_user):
    """Goal: bearer token grants access to user profile.
    Precondition: user registered by fixture.
    Expected: 200 status and matching user email."""
    response = api.get("/users/me", headers=auth_headers)
    assert response.status == 200, response.text()
    assert response.json()["email"] == test_user["email"]
