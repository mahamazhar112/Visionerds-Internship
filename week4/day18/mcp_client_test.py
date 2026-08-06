import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-filesystem",
        r"C:\Users\PMLS\Desktop\visionerds-Internship\week4\day18"
    ]
)


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_response = await session.list_tools()
            print("Available tools from the MCP server:\n")
            for tool in tools_response.tools:
                print(f"- {tool.name}")

            print("\n--- Now actually calling a tool ---\n")

            # Call list_directory on day18's own folder
            result = await session.call_tool(
                "list_directory",
                arguments={"path": r"C:\Users\PMLS\Desktop\visionerds-Internship\week4\day18"}
            )

            print("Result from list_directory:")
            for content_item in result.content:
                print(content_item.text)


if __name__ == "__main__":
    asyncio.run(main())