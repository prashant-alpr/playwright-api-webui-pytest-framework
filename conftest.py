import pytest
import os
from playwright.sync_api import Playwright, Browser
from config.config import Config
from api_endpoints.api_endpoints import APIEndpoints

@pytest.fixture(scope="session")
def shared_data():
    return {}

@pytest.fixture(scope="session")
def user_credentials():
    # Read variables injected by GitHub Actions OR local .env
    email = os.getenv("APP_EMAIL")
    password = os.getenv("APP_PASSWORD")
    if not email or not password:
        pytest.fail("Missing credentials! Ensure APP_EMAIL and APP_PASSWORD are set.")
    return {"email": email, "password": password}

@pytest.fixture(scope="session")
def browser_setup(playwright: Playwright, browser: Browser, shared_data, user_credentials):
    # Creating API Context
    api_context = playwright.request.new_context(base_url=Config.BASE_URL)
    # Login through API
    response = api_context.post(url=APIEndpoints.login_url,
                                headers={"Content-Type": "application/json"},
                                data={"userEmail":user_credentials.get("email"),"userPassword":user_credentials.get("password")})
    if not response.ok:
        raise ValueError(f"API Login failed [{response.status}]: {response.text()}")
    else:
        print(f"Json response: {response.json()}")
    # Capturing the token, userId from API Response Json
    token = response.json().get("token")
    shared_data["token"] = token
    user_id = response.json().get("userId")
    shared_data["user_id"] = user_id
    # Creating browser context
    context = browser.new_context()
    # Setting the localStorage with token, userId from API Response
    context.add_init_script(f"window.localStorage.setItem('token', '{token}');")
    context.add_init_script(f"window.localStorage.setItem('userId', '{user_id}');")
    page = context.new_page()
    yield page, api_context
    context.close()
    browser.close()
    api_context.dispose()


