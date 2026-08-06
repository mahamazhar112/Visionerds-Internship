import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["calculator_server.py"]
)


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_response = await session.list_tools()
            print("Available tools from YOUR OWN MCP server:\n")
            for tool in tools_response.tools:
                print(f"- {tool.name}: {tool.description}")

            print("\n--- Calling your calculator tool ---\n")

            result = await session.call_tool(
                "calculator",
                arguments={"a": 47, "b": 89, "operation": "*"}
            )

            print("Result:")
            for content_item in result.content:
                print(content_item.text)


if __name__ == "__main__":
    asyncio.run(main())