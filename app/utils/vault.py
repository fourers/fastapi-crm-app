from functools import cache

from hvac import Client


@cache
def _get_client() -> Client:
    return Client()


def get_secret(path: str) -> dict:
    client = _get_client()
    return client.secrets.kv.v2.read_secret_version(
        path=path,
    )["data"]["data"]
