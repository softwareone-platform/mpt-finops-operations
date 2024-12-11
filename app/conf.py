import pathlib

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings

PROJECT_ROOT = pathlib.Path(__file__).parent.parent


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    debug: bool = False

    @computed_field
    @property
    def postgres_async_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )
