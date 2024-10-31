# Obsidian Notion Sync

🧑‍💻 A tool to sync Obsidian notes to Notion via GitHub.

![Diagram](img/productImage.png)

# 📩 Installation

```bash
pip install obsidian-notion-sync
```

[![PyPI - Version](https://img.shields.io/pypi/v/obsidian-notion-sync.svg)](https://pypi.org/project/obsidian-notion-sync)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/obsidian-notion-sync.svg)](https://pypi.org/project/obsidian-notion-sync)


# 🔄 Usage

Basic sync:
```bash
obsidian-notion-sync
```

Enable debug logging:
```bash
obsidian-notion-sync --debug
```

View help:
```bash
obsidian-notion-sync --help
```


# 🛠️ Configuration

Before using the tool, you need to set up the following environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| GITHUB_TOKEN | Your GitHub personal access token | ghp_1234... |
| NOTION_TOKEN | Your Notion integration token | secret_5678... |
| OBSIDIAN_DIR | Path to your Obsidian vault | /Users/you/ObsidianVault |
| REPO_NAME | Name for the GitHub repository | My-Second-Brain |
| NOTION_PAGE_ID | ID of your Notion page | abc123... |

## 🍪 Setting up tokens

1. **GitHub Token**: 
   - Go to GitHub Settings → Developer Settings → Personal Access Tokens
   - Create a new token with 'repo' permissions
   
2. **Notion Token**: 
__(more details below)__
   - Go to www.notion.so/my-integrations
   - Create a new integration
   - Copy the integration token
   
3. **Notion page ID**: 
__(more details below)__
   - Create a new page in Notion
   - Copy the page ID from the URL (it's the part after the page name and after the last '-')

## 📄 (Detailed) Setting up notion page 
__(Skip this section if you were able to set the notion api tokens and page access  )__

1. Create a notion page (The red box highlighted is the Page Id - you need)
![Notion Page](img/Obsidian_notion_page.png)

2. Go to https://www.notion.so/profile/integrations 
![Integration](img/Integrations.png)

3. Create an integration  
![New Integration](img/NewIntegrations.png)

4. Copy this token 
![Copy This token](img/CopyThisToken.png)

5. Allow your notion page to gain access
![Allow page for integration access](img/PageAccessToIntegration.png)

## 📑 Example Configuration Script

You can create a shell script to set up your environment:

```bash
#!/bin/bash
export GITHUB_TOKEN="your_github_token"
export NOTION_TOKEN="your_notion_token"
export OBSIDIAN_DIR="/path/to/your/obsidian/vault"
export REPO_NAME="your-repo-name"
export NOTION_PAGE_ID="your_page_id"

obsidian-notion-sync --debug
```

Save this as `run-sync.sh`, make it executable (`chmod +x run-sync.sh`), and run it with `./run-sync.sh`.


## 🖥️ Troubleshooting

If you encounter errors:

1. Check that all environment variables are set correctly:
   ```bash
   echo $GITHUB_TOKEN
   echo $NOTION_TOKEN
   echo $OBSIDIAN_DIR
   echo $REPO_NAME
   echo $NOTION_PAGE_ID
   ```

2. Ensure your Obsidian vault path exists and is accessible

3. Verify that your GitHub token has the necessary permissions

4. Check that your Notion integration is properly configured and has access to the page

## 🧑‍🧑‍🧒‍🧒 Support

If you encounter any issues, please file them on our GitHub repository's issue tracker.


## License

`obisidian-notion-sync` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

# 📂 Directory structure:
```
# obsidian_notion_sync/
# ├── .github/
# │   └── workflows/
# │       └── sync.yml
# ├── src/
# │   └── obsidian_notion_sync/
# │       ├── __init__.py
# │       ├── __about__.py
# │       ├── _version.py
# │       ├── cli.py
# │       ├── config.py
# │       ├── sync.py
# │       ├── sync_to_notion.py
# │       └── exceptions.py
# ├── tests/
# │   └── __init__.py
# ├── .gitignore
# ├── LICENSE
# ├── README.md
# ├── pyproject.toml
```