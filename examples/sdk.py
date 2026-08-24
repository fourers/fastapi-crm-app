from dataclasses import dataclass, field
from functools import cached_property

import httpx


@dataclass
class Client:
    api_endpoint: str
    oidc_config_endpoint: str
    client_id: str
    client_secret: str
    username: str
    password: str
    client: httpx.Client = field(init=False)
    access_token: str | None = field(init=False)

    def __post_init__(self):
        self.api_endpoint = self.api_endpoint.rstrip("/")
        self.client = httpx.Client()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        self.client.close()

    @cached_property
    def oidc_config(self) -> dict:
        response = self.client.get(self.oidc_config_endpoint)
        response.raise_for_status()
        return response.json()

    def login(self) -> None:
        token_resp = self.client.post(
            self.oidc_config["token_endpoint"],
            data={
                "grant_type": "password",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "username": self.username,
                "password": self.password,
                "scope": "openid profile email",
            },
        )
        token_resp.raise_for_status()
        tokens = token_resp.json()
        self.access_token = tokens["access_token"]

    @property
    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}"}

    def logout(self) -> None:
        response = self.client.post(
            self.oidc_config["end_session_endpoint"],
            headers=self.headers,
        )
        response.raise_for_status()

    def post(self, endpoint: str, data: dict) -> dict:
        response = self.client.post(
            f"{self.api_endpoint}{endpoint}",
            json=data,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: dict | None = None) -> dict | None:
        response = self.client.put(
            f"{self.api_endpoint}{endpoint}",
            json=data,
            headers=self.headers,
        )
        response.raise_for_status()
        if data:
            return response.json()

    def create_client(self, data: dict) -> dict:
        return self.post("/api/client", data)

    def create_user(self, data: dict) -> dict:
        return self.post("/api/user", data)

    def create_group(self, data: dict) -> dict:
        return self.post("/api/group", data)

    def add_user_to_group(self, user_id: int, group_id: int) -> None:
        self.put(f"/api/group/{group_id}/user/{user_id}")

    def set_parent_of_group(self, parent_id: int, group_id: int) -> None:
        self.put(f"/api/group/{group_id}/parent/{parent_id}")
