from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

NWS_API_URL = "https://api.weather.gov/"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            mcp.logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            mcp.logger.error(f"Request error: {e}")
        except Exception as e:
            mcp.logger.error(f"Unexpected error: {e}")
    return None

def format_alert(feature: dict) -> str:
    props = feature["properties"]
    return f"""
    Event: {props.get("event", "Unknown Event")}
    Area: {props.get("areaDesc", "Unknown Area")}
    Severity: {props.get("severity", "Unknown Severity")}
    Description: {props.get("description", "No description available")}
    Instruction: {props.get("instruction", "No instruction available")}
    """

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a state.

    Args:
        state (str): The two-letter state abbreviation.
    """

    if len(state) != 2:
        return "Invalid state abbreviation. Please provide a two-letter state code."

    url = f"{NWS_API_URL}alerts/active?area={state.upper()}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "No active alerts found or an error occurred."

    alerts = data["features"]
    if not alerts:
        return "No active alerts found."

    formatted_alerts = "\n".join(format_alert(alert) for alert in alerts)
    return f"Active weather alerts for {state.upper()}:\n{formatted_alerts}"


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get the weather forecast for a specific latitude and longitude.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
    """

    url = f"{NWS_API_URL}/points/{latitude},{longitude}"
    data = await make_nws_request(url)

    if not data or "properties" not in data:
        return "No forecast data found or an error occurred."

    forecast = data["properties"].get("periods", [])
    if not forecast:
        return "No forecast available for the specified location."

    formatted_forecast = "\n".join(
        f"{period['name']}: {period['detailedForecast']}" for period in forecast
    )
    return f"Weather forecast:\n{formatted_forecast}"


if __name__ == "__main__":
    mcp.run(transport="stdio")