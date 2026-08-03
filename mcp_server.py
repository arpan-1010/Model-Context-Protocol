import logging

from mcp.server.fastmcp import FastMCP
from tools import calculator_tool, weather_tool, tensor_tool

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("mcp_server")

mcp = FastMCP("my-mcp-server")

mcp.tool()(calculator_tool)
mcp.tool()(weather_tool)
mcp.tool()(tensor_tool)

if __name__ == "__main__":
    logger.info("Starting MCP server on stdio...")
    mcp.run(transport="stdio")