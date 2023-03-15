from mcp.server.fastmcp import FastMCP

# Minimal MCP server to verify MCP connectivity from Trae
mcp = FastMCP("LangChainDemo")

@mcp.tool()
def ping(message: str) -> str:
    """Echo tool: returns 'pong: <message>'"""
    return f"pong: {message}"

@mcp.tool()
def soma(a: float, b: float) -> float:
    """Soma dois números (a + b)."""
    return a + b

if __name__ == "__main__":
    # Use stdio transport so Trae MCP can spawn this as a subprocess
    mcp.run(transport="stdio")