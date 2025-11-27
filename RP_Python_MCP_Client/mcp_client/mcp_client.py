import sys
from contextlib import AsyncExitStack
from typing import Any, Awaitable, Callable, ClassVar, Self

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# The below class is used to manage communication with the target MCP server.
# You’ll handle this communication through .client_session, which is a class 
# attribute that holds an instance of mcp.ClientSession.
class MCPClient:
    """MCP client to interact with MCP server.

    Usage:
        async with MCPClient(server_path) as client:
            # Call client methods here...
    """

    client_session: ClassVar[ClientSession]

    def __init__(self, server_path: str):
        self.server_path = server_path
        # AsyncExitStack is a context manager from Python’s contextlib module that allows you to 
        # programmatically manage multiple asynchronous context managers. 
        # You need this class to manage the stdio client and its session.
        self.exit_stack = AsyncExitStack()

    # Since we are going to use MCPClient class as an asynchronous context manager, we need to 
    # implement the .__aenter__() and .__aexit__() special methods.


    # The .__aenter__() method runs when the async with statement enters the target context. 
    # This is a good time to create the client session, which you do by calling the ._connect_to_server() helper method. 

    # Because .client_session is a class attribute, you use the class object (cls) to assign it a value. 
    # Note that using self (argument) instead of cls (argument) will create a new instance attribute, rather than referring to the class attribute.
    # The .client_session attribute allows you to create and manage a client session 
    # over standard input/output (I/O) using the stdio_client() function.
    async def __aenter__(self) -> Self:
        cls = type(self)
        cls.client_session = await self._connect_to_server()
        return self

    # The .__aexit__() method is called automatically when the async with statement exits. 
    # This is the right moment to close the client session: call .aclose() on the AsyncExitStack 
    # and await it asynchronously to release the resources cleanly.
    async def __aexit__(self, *_) -> None:
        await self.exit_stack.aclose()

    # In this method we are establishing a connection between MCPClient and an MCP Server.
    async def _connect_to_server(self) -> ClientSession:
        print("Connecting to server...")
        try:
            # We use the .exit_stack object to enter an asynchronous context and access the 
            # read and write streams of your client’s standard I/O.
            read, write = await self.exit_stack.enter_async_context(
                stdio_client(
                    server=StdioServerParameters(
                        command="sh", # Shell command
                        args=[
                            "-c", # to execute the a string as command
                            f"{sys.executable} {self.server_path} 2>/dev/null", # 2>/dev/null bit redirects any error output so the terminal window doesn’t get cluttered.
                        ],
                        env=None,
                    )
                )
            )
            # We pass the read and write communication channels to the ClientSession class, which manages the communication session.
            client_session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            # Finally, you initialize the session and return it to the caller.
            await client_session.initialize()
            return client_session
        except Exception:
            raise RuntimeError("Error: Failed to connect to server")
    
    """
    The AsyncExitStack instance enables you to maintain the stdio client and its session in context throughout the app’s execution. 
    You only exit both contexts when you call .exit_stack.aclose() in the .__aexit__() method.

    If any step fails, you raise a RuntimeError to indicate that the connection attempt was unsuccessful. 
    Note that catching the broad Exception class isn’t a best practice in Python. 
    However, in this example, you use this exception for the sake of simplicity and convenience.
    """