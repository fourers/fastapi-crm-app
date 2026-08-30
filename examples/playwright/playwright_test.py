import os

from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()
app_endpoint = os.environ["CLICK_CLI_APP_ENDPOINT"].rstrip("/")


def test_login_and_homepage(page: Page):
    page.goto(f"{app_endpoint}/login")

    expect(page.get_by_role("main")).to_match_aria_snapshot(
        '- heading "Welcome" [level=1]\n- paragraph: Sign in to continue\n- link "Login":\n  - /url: /auth/login'
    )
    page.get_by_role("link", name="Login").click()

    page.get_by_role("textbox", name="Username").fill("admin")
    page.get_by_role("textbox", name="Password").fill("password")
    page.get_by_role("button", name="Sign In").click()

    expect(page).to_have_url(f"{app_endpoint}/")
    expect(page.get_by_role("main")).to_match_aria_snapshot(
        '- main:\n  - heading "You are logged in" [level=1]\n  - link "Clients":\n    - /url: /clients\n  - link "Users":\n    - /url: /users\n  - link "Groups":\n    - /url: /groups'
    )

    page.get_by_role("button", name="Logout").click()
    expect(page).to_have_url(f"{app_endpoint}/login")
