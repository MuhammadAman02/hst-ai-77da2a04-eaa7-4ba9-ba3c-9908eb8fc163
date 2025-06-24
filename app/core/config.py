"""
Configuration settings for Seiko Watch Store
"""

import os
from typing import Optional
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    app_name: str = "Seiko Watch Store"
    app_version: str = "1.0.0"
    app_description: str = "Professional e-commerce platform for luxury Seiko timepieces"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = False
    
    # Security
    secret_key: str = "seiko-watch-store-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = "sqlite:///./seiko_store.db"
    
    # Payment (for future integration)
    stripe_publishable_key: Optional[str] = None
    stripe_secret_key: Optional[str] = None
    
    # Email (for future integration)
    smtp_server: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # File uploads
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: list = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    
    @validator("debug", pre=True)
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return bool(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()