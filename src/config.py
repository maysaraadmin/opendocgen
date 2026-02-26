"""
Configuration management for OpenDocGen.
"""

import os
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Core Application Settings
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=8000, env="APP_PORT")
    secret_key: str = Field(default="change-this-to-a-random-secret-key", env="SECRET_KEY")
    
    # Ollama Configuration
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    default_model: str = Field(default="llama3.2", env="DEFAULT_MODEL")
    alternate_model: str = Field(default="mistral", env="ALTERNATE_MODEL")
    code_model: str = Field(default="codellama", env="CODE_MODEL")
    embedding_model: str = Field(default="nomic-embed-text", env="EMBEDDING_MODEL")
    ollama_num_gpu: int = Field(default=35, env="OLLAMA_NUM_GPU")
    ollama_keep_alive: str = Field(default="24h", env="OLLAMA_KEEP_ALIVE")
    
    # SearXNG Configuration
    searxng_url: str = Field(default="http://localhost:8080", env="SEARXNG_URL")
    searxng_timeout: int = Field(default=30, env="SEARXNG_TIMEOUT")
    searxng_safe_search: int = Field(default=0, env="SEARXNG_SAFE_SEARCH")
    
    # Browserless Configuration
    browserless_url: str = Field(default="http://localhost:3000", env="BROWSERLESS_URL")
    browserless_token: Optional[str] = Field(default=None, env="BROWSERLESS_TOKEN")
    browserless_timeout: int = Field(default=60000, env="BROWSERLESS_TIMEOUT")
    
    # Chroma Configuration
    chroma_url: str = Field(default="http://localhost:8000", env="CHROMA_URL")
    chroma_persist_directory: Path = Field(default=Path("./data/chroma"), env="CHROMA_PERSIST_DIRECTORY")
    
    # Unstructured Configuration
    unstructured_url: str = Field(default="http://localhost:8000", env="UNSTRUCTURED_URL")
    unstructured_timeout: int = Field(default=120, env="UNSTRUCTURED_TIMEOUT")
    
    # Storage Paths
    upload_dir: Path = Field(default=Path("./data/uploads"), env="UPLOAD_DIR")
    download_dir: Path = Field(default=Path("./data/downloads"), env="DOWNLOAD_DIR")
    output_dir: Path = Field(default=Path("./data/output"), env="OUTPUT_DIR")
    cache_dir: Path = Field(default=Path("./data/cache"), env="CACHE_DIR")
    log_dir: Path = Field(default=Path("./data/logs"), env="LOG_DIR")
    
    # Security Settings
    max_file_size: int = Field(default=104857600, env="MAX_FILE_SIZE")  # 100MB
    allowed_extensions: str = Field(default="pdf,docx,txt,md,csv,json,xlsx", env="ALLOWED_EXTENSIONS")
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # Feature Flags
    enable_gpu: bool = Field(default=True, env="ENABLE_GPU")
    enable_memory: bool = Field(default=True, env="ENABLE_MEMORY")
    enable_cache: bool = Field(default=True, env="ENABLE_CACHE")
    enable_web_scraping: bool = Field(default=True, env="ENABLE_WEB_SCRAPING")
    enable_code_execution: bool = Field(default=True, env="ENABLE_CODE_EXECUTION")
    
    # Legacy compatibility
    @property
    def api_host(self) -> str:
        return self.app_host
    
    @property
    def api_port(self) -> int:
        return self.app_port
    
    @property
    def chroma_persist_dir(self) -> Path:
        return self.chroma_persist_directory
    
    @property
    def uploads_dir(self) -> Path:
        return self.upload_dir
    
    @property
    def downloads_dir(self) -> Path:
        return self.download_dir
    
    @property
    def app_name(self) -> str:
        return "OpenDocGen"
    
    @property
    def app_version(self) -> str:
        return "0.1.0"
    
    @property
    def cors_origins(self) -> List[str]:
        return ["http://localhost:3000", "http://localhost:8080", "http://localhost:8000"]
    
    def get_allowed_extensions_list(self) -> List[str]:
        """Get allowed extensions as a list."""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings


def create_directories():
    """Create necessary directories."""
    directories = [
        settings.chroma_persist_directory,
        settings.upload_dir,
        settings.download_dir,
        settings.output_dir,
        settings.cache_dir,
        settings.log_dir,
        Path("./data/logs"),
        Path("./data/backups"),
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
