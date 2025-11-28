Link :
https://realpython.com/python-mcp/

Python version:
3.12.5

Requirements :
mcp[cli] == 1.22.0
pytest-asyncio == 1.3.0

Description :
	Here we are using the host as Cursor IDE.
	Open Cursor -> Settings -> Tools & MCP -> New MCP Server -> Enter the below json string
	
	{
  "mcpServers": {
    "ecommerce_db_server": {
      "command": "C:\\Users\\envs\\GenAI\\Scripts\\python", (Path to python.exe)
      "args": ["D:\\MCP\\Model_Context_Protocol\\RP_Python_MCP\\main.py"],
      "description": "A set of tools that you can use to look up customer, order, and product information in a transactional database"
    }
  }
}


