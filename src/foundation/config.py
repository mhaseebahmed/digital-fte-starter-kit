from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath, Field

class GlobalConfig(BaseSettings):
    # 1. Environment
    ENV: str = Field(default="dev", pattern="^(dev|prod)$")
    
    # 2. File System
    VAULT_PATH: Path = Field(default=Path("./Vault"))
    
    # 3. Security: REMOVED API KEY (Handled by 'claude login')
    
    # 4. Limits
    MAX_RETRIES: int = 3
    POLL_INTERVAL: int = 60

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

    def get_inbox_path(self) -> Path:
        return self.VAULT_PATH / "00_Inbox"

    def get_processing_path(self) -> Path:
        return self.VAULT_PATH / "10_Processing"

    def get_done_path(self) -> Path:
        return self.VAULT_PATH / "20_Done"

# Singleton
try:
    settings = GlobalConfig()
except Exception as e:
    print(f"❌ FATAL CONFIG ERROR: {e}")
    exit(1)