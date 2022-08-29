from os import path

from pydantic import BaseSettings


class _Settings(BaseSettings):
    src_data_dir: str
    out_data_dir: str = path.join(path.dirname(__file__), ".output")


settings = _Settings()
