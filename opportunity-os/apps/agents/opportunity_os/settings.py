"""Runtime configuration loaded from environment."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # AI providers
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")

    # Data providers
    semrush_api_key: str = Field(default="", alias="SEMRUSH_API_KEY")
    dataforseo_login: str = Field(default="", alias="DATAFORSEO_LOGIN")
    dataforseo_password: str = Field(default="", alias="DATAFORSEO_PASSWORD")
    apify_token: str = Field(default="", alias="APIFY_TOKEN")
    brightdata_token: str = Field(default="", alias="BRIGHTDATA_TOKEN")

    # Reddit
    reddit_client_id: str = Field(default="", alias="REDDIT_CLIENT_ID")
    reddit_client_secret: str = Field(default="", alias="REDDIT_CLIENT_SECRET")
    reddit_user_agent: str = Field(
        default="opportunity-os/0.1", alias="REDDIT_USER_AGENT"
    )

    # Storage
    database_url: str = Field(default="", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    # Models
    primary_model: str = Field(default="claude-opus-4-7", alias="PRIMARY_MODEL")
    fast_model: str = Field(default="claude-haiku-4-5-20251001", alias="FAST_MODEL")

    # Cost controls
    daily_budget_usd: float = Field(default=50.0, alias="DAILY_BUDGET_USD")
    cache_ttl_hours: int = Field(default=24, alias="CACHE_TTL_HOURS")


settings = Settings()
