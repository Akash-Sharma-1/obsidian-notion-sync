import os
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from notion_client import Client
import markdown2
import re
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path

## Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class NotionBlockType(Enum):
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    PARAGRAPH = "paragraph"
    BULLETED_LIST = "bulleted_list_item"
    NUMBERED_LIST = "numbered_list_item"
    CODE = "code"
    QUOTE = "quote"
    IMAGE = "image"

@dataclass
class NotionBlock:
    type: NotionBlockType
    content: str
    additional_props: Dict = None

    def to_notion_format(self) -> Dict[str, Any]:
        base_block = {
            "type": self.type.value,
            self.type.value: {
                "rich_text": [{"type": "text", "text": {"content": self.content}}]
            }
        }
        
        if self.additional_props:
            base_block[self.type.value].update(self.additional_props)
            
        # Special handling for images
        if self.type == NotionBlockType.IMAGE:
            base_block["image"] = {
                "type": "external",
                "external": {"url": self.content}
            }
            
        return base_block

class MarkdownConverter:
    """Converts Markdown content to HTML to Notion blocks"""
    
    def __init__(self, content: str):
        self.content = content
        self.html_content = markdown2.markdown(content)
        
    def _parse_heading(self, line: str, level: int) -> NotionBlock:
        text = line[4:-5]  # Remove <h1> and </h1>
        block_type = getattr(NotionBlockType, f"HEADING_{level}")
        return NotionBlock(type=block_type, content=text)
    
    def _parse_paragraph(self, line: str) -> NotionBlock:
        text = line[3:-4]  # Remove <p> and </p>
        return NotionBlock(type=NotionBlockType.PARAGRAPH, content=text)
    
    def _parse_list_items(self, line: str, ordered: bool = False) -> List[NotionBlock]:
        block_type = NotionBlockType.NUMBERED_LIST if ordered else NotionBlockType.BULLETED_LIST
        list_item_pattern = re.compile(r'<li>(.*?)</li>')
        items = list_item_pattern.findall(line)
        return [NotionBlock(type=block_type, content=item) for item in items]
    
    def _parse_code(self, line: str) -> NotionBlock:
        text = line[11:-13]  # Remove <pre><code> and </code></pre>
        return NotionBlock(
            type=NotionBlockType.CODE,
            content=text,
            additional_props={"language": "plain text"}
        )
    
    def _parse_quote(self, line: str) -> NotionBlock:
        text = line[12:-13]  # Remove <blockquote> tags
        return NotionBlock(type=NotionBlockType.QUOTE, content=text)
    
    def _parse_image(self, line: str) -> NotionBlock:
        src = re.search(r'src="(.*?)"', line).group(1)
        return NotionBlock(type=NotionBlockType.IMAGE, content=src)
    
    def to_notion_blocks(self) -> List[Dict[str, Any]]:
        blocks = []
        lines = self.html_content.splitlines()
        
        for line in lines:
            if not line.strip():
                continue
                
            if line.startswith("<h1>"):
                blocks.append(self._parse_heading(line, 1))
            elif line.startswith("<h2>"):
                blocks.append(self._parse_heading(line, 2))
            elif line.startswith("<h3>"):
                blocks.append(self._parse_heading(line, 3))
            elif line.startswith("<p>"):
                blocks.append(self._parse_paragraph(line))
            elif "<ul>" in line:
                blocks.extend(self._parse_list_items(line))
            elif "<ol>" in line:
                blocks.extend(self._parse_list_items(line, ordered=True))
            elif line.startswith("<pre><code>"):
                blocks.append(self._parse_code(line))
            elif line.startswith("<blockquote>"):
                blocks.append(self._parse_quote(line))
            elif line.startswith("<img"):
                blocks.append(self._parse_image(line))
                
        return [block.to_notion_format() for block in blocks]

class NotionSync:
    """Handles synchronization with Notion using Notion API"""
    
    def __init__(self, token: str, database_id: str):
        self.client = Client(auth=token)
        self.database_id = database_id
        
    def create_page(self, title: str, parent_id: str = None) -> Dict:
        target_id = parent_id or self.database_id
        return self.client.pages.create(
            parent={"page_id": target_id},
            properties={
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            }
        )
    
    def add_blocks_to_page(self, page_id: str, blocks: List[Dict]) -> None:
        if blocks:
            self.client.blocks.children.append(
                block_id=page_id,
                children=blocks
            )

class FileProcessor:
    """Processes files and directories for syncing"""
    
    def __init__(self, notion_sync: NotionSync):
        self.notion_sync = notion_sync
        
    def process_markdown_file(self, file_path: str, parent_id: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        title = os.path.splitext(os.path.basename(file_path))[0]
        converter = MarkdownConverter(content)
        blocks = converter.to_notion_blocks()
        
        # Create page and add blocks
        page = self.notion_sync.create_page(title, parent_id)
        self.notion_sync.add_blocks_to_page(page["id"], blocks)

        logger.info(f"Processed Markdown file: {file_path} ...")
        
    def process_directory(self, directory: str, parent_id: str) -> None:
        for item in os.listdir(directory):
            if item.startswith('.') or item == "test":
                continue
                
            item_path = os.path.join(directory, item)
            
            if os.path.isdir(item_path):
                page = self.notion_sync.create_page(item, parent_id)
                self.process_directory(item_path, page['id'])
            elif item.endswith('.md'):
                self.process_markdown_file(item_path, parent_id)

def main():


    token = os.environ['NOTION_TOKEN']
    database_id = os.environ['NOTION_PAGE_ID']
    
    notion_sync = NotionSync(token, database_id)
    processor = FileProcessor(notion_sync)
    
    logger.info(f"Starting sync to Notion database: {database_id}")
    directory = "ObsidianClonedVault"
    logger.info(Path.cwd())
    
    processor.process_directory(directory, database_id)
    logger.info("Sync to Notion completed.")

if __name__ == "__main__":
    main()