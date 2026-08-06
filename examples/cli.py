import click
import httpx
import jwt
from dotenv import load_dotenv
from faker import Faker
from jwt import PyJWKClient
from rich import print_json

load_dotenv()

TEST_ENDPOINT = "http://127.0.0.1:8000"

fake = Faker()


class TestSession:
    def __init__(self, username: str, password: str):
        self.client = httpx.Client()
        self.username = username
        self.password = password
        self.access_token = "xxx"

        from app.config.keycloak import settings

        self.keycloak_url = settings.server_url
        self.realm = settings.realm
        self.client_id = settings.client_id
        self.client_secret = settings.client_secret

    def __enter__(self):
        self.login(self.username, self.password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        self.client.close()

    def login(self, username: str, password: str) -> None:
        token_resp = self.client.post(
            f"{self.keycloak_url}/realms/{self.realm}/protocol/openid-connect/token",
            data={
                "grant_type": "password",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
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
            f"{self.keycloak_url}/realms/{self.realm}/protocol/openid-connect/logout",
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

    def me(self) -> dict:
        response = self.client.get(f"{TEST_ENDPOINT}/auth/me", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def introspect(self) -> dict:
        response = self.client.post(
            f"{self.keycloak_url}/realms/{self.realm}/protocol/openid-connect/token/introspect",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "token": self.access_token,
                "token_type_hint": "access_token",
            },
        )
        response.raise_for_status()
        return response.json()

    def decode(self) -> dict:
        jwk_keys = PyJWKClient(
            f"{self.keycloak_url}/realms/{self.realm}/protocol/openid-connect/certs"
        )
        return {
            "header": jwt.get_unverified_header(self.access_token),
            "payload": jwt.decode(
                self.access_token,
                key=jwk_keys.get_signing_key_from_jwt(self.access_token),
                algorithms=["RS256"],
                options={"verify_signature": False},
            ),
        }


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


@cli.command()
@user_password_options
def me(user: str, password: str):
    with TestSession(user, password) as session:
        response = session.me()
        print_json(data=response)


@cli.command()
@user_password_options
def introspect(user: str, password: str):
    with TestSession(user, password) as session:
        response = session.introspect()
        print_json(data=response)


@cli.command()
@user_password_options
def decode(user: str, password: str):
    with TestSession(user, password) as session:
        response = session.decode()
        print_json(data=response)


if __name__ == "__main__":
    cli()
