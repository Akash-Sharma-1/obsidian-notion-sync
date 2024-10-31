"""Configuration management for obsidian-notion-sync"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class SyncConfig:
    """Configuration for the sync process"""
    github_token: str
    notion_token: str
    obsidian_dir: Path
    repo_name: str
    notion_database_id: str
    
    @classmethod
    def from_env(cls) -> 'SyncConfig':
        """Create configuration from environment variables"""
        required_vars = {
            'GITHUB_TOKEN': os.getenv('GITHUB_TOKEN'),
            'NOTION_TOKEN': os.getenv('NOTION_TOKEN'),
            'OBSIDIAN_DIR': os.getenv('OBSIDIAN_DIR'),
            'REPO_NAME': os.getenv('REPO_NAME'),
            'NOTION_PAGE_ID': os.getenv('NOTION_PAGE_ID')
        }
        
        missing_vars = [k for k, v in required_vars.items() if not v]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
        return cls(
            github_token=required_vars['GITHUB_TOKEN'],
            notion_token=required_vars['NOTION_TOKEN'],
            obsidian_dir=Path(required_vars['OBSIDIAN_DIR']),
            repo_name=required_vars['REPO_NAME'],
            notion_database_id=required_vars['NOTION_PAGE_ID']
        )