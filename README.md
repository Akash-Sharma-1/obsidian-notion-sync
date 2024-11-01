<p align="center">
   <p align="center">
      <b> A tool to sync Obsidian notes to Notion via GitHub </b> 👨‍💻...
      <p align="center">
      <img src="https://raw.githubusercontent.com/Akash-Sharma-1/obsidian-notion-sync/refs/heads/main/img/productImage.png" width="300">
      <br/>
      <a href="https://github.com/Akash-Sharma-1/obsidian-notion-sync/issues">Report a Bug/Issue</a> | <a href="https://github.com/Akash-Sharma-1/obsidian-notion-sync/discussions">Request a Feature</a> | <a href="https://github.com/users/Akash-Sharma-1/obsidian-notion-sync/1">View Project Status</a>
        <p align="center"><img src="https://img.shields.io/badge/Tests-Passing-brightgreen" /> <img src="https://img.shields.io/badge/PR-Welcomed !-orange" />  <img src="https://img.shields.io/badge/License-MIT-blue.svg" /> <img src="https://img.shields.io/badge/Maintained%3F-Yes !-violet.svg" />

   </p>
</p>
</p>

---

# Obsidian Notion Sync

# 📩 Installation

```bash
pip install obsidian-notion-sync
```

[![PyPI - Version](https://img.shields.io/pypi/v/obsidian-notion-sync.svg)](https://pypi.org/project/obsidian-notion-sync)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/obsidian-notion-sync.svg)](https://pypi.org/project/obsidian-notion-sync)


# 🔄 Usage

There are 2 modes to use it : 

**Doing Obsidian sync with Git** (this automatically triggers the below mode with Github Action)
```bash
>> obsidian-notion-sync git-sync
```

**Doing Obsidian Vault sync with Notion**
```bash
>> obsidian-notion-sync notion-sync
```

**Synopsis**
```bash
>> obsidian-notion-sync

Usage: obsidian-notion-sync [OPTIONS] COMMAND [ARGS]...
Sync Obsidian notes to Notion via GitHub

Options:
  --debug  Enable debug logging
  --help   Show this message and exit.

Commands:
  git-sync     Sync Obsidian notes to GitHub
  notion-sync  Sync Github placed Obsidian notes with Notion

```

# 🎛️ How does it work ? 

### This is how the pipeline's overview looks like: 

![Pipeline](img/Pipeline.png)

## 🎯 Detailed workflow 

### Step 1 : Takes up file all the files from your obsidian vault. 
Uses the vault path given in the env variable

![Obsidian Vault](img/obsidian_vault.png)

### Step 2 : Upon the running of the command, it copies the value at the place of invocation 
Choose a place of invocation and it creates a directory named 'ObsidianClonedVault'.
   
![Collected Locally](img/CollectedLocally.png)

### Step 3 : It then syncs this folder with a Github Repo 
You can supply the name for an existing repo or it would create a new one with the given name in the env variable.

![Github sycning](img/SyncingWithGithub.png)

### Step 4 : Once the syncing is completed, it triggers a Github action that uploads these files to notion via Notion APIs.
A Github workflow runs in the Github action space. You will get a mail if it fails for some reason. Check the logs for more debugging on that front.

![Github Actions](img/GithubActions.png)

### Step 5 : Voila ! You can now access your notes on Notion too !
If everything goes well, it will update your notion page specified in the env variable.

![Notion Populates](img/Notion%20Populated.png)


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
__(more details below on its access)__
   - Go to www.notion.so/my-integrations
   - Create a new integration
   - Copy the integration token
   
3. **Notion page ID**: 
__(more details below on its access)__
   - Create a new page in Notion
   - Copy the page ID from the URL (it's the part after the page name and after the last '-')

### 📑 Example Configuration Script

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

## 📄 Setting up your notion page
__(Skip this section if you were able to set the notion api tokens and page access  )__

### Step 1 : Create a notion page for storing your Obsidian Vault
The red box highlighted is the Page Id - it is a 32 sized alphanumeric unique ID for the page which starts after the name of your page.

![Notion Page](img/Obsidian_notion_page.png)

### Step 2 : Go to https://www.notion.so/profile/integrations 
You can open it from the settings in your notion app as well.

![Integration](img/Integrations.png)

### Step 3 : Create an integration  
You can use the API tokens of an existing integration as well. Make sure it has the permission to read + write content.

![New Integration](img/NewIntegrations.png)

### Step 4 : Copy this token 
Set this token as your environment variable as mentioned above.

![Copy This token](img/CopyThisToken.png)

### Step 5 : Allow your notion page to gain access
It will not have access to this connection by default.

![Allow page for integration access](img/PageAccessToIntegration.png)


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

# 🧑‍🧑‍🧒‍🧒 Support

If you encounter any issues, please file them on our GitHub repository's issue tracker.

# 🧑‍💻👩‍💻 Contribution

The agenda is to make this package as the easy and smooth package (with lesser bugs ;) for syncing a multitude for note taking applications but firstly achieve a robust two way sync between notion and obsidian.

Please refer to the ![CONTRIBUTING.md](CONTRIBUTING.md) for more details. (TBD with more implementation and design considerations)


# 📂 Directory structure of the project:
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

## License

`obisidian-notion-sync` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.