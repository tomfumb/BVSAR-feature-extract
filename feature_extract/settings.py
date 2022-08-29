from tempfile import gettempdir

from pydantic import BaseSettings


class _Settings(BaseSettings):
    src_data_dir: str
    out_data_dir: str = gettempdir()


settings = _Settings()
