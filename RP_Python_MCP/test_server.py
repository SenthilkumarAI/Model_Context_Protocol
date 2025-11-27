# https://realpython.com/python-mcp/

# Before connecting your server to an MCP client, it's important to verify 
# that your server is running and that the tools you've created are available to the client.
# To do this, you'll write a unit test that connects to your MCP server in the same way an MCP client would.

import asyncio
import pytest
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = r"D:\MCP\RP_Python_MCP\main.py"
EXPECTED_TOOLS = [
    "get_customer_info",
    "get_order_details",
    "check_inventory",
    "get_customer_ids_by_name",
    "get_orders_by_customer_id",
]

# decorator - allowing pytest to run your asynchronous function in an event loop.
@pytest.mark.asyncio
# asynchronous function, which connects to your server, displays the
# server's tool names and descriptions, and asserts that all or the expected tools are there.
async def test_mcp_server_connection():
    """Connect to an MCP server and verify the tools"""

    # AsyncExitStack object that manages multiple async with contexts for proper cleanup, especially for open connections to your server.
    exit_stack = AsyncExitStack()

    # Here we are connecting our server and initialize a client session.
    # By doing so, you access a host of methods that interact with your server.
    # ====================================================================================
    server_params = StdioServerParameters(command="python", args=[SERVER_PATH], env=None)

    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))

    stdio, write = stdio_transport
    
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))

    await session.initialize()
    # ====================================================================================


    # Here we are making a request to our server to extract the names and descriptions of all the available tools.
    # ====================================================================================
    response = await session.list_tools()
    tools = response.tools
    tool_names = [tool.name for tool in tools]
    tool_descriptions = [tool.description for tool in tools]

    print("\nYour server has the following tools:")
    for tool_name, tool_description in zip(tool_names, tool_descriptions):
        print(f"{tool_name}: {tool_description}")
    # ====================================================================================

    assert sorted(EXPECTED_TOOLS) == sorted(tool_names)
    
    await exit_stack.aclose()