from playwright.sync_api import Page, expect


def test_login_and_homepage(page: Page):
    page.goto("http://localhost:8000/login")

    expect(page.get_by_role("main")).to_match_aria_snapshot("- heading \"Welcome\" [level=1]\n- paragraph: Sign in to continue\n- link \"Login\":\n  - /url: /auth/login")
    page.get_by_role("link", name="Login").click()

    page.get_by_role("textbox", name="Username").fill("admin")
    page.get_by_role("textbox", name="Password").fill("password")
    page.get_by_role("button", name="Sign In").click()

    expect(page).to_have_url("http://localhost:8000/")
    expect(page.get_by_role("main")).to_match_aria_snapshot("- main:\n  - heading \"You are logged in\" [level=1]\n  - link \"View Clients\":\n    - /url: /clients\n  - link \"View Users\":\n    - /url: /users")

    page.get_by_role("button", name="Logout").click()
    expect(page).to_have_url("http://localhost:8000/login")
