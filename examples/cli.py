import os
import time

import click
import httpx
import jwt
from dotenv import load_dotenv
from faker import Faker
from jwt import PyJWKClient
from rich import print_json

load_dotenv()

TEST_ENDPOINT = "http://localhost:8000"
KC_URL = "http://localhost:8080"
KC_REALM = "myapp"
KC_CLIENT_ID = "click-cli"
KC_CLIENT_SECRET = os.environ["CLICK_CLI_SECRET"]

fake = Faker()


class TestSession:
    def __init__(self, username: str, password: str):
        self.client = httpx.Client()
        self.username = username
        self.password = password
        self.access_token = "xxx"

    def __enter__(self):
        self.login(self.username, self.password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        self.client.close()

    def login(self, username: str, password: str) -> None:
        token_resp = self.client.post(
            f"{KC_URL}/realms/{KC_REALM}/protocol/openid-connect/token",
            data={
                "grant_type": "password",
                "client_id": KC_CLIENT_ID,
                "client_secret": KC_CLIENT_SECRET,
                "username": username,
                "password": password,
                "scope": "openid profile email",
            },
        )
        token_resp.raise_for_status()
        tokens = token_resp.json()
        self.access_token = tokens["access_token"]

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def logout(self) -> None:
        response = self.client.post(
            f"{KC_URL}/realms/{KC_REALM}/protocol/openid-connect/logout",
            headers=self.headers,
        )
        response.raise_for_status()


def user_password_options(func):
    func = click.option("--user", default="admin", type=click.STRING)(func)
    return click.option("--password", default="password", type=click.STRING)(func)


@click.group()
def cli():
    pass


@cli.command()
@user_password_options
def random_client(user: str, password: str):
    with TestSession(user, password) as session:
        first_name = fake.first_name()
        last_name = fake.last_name()
        response = session.client.post(
            f"{TEST_ENDPOINT}/api/client",
            json={
                "first_name": first_name,
                "last_name": last_name,
                "email": f"{first_name}.{last_name}@example.com".lower(),
            },
            headers=session.headers,
        )
        response.raise_for_status()
        print_json(data=response.json())


@cli.command()
@user_password_options
def random_user(user: str, password: str):
    with TestSession(user, password) as session:
        first_name = fake.first_name()
        last_name = fake.last_name()
        response = session.client.post(
            f"{TEST_ENDPOINT}/api/user",
            json={
                "username": f"{first_name[0]}{last_name}".lower(),
                "email": f"{first_name}.{last_name}@example.com".lower(),
                "first_name": first_name,
                "last_name": last_name,
            },
            headers=session.headers,
        )
        response.raise_for_status()
        print_json(data=response.json())


@cli.command()
@user_password_options
def list_clients(user: str, password: str):
    with TestSession(user, password) as session:
        response = session.client.get(
            f"{TEST_ENDPOINT}/api/client",
            headers=session.headers,
        )
        response.raise_for_status()
        print_json(data=response.json())


@cli.command()
@user_password_options
def list_users(user: str, password: str):
    with TestSession(user, password) as session:
        response = session.client.get(
            f"{TEST_ENDPOINT}/api/user",
            headers=session.headers,
        )
        response.raise_for_status()
        print_json(data=response.json())


@cli.command()
@user_password_options
def me(user: str, password: str):
    with TestSession(user, password) as session:
        response = session.client.get(
            f"{TEST_ENDPOINT}/auth/me", headers=session.headers
        )
        response.raise_for_status()
        print_json(data=response.json())


@cli.command()
@user_password_options
def introspect(user: str, password: str):
    with TestSession(user, password) as session:
        response = session.client.post(
            f"{KC_URL}/realms/{KC_REALM}/protocol/openid-connect/token/introspect",
            data={
                "client_id": KC_CLIENT_ID,
                "client_secret": KC_CLIENT_SECRET,
                "token": session.access_token,
                "token_type_hint": "access_token",
            },
        )
        response.raise_for_status()
        print_json(data=response.json())


@cli.command()
@user_password_options
def decode(user: str, password: str):
    with TestSession(user, password) as session:
        jwk_keys = PyJWKClient(
            f"{KC_URL}/realms/{KC_REALM}/protocol/openid-connect/certs"
        )
        data = {
            "header": jwt.get_unverified_header(session.access_token),
            "payload": jwt.decode(
                session.access_token,
                key=jwk_keys.get_signing_key_from_jwt(session.access_token),
                algorithms=["RS256"],
                options={"verify_signature": False},
            ),
        }
        print_json(data=data)


@cli.command
@user_password_options
def token(user: str, password: str):
    with TestSession(user, password) as session:
        click.secho("Access token:", fg="cyan")
        click.echo(session.access_token)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            click.secho("\nEnding session...", fg="yellow")


if __name__ == "__main__":
    cli()
