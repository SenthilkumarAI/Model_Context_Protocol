from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp_server")

@mcp.tool()
async def echo(message: str) -> str:
    """Echo back the message."""
    return message

@mcp.prompt()
async def greeting_prompt(name: str) -> str:
    """A simple greeting prompt."""
    return f"Greet {name} kindly."

@mcp.resource("file://./greeting.txt")
def greeting_file() -> str:
    """The greeting text file."""
    with open("greeting.txt", "r", encoding="utf-8") as file:
        return file.read()

if __name__ == "__main__":
    mcp.run(transport="stdio")

"""
Note: MCP supports two transport mechanisms:

Stdio transport: 
Uses standard input/output streams for direct communication between 
local processes on the same machine.

Streamable HTTP transport: 
Uses HTTP POST requests for client-to-server messages, enabling communication 
with remote servers.
"""