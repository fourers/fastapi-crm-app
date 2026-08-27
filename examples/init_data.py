import os
from dataclasses import dataclass

from dotenv import load_dotenv
from faker import Faker
from sdk import Client

fake = Faker()


@dataclass
class TestClient:
    client: Client

    def random_client(self) -> int:
        first_name = fake.first_name()
        last_name = fake.last_name()
        response = self.client.create_client(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": f"{first_name}.{last_name}@example.com".lower(),
            },
        )
        return response["id"]

    def random_user(self) -> int:
        first_name = fake.first_name()
        last_name = fake.last_name()
        response = self.client.create_user(
            {
                "username": f"{first_name[0]}{last_name}".lower(),
                "email": f"{first_name}.{last_name}@example.com".lower(),
                "first_name": first_name,
                "last_name": last_name,
            }
        )
        return response["id"]

    def random_group(self) -> int:
        response = self.client.create_group(
            {
                "name": fake.company(),
            }
        )
        return response["id"]


def get_client():
    return Client(
        api_endpoint="http://localhost:8000",
        oidc_config_endpoint="http://localhost:8080/realms/myapp/.well-known/openid-configuration",
        client_id="click-cli",
        client_secret=os.environ["CLICK_CLI_SECRET"],
        username="admin",
        password="password",
    )


def init():
    with get_client() as client:
        test_client = TestClient(client)

        for _ in range(10):
            test_client.random_client()

        for _ in range(5):
            new_group = test_client.random_group()

            for _ in range(2):
                child_group = test_client.random_group()
                client.set_parent_of_group(new_group, child_group)

                new_user = test_client.random_user()
                client.add_user_to_group(new_user, new_group)


if __name__ == "__main__":
    load_dotenv()
    init()
