# SPDX-FileCopyrightText: 2024-present Akash Sharma <howdy.akash@gmail.com>
#
# SPDX-License-Identifier: MIT
"""
Obsidian to Notion sync tool
"""


from obsidian_notion_sync.sync import NotionSync
from obsidian_notion_sync.config import SyncConfig

__all__ = ['NotionSync', 'SyncConfig']