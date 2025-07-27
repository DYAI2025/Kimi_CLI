#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration for $projectname$
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for Kimi K2 Agent"""
    
    # Project Information
    PROJECT_NAME = "$projectname$"
    VERSION = "1.0.0"
    
    # API Configuration
    API_KEY = os.getenv("MOONSHOT_API_KEY", "")
    BASE_URL = os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.ai/v1")
    
    # Model Configuration
    MODEL_NAME = os.getenv("KIMI_MODEL", "moonshotai/Kimi-K2-Instruct")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.6"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
    
    # Agent Configuration
    AUTO_SAVE_CONVERSATIONS = os.getenv("AUTO_SAVE_CONVERSATIONS", "true").lower() == "true"
    CONVERSATION_DIR = os.getenv("CONVERSATION_DIR", "conversations")
    PLAN_DIR = os.getenv("PLAN_DIR", "plans")
    
    # Safety Configuration
    ALLOW_SHELL_EXECUTION = os.getenv("ALLOW_SHELL_EXECUTION", "true").lower() == "true"
    COMMAND_TIMEOUT = int(os.getenv("COMMAND_TIMEOUT", "30"))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "kimi_agent.log")
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        errors = []
        
        if not cls.API_KEY or cls.API_KEY == "sk-demo_key_please_replace":
            errors.append("MOONSHOT_API_KEY is required")
        
        if cls.TEMPERATURE < 0.0 or cls.TEMPERATURE > 1.0:
            errors.append("TEMPERATURE must be between 0.0 and 1.0")
        
        if cls.MAX_TOKENS < 1 or cls.MAX_TOKENS > 128000:
            errors.append("MAX_TOKENS must be between 1 and 128000")
        
        return errors
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        dirs = [cls.CONVERSATION_DIR, cls.PLAN_DIR]
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)