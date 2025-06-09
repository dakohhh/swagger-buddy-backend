import os
import certifi
from pathlib import Path
from dotenv import load_dotenv
from fastapi import Depends
from pydantic import Field
from functools import lru_cache
from typing import Annotated, List, Literal, Union, cast
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()



EnvironmentType = Literal["development", "production"]

env = os.getenv("PYTHON_ENV", "development")

PYTHON_ENV: EnvironmentType = cast(EnvironmentType, env)

# Core application paths
BASE_DIR: Path = Path(__file__).resolve().parent.parent
CERTIFICATE: str = os.path.join(os.path.dirname(certifi.__file__), "cacert.pem")
DOTENV: str = os.path.join(BASE_DIR, ".env")

class APIDocsConfig(BaseSettings):
    """API Documentation configurations with secure password handling"""
    
    # Using str for sensitive credentials
    API_DOCS_USERNAME: str = Field(..., env="API_DOCS_USERNAME")
    API_DOCS_PASSWORD: str = Field(..., env="API_DOCS_PASSWORD")
    
    # API documentation endpoints
    API_DOCS_URL: str = Field("/docs", env="API_DOCS_URL", description="Swagger UI endpoint")
    API_REDOC_URL: str = Field("/redocs", env="API_REDOC_URL", description="ReDoc UI endpoint")
    OPENAPI_URL: str = Field("/openapi.json", env="OPENAPI_URL", description="OpenAPI schema endpoint")


class GlobalConfig(BaseSettings):
    """Base configuration class with shared settings across environments"""

    # Application metadata
    APP_NAME: str = Field("Swagger Buddy API", env="APP_NAME")
    APP_VERSION: str = Field("1.0", env="APP_VERSION")
    APPLICATION_CERTIFICATE: str = Field(default=CERTIFICATE)
    BASE_DIR: Path = Field(default=BASE_DIR)


    ENVIRONMENT: EnvironmentType = PYTHON_ENV

    # If needed, set the port to <PORT>
    # PORT: int = Field(<int:PORT>, env="PORT", description="Application port")

    # Security configurations
    BCRYPT_SALT: int = Field(10, description="Salt rounds for password hashing")
    ACCESS_TOKEN_JWT_EXPIRES_IN: str = Field("1h", env="ACCESS_TOKEN_JWT_EXPIRES_IN")
    REFRESH_TOKEN_JWT_EXPIRES_IN: str = Field("30d", env="REFRESH_TOKEN_JWT_EXPIRES_IN")
    DEFAULT_DB_TOKEN_EXPIRY_DURATION: str = Field("5m", env="DEFAULT_DB_TOKEN_EXPIRY_DURATION")
    CORS_ORIGINS: str = Field(..., env="CORS_ORIGINS")

    # API Documentation settings
    API_DOCS: APIDocsConfig = Field(default_factory=APIDocsConfig)

    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")

    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    @property
    def CORS_ORIGINS_PROCESSED(self) -> List[str]:
        """Parse CORS_ORIGINS from comma-separated string or JSON array"""
        if isinstance(self.CORS_ORIGINS, str):
            if not self.CORS_ORIGINS:
                return []
            # Handle comma-separated values
            if self.CORS_ORIGINS.startswith('[') and self.CORS_ORIGINS.endswith(']'):
                # It's already a JSON array string
                import json
                return json.loads(self.CORS_ORIGINS)
            else:
                # It's comma-separated, split it
                return [origin.strip() for origin in self.CORS_ORIGINS.split(',') if origin.strip()]
        return self.CORS_ORIGINS if isinstance(self.CORS_ORIGINS, list) else []


class DevelopmentConfig(GlobalConfig):
    """Development environment specific configurations"""

    DEBUG: bool = True
    JWT_SECRET: str = Field("secret", description="WARNING: Use strong secret in production")
    JWT_ALGORITHM: str = Field("HS256")
    REDIS_URI: str = Field("redis://localhost:6379/0", description="Local Redis instance")
    BASE_URL: str = "http://localhost:3000"

class ProductionConfig(GlobalConfig):
    """Production environment specific configurations with stricter settings"""

    DEBUG: bool = False
    REDIS_URI: str = Field(..., env="REDIS_URI")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field("HS256")
    BASE_URL: str = Field(..., env="BASE_URL")
    


@lru_cache()
def get_settings() -> DevelopmentConfig | ProductionConfig:
    """
    Factory function to get environment-specific settings
    
    Returns:
        GlobalConfig: Configuration instance based on current environment
    
    Raises:
        ValueError: If PYTHON_ENV is invalid or not set
    """
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig
    }

    if not PYTHON_ENV or PYTHON_ENV not in configs:
        raise ValueError(f"Invalid deployment environment: `{env}`, Must be one of: {list(configs.keys())}")

    return configs[PYTHON_ENV]()



ConfigType = Union[GlobalConfig, DevelopmentConfig, ProductionConfig]


# Initialize settings instance
settings = get_settings()

# Settings for dependency injection
SettingsDep =  Annotated[ConfigType, Depends(get_settings)]

# Uncomment the line below to check the settings set
# print(settings.CORS_ORIGINS_PROCESSED)
