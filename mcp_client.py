import asyncio
import logging

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("mcp_client")

async def main():
    server_params = StdioServerParameters(command="python", args=["mcp_server.py"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()
            logger.info("Session initialized")

            tools = await session.list_tools()
            logger.info("Available tools: %s", [t.name for t in tools.tools])

            calc = await session.call_tool(
                "calculator_tool",
                {"expression": "25 * (10 + 2)"}
            )
            logger.info("Calculator result: %s", calc.content[0].text)

            weather = await session.call_tool(
                "weather_tool",
                {"city": "Kolkata"}
            )
            logger.info("Weather result: %s", weather.content[0].text)

            tensor = await session.call_tool(
                "tensor_tool",
                {"operation": "norm", "size": 5}
            )
            logger.info("Tensor result: %s", tensor.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())