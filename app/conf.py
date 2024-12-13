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

    # TODO: Actually set up the testing db
    # test_postgres_db: str
    # test_postgres_user: str
    # test_postgres_password: str
    # test_postgres_host: str
    # test_postgres_port: int

    debug: bool = False

    @computed_field
    def postgres_async_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )

    @computed_field
    def test_postgres_async_url(self) -> PostgresDsn:
        return self.postgres_async_url

        # TODO: Actually set up the testing db

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.test_postgres_user,
            password=self.test_postgres_password,
            host=self.test_postgres_host,
            port=self.test_postgres_port,
            path=self.test_postgres_db,
        )
