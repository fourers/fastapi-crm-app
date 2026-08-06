import hashlib


def sha_256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
