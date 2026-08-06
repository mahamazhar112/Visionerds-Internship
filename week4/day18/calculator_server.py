from mcp.server.fastmcp import FastMCP

# Create the MCP server, give it a name
mcp = FastMCP("calculator-server")


@mcp.tool()
def calculator(a: float, b: float, operation: str) -> str:
    """
    Performs basic math operations: add, subtract, multiply, divide.

    Args:
        a: first number
        b: second number
        operation: one of '+', '-', '*', '/'
    """
    if operation == '+':
        result = a + b
    elif operation == '-':
        result = a - b
    elif operation == '*':
        result = a * b
    elif operation == '/':
        if b == 0:
            return "Error, cannot divide by zero"
        result = a / b
    else:
        return f"Unknown operation: {operation}"

    return str(result)


if __name__ == "__main__":
    mcp.run(transport="stdio")