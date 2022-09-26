from tempfile import gettempdir

from pydantic import BaseSettings


class _Settings(BaseSettings):
    out_data_dir: str = gettempdir()
    data_access_prefix: str


settings = _Settings()
