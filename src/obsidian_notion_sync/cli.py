"""Command-line interface for obsidian-notion-sync"""

import sys
import logging
import click
from obsidian_notion_sync.config import SyncConfig
from obsidian_notion_sync.sync import NotionSync
from obsidian_notion_sync.sync_to_notion import main as notion_sync_main


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--debug', is_flag=True, help='Enable debug logging')
def main(ctx, debug):
    """Sync Obsidian notes to Notion via GitHub"""

    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # If no subcommand is used, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit()

@main.command()
def git_sync():
    """Sync Obsidian notes to GitHub"""
    try:
        config = SyncConfig.from_env()
        sync = NotionSync(config)
        sync.run()
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        sys.exit(1)

@main.command()
def notion_sync():
    """Sync Github placed Obsidian notes with Notion"""
    try:
        notion_sync_main()
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        sys.exit(1)



if __name__ == "__main__":
    main()