from pydantic import BaseSettings


class _Settings(BaseSettings):
    creds_hash: str


settings = _Settings()
