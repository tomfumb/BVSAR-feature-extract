from os import path
from tempfile import gettempdir

from pydantic import BaseSettings


class _Settings(BaseSettings):
    src_data_dir: str = path.join(path.dirname(__file__), "..", "..", "data")
    out_data_dir: str = gettempdir()


settings = _Settings()
