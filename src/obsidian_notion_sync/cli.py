"""Command-line interface for obsidian-notion-sync"""

import sys
import logging
import click
from obsidian_notion_sync.config import SyncConfig
from obsidian_notion_sync.sync import NotionSync

@click.command()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def main(debug):
    """Sync Obsidian notes to Notion via GitHub"""
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        config = SyncConfig.from_env()
        sync = NotionSync(config)
        sync.run()
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()