"""Exception classes for obsidian-notion-sync"""

class SyncError(Exception):
    """Base exception for sync-related errors"""
    pass

class GitOperationError(SyncError):
    """Exception for Git operation failures"""
    pass

class GithubOperationError(SyncError):
    """Exception for Github API operation failures"""
    pass