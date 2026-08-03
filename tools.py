import ast
import logging
import operator
import random

import requests
import torch

logger = logging.getLogger("mcp_tools")

_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def _safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported or unsafe expression")

def calculator_tool(expression: str) -> str:
    logger.info("calculator_tool called with expression=%r", expression)
    try:
        result = _safe_eval(ast.parse(expression, mode="eval").body)
        logger.debug("calculator_tool result=%s", result)
        return f"Result : {result}"
    except Exception as e:
        logger.warning("calculator_tool failed: %s", e)
        return f"Calculator Error: {e}"

_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

_WMO_CONDITIONS = {
    0: "Clear",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light Drizzle",
    61: "Light Rain",
    63: "Rain",
    65: "Heavy Rain",
    71: "Light Snow",
    73: "Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    95: "Thunderstorm",
}

def weather_tool(city: str) -> str:
    logger.info("weather_tool called with city=%r", city)
    try:
        geo_resp = requests.get(_GEOCODE_URL, params={"name": city, "count": 1}, timeout=5)
        geo_resp.raise_for_status()
        results = geo_resp.json().get("results")
        if not results:
            logger.warning("weather_tool: no geocoding match for city=%r", city)
            return f"Weather Error: could not find location '{city}'"

        lat, lon = results[0]["latitude"], results[0]["longitude"]
        resolved_name = results[0].get("name", city)

        weather_resp = requests.get(
            _FORECAST_URL,
            params={"latitude": lat, "longitude": lon, "current_weather": True},
            timeout=5,
        )
        weather_resp.raise_for_status()
        current = weather_resp.json()["current_weather"]

        temp = current["temperature"]
        condition = _WMO_CONDITIONS.get(current["weathercode"], "Unknown")

        logger.debug("weather_tool result: temp=%s condition=%s", temp, condition)
        return f"Weather in {resolved_name} : {temp}°C, {condition}"

    except requests.RequestException as e:
        logger.error("weather_tool: API request failed (%s), falling back to mock data", e)
        return _mock_weather(city)
    except (KeyError, IndexError) as e:
        logger.error("weather_tool: unexpected API response shape (%s)", e)
        return _mock_weather(city)


def _mock_weather(city: str) -> str:
    temp = random.randint(20, 40)
    condition = random.choice(["Sunny", "Cloudy", "Rainy"])
    logger.info("weather_tool: using mock data for city=%r", city)
    return f"Weather in {city} : {temp}°C, {condition} (mock data)"

def tensor_tool(operation: str, size: int = 4) -> str:
    logger.info("tensor_tool called with operation=%r size=%s", operation, size)

    if size < 1:
        logger.warning("tensor_tool: invalid size=%s", size)
        return "Error: size must be a positive integer"

    x = torch.randn(size, size)
    if operation == "mean":
        result = f"Tensor mean : {x.mean().item(): .4f}"
    elif operation == "norm":
        result = f"Tensor L2 norm : {torch.norm(x).item(): .4f}"
    elif operation == "eigen":
        sym = (x + x.T) / 2
        vals = torch.linalg.eigvals(sym).real
        rounded = [round(v, 4) for v in vals.tolist()]
        result = f"Eigen Value : {rounded}"
    else:
        logger.warning("tensor_tool: unknown operation=%r", operation)
        result = "Unknown operation. Use : mean, norm, eigen"

    logger.debug("tensor_tool result=%s", result)
    return result