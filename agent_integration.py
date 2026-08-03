import asyncio
import logging
import re

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("simple_agent")

class SimpleAgent:

    async def run_task(self, city: str):

        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:

                await session.initialize()
                logger.info("Agent started for city=%r", city)

                weather = await session.call_tool(
                    "weather_tool",
                    {"city": city}
                )
                weather_text = weather.content[0].text
                logger.info("[Step 1] Weather: %s", weather_text)

                match = re.search(r"(-?\d+(?:\.\d+)?)\s*°C", weather_text)
                if not match:
                    logger.error("Could not parse temperature from: %s", weather_text)
                    return
                temp = float(match.group(1))

                expression = f"{temp} * 1.5 + 10"
                calc = await session.call_tool(
                    "calculator_tool",
                    {"expression": expression}
                )
                calc_text = calc.content[0].text
                logger.info("[Step 2] Calculation: %s", calc_text)

                tensor = await session.call_tool(
                    "tensor_tool",
                    {"operation": "mean", "size": 8}
                )
                tensor_text = tensor.content[0].text
                logger.info("[Step 3] Tensor Analysis: %s", tensor_text)

                logger.info(
                    "Final Agent Report | City: %s | %s | %s | %s",
                    city, weather_text, calc_text, tensor_text,
                )


async def main():
    agent = SimpleAgent()
    await agent.run_task("Kolkata")


if __name__ == "__main__":
    asyncio.run(main())