import os

import click
import httpx
from dotenv import load_dotenv
from faker import Faker
from rich import print_json

load_dotenv()

TEST_ENDPOINT = "http://127.0.0.1:8000"
KC_URL = os.environ["KC_URL"]
KC_REALM = os.environ["KC_REALM"]
KC_CLIENT_ID = os.environ["KC_CLIENT_ID"]

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

    def create_random_client(self) -> dict:
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name}.{last_name}@example.com".lower()
        response = self.client.post(
            f"{TEST_ENDPOINT}/api/client",
            json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
            },
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def create_random_user(self) -> dict:
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name[0]}{last_name}".lower()
        email = f"{first_name}.{last_name}@example.com".lower()
        response = self.client.post(
            f"{TEST_ENDPOINT}/api/user",
            json={
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            },
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def get_clients(self) -> list[dict]:
        response = self.client.get(
            f"{TEST_ENDPOINT}/api/client",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def get_users(self) -> list[dict]:
        response = self.client.get(
            f"{TEST_ENDPOINT}/api/user",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()


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
        response = session.create_random_client()
        print_json(data=response)


@cli.command()
@user_password_options
def random_user(user: str, password: str):
    with TestSession(user, password) as session:
        response = session.create_random_user()
        print_json(data=response)


@cli.command()
@user_password_options
def list_clients(user: str, password: str):
    with TestSession(user, password) as session:
        response = session.get_clients()
        print_json(data=response)


@cli.command()
@user_password_options
def list_users(user: str, password: str):
    with TestSession(user, password) as session:
        response = session.get_users()
        print_json(data=response)


if __name__ == "__main__":
    cli()
