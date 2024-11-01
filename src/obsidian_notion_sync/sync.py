import os
import sys
import time
import subprocess
from pathlib import Path
import json
from dataclasses import dataclass
from typing import Optional, List, Dict
import logging
from abc import ABC, abstractmethod
import requests
from github import Github, GithubException
from notion_client import Client
import markdown2
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

class SyncError(Exception):
    """Base exception for sync-related errors"""
    pass

class GitOperationError(SyncError):
    """Exception for Git operation failures"""
    pass

class GithubOperationError(SyncError):
    """Exception for Github API operation failures"""
    pass

class GitManager:
    """Manages Git operations"""
    
    def __init__(self, repo_name: str):
        self.repo_name = repo_name
        # Use absolute path to root folder's ObsidianClonedVault
        self.repo_dir = Path.cwd()
        self.original_dir = Path.cwd()
        
    def init_repo(self) -> None:
        """Initialize git repository"""
        try:
            self.repo_dir.mkdir(exist_ok=True)
            os.chdir(self.repo_dir)
            subprocess.run(["git", "init"] )
        except subprocess.CalledProcessError as e:
            os.chdir(self.original_dir)
            raise GitOperationError(f"Failed to initialize git repository: {e.stderr.decode()}")
            
    def commit_changes(self, message: str) -> None:
        """Commit changes to git repository"""
        try:
            os.chdir(self.repo_dir)
            subprocess.run(["git", "add", "."] )
            subprocess.run(["git", "commit", "-m", message] )
        except subprocess.CalledProcessError as e:
            raise GitOperationError(f"Failed to commit changes: {e.stderr.decode()}")
        finally:
            os.chdir(self.original_dir)
            
    def setup_and_push(self, clone_url: str) -> None:
        """Setup branch and push to remote"""
        try:
            os.chdir(self.repo_dir)
            subprocess.run(["git", "branch", "-M", "main"] )
            subprocess.run(["git", "remote", "add", "origin", clone_url] )
            subprocess.run(["git", "push", "-u", "origin", "main"] )
        except subprocess.CalledProcessError as e:
            raise GitOperationError(f"Failed to push changes: {e.stderr.decode()}")
        finally:
            os.chdir(self.original_dir)

class GithubManager:
    """Manages GitHub operations"""
    
    def __init__(self, token: str):
        self.github = Github(token)
        self.user = self.github.get_user()
        logger.info(f"Authenticated as GitHub user: {self.user.login}")
        
    def get_or_create_repo(self, repo_name: str) -> str:
        """Get existing repository or create new one"""
        try:
            repo = self.user.get_repo(repo_name)
            logger.info(f"Found existing repository: {repo_name}")
        except GithubException:
            repo = self.user.create_repo(repo_name, private=True)
            logger.info(f"Created new repository: {repo_name}")
        return repo
        
    def add_secrets(self, repo: str, secrets: Dict[str, str]) -> None:
        """Add secrets to GitHub repository"""
        try:
            for key, value in secrets.items():
                repo.create_secret(key, value)
            logger.info("Successfully added secrets to repository")
        except GithubException as e:
            raise GithubOperationError(f"Failed to add secrets: {str(e)}")
        

class WorkflowManager:
    """Manages GitHub Actions workflow"""
    
    @staticmethod
    def create_workflow_file() -> None:
        """Create GitHub Actions workflow file"""
        workflow_dir =  Path.cwd() / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_content = """
name: Sync to Notion

on:
  push:
    branches: [main]

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: checkout repo content
        uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          pip install requests markdown2 notion-client logging click obsidian_notion_sync 
      - name: Sync to Notion
        env:
          NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
          NOTION_PAGE_ID: ${{ secrets.NOTION_PAGE_ID }}
        run: |
          cd $GITHUB_WORKSPACE
          obsidian-notion-sync notion-sync

    """
        
        workflow_path = workflow_dir / "sync.yml"
        workflow_path.write_text(workflow_content)
        logger.info("Created GitHub Actions workflow file")

class FileSync:
    """Handles file synchronization"""
    
    @staticmethod
    def sync_obsidian_files(source_dir: Path) -> None:
        """Sync Obsidian files to root's 'ObsidianClonedVault' directory"""
        # Get the absolute path to ObsidianClonedVault in root
        target_dir = Path.cwd() / "ObsidianClonedVault"
        
        try:
            # Create the target directory if it doesn't exist
            target_dir.mkdir(exist_ok=True)
            
            # Remove existing contents of the target directory
            for item in target_dir.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir() and item.name != '.git':  # Preserve .git directory
                    shutil.rmtree(item)
            
            # Copy files from source to target
            for item in source_dir.glob('**/*'):
                if '.git' in item.parts:  # Skip .git directories and files
                    continue
                    
                relative_path = item.relative_to(source_dir)
                target_path = target_dir / relative_path
                
                if item.is_file():
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target_path)
                elif item.is_dir():
                    target_path.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Successfully synced Obsidian files to {target_dir}")
        except Exception as e:
            raise SyncError(f"Failed to sync files: {str(e)}")

class NotionSync:
    """Manages the entire sync process"""
    
    def __init__(self, config: SyncConfig):
        self.config = config
        self.github_manager = GithubManager(config.github_token)
        self.git_manager = GitManager(config.repo_name)
        
    def run(self) -> None:
        """Run the complete sync process"""
        try:
            # Initialize Git repository
            self.git_manager.init_repo()
            
            # Setup GitHub repository
            repo = self.github_manager.get_or_create_repo(self.config.repo_name)
            
            # Sync files
            FileSync.sync_obsidian_files(self.config.obsidian_dir)
            
            # Initial commit and push
            self.git_manager.commit_changes("Initial sync of Obsidian notes")
            self.git_manager.setup_and_push(repo.clone_url)
            
            # Create workflow directory in ObsidianClonedVault
            workflow_dir = self.git_manager.repo_dir / ".github" / "workflows"
            workflow_dir.mkdir(parents=True, exist_ok=True)
            
            # Setup GitHub Actions
            WorkflowManager.create_workflow_file()
            
            # Commit and push workflow
            self.git_manager.commit_changes("Add GitHub Actions workflow")
            self.git_manager.setup_and_push(repo.clone_url)
            
            # Add secrets
            secrets = {
                "NOTION_TOKEN": self.config.notion_token,
                "NOTION_PAGE_ID": self.config.notion_database_id
            }
            self.github_manager.add_secrets(repo, secrets)
            
            logger.info("Sync process completed successfully")
            
        except (SyncError, GitOperationError, GithubOperationError) as e:
            logger.error(f"Sync process failed: {str(e)}")
            raise

def main():
    try:
        config = SyncConfig.from_env()
        sync = NotionSync(config)
        sync.run()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()



