from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath, Field, ValidationError, field_validator

class GlobalConfig(BaseSettings):
    # 1. Environment
    ENV: str = Field(default="dev", pattern="^(dev|prod)$")
    
    # 2. File System
    VAULT_PATH: Path = Field(default=Path("./Vault"))
    
    # 3. Limits
    MAX_RETRIES: int = Field(default=3, ge=1)
    POLL_INTERVAL: int = Field(default=60, ge=5) # Minimum 5 seconds

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

    @field_validator("VAULT_PATH")
    @classmethod
    def check_vault_path(cls, v: Path) -> Path:
        if v.exists() and not v.is_dir():
            raise ValueError(f"Path {v} exists but is not a directory.")
        return v

    def get_inbox_path(self) -> Path:
        return self.VAULT_PATH / "00_Inbox"

    def get_processing_path(self) -> Path:
        return self.VAULT_PATH / "10_Processing"

    def get_done_path(self) -> Path:
        return self.VAULT_PATH / "20_Done"

# Singleton
# We allow this to raise ValidationError so the app crashes on bad config.
# This is desired behavior for Enterprise Software ("Fail Fast").
settings = GlobalConfig()
