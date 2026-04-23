""" Configurações da aplicação, utilizando Pydantic para validação e carregamento de variáveis de ambiente. """

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str | None = None

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_server: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "atos_receita"

    secret_key: str = "troque-esta-chave-em-producao"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    rpa_target_url: str = "http://normas.receita.fazenda.gov.br/sijut2consulta/consulta.action"
    rpa_api_url: str = "http://localhost:8000/api/v1/atos/bulk"

    logs_path: Path = Path("infra/logs")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url

        # método de construção da URL de conexão com o banco de dados, considerando o ambiente (local ou docker)
        if self.postgres_server == "db":
            # rodando no docker
            host = "db"
        else:
            # rodando local (pytest)
            host = "localhost"

        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@"
            f"{host}:{self.postgres_port}/{self.postgres_db}"
        )

settings = Settings()
settings.logs_path.mkdir(parents=True, exist_ok=True)