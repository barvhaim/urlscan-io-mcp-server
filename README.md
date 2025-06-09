# MCP Server for `urlscan.io`
_This is not an official `urlscan.io` project!_

<img width="1269" alt="Image" src="https://github.com/user-attachments/assets/5d8e082f-a43e-4900-a612-0aef91f6369c" />

## Usage
```json
{
  "mcpServers": {
    "urlscan_io": {
      "command": "uv",
      "env": {
        "URLSCAN_API_KEY": "xxx"
      },
      "args": [
        "--directory",
        "/PATH/TO/urlscan-io-mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
```
