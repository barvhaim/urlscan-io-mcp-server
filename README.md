# MCP Server for `urlscan.io`
_This is not an official `urlscan.io` project!_

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