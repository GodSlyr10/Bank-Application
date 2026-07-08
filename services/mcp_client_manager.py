from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters,
)

from langchain_mcp_adapters.tools import load_mcp_tools



class MCPClientManager:

    def __init__(self, servers: dict):

        self.servers = servers
        self.exit_stack = AsyncExitStack()
        self.sessions = []


    async def connect(self):

        all_tools = []


        for name, server in self.servers.items():

            print(
                f"Connecting to MCP server: {name}"
            )


            server_params = StdioServerParameters(
                command=server["command"],
                args=server["args"],
            )


            read, write = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )


            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )


            await session.initialize()


            self.sessions.append(session)


            tools = await load_mcp_tools(
                session
            )


            print(
                f"Loaded {len(tools)} tools from {name}"
            )


            all_tools.extend(tools)


        return all_tools



    async def close(self):

        await self.exit_stack.aclose()