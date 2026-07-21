import secrets

import click
import httpx
from faker import Faker
from rich import print_json

TEST_ENDPOINT = "http://127.0.0.1:8000"

fake = Faker()


class TestSession:
    def __init__(self, username: str):
        self.client = httpx.Client()
        self.username = username

    def __enter__(self):
        response = self.client.post(
            f"{TEST_ENDPOINT}/login",
            data={
                "grant": "password",
                "username": self.username,
                "password": secrets.token_urlsafe(16),
            },
        )
        if response.status_code != 303:
            response.raise_for_status()
        return self

    def __exit__(self, exc_type, exc, tb):
        response = self.client.post(f"{TEST_ENDPOINT}/logout")
        if response.status_code != 303:
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
                "name": f"{first_name} {last_name}",
                "email": email,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_clients(self) -> list[dict]:
        response = self.client.get(f"{TEST_ENDPOINT}/api/client")
        response.raise_for_status()
        return response.json()

    def get_users(self) -> list[dict]:
        response = self.client.get(f"{TEST_ENDPOINT}/api/user")
        response.raise_for_status()
        return response.json()


@click.group()
def cli():
    pass


@cli.command()
@click.option("--user", default="admin", type=click.STRING)
def random_client(user: str):
    with TestSession(user) as session:
        response = session.create_random_client()
        print_json(data=response)


@cli.command()
@click.option("--user", default="admin", type=click.STRING)
def random_user(user: str):
    with TestSession(user) as session:
        response = session.create_random_user()
        print_json(data=response)


@cli.command()
@click.option("--user", default="admin", type=click.STRING)
def list_clients(user: str):
    with TestSession(user) as session:
        response = session.get_clients()
        print_json(data=response)


@cli.command()
@click.option("--user", default="admin", type=click.STRING)
def list_users(user: str):
    with TestSession(user) as session:
        response = session.get_users()
        print_json(data=response)


if __name__ == "__main__":
    cli()
