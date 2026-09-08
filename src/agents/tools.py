import datetime as dt
import json
from urllib.parse import urlencode
from urllib.request import urlopen

import pytz
from smolagents import DuckDuckGoSearchTool, FinalAnswerTool, tool

WEATHER_DESCRIPTIONS = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}


@tool
def get_weather(location: str) -> str:
    """Get the current weather for a city or place using Open-Meteo.

    Args:
        location: A city or place name, such as 'Buga, Colombia'.
    """
    try:
        geocode_query = urlencode({"name": location, "count": 1, "language": "en", "format": "json"})
        with urlopen(
            f"https://geocoding-api.open-meteo.com/v1/search?{geocode_query}",
            timeout=10,
        ) as response:
            places = json.load(response).get("results", [])
        if not places:
            return f"I could not find a location named {location}."

        place = places[0]
        forecast_query = urlencode(
            {
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                "timezone": "auto",
            }
        )
        with urlopen(
            f"https://api.open-meteo.com/v1/forecast?{forecast_query}",
            timeout=10,
        ) as response:
            current = json.load(response)["current"]
    except (OSError, KeyError, json.JSONDecodeError) as error:
        return f"I could not retrieve weather for {location}: {error}"

    weather_code = current["weather_code"]
    description = WEATHER_DESCRIPTIONS.get(weather_code, "unknown conditions")
    return (
        f"Current weather in {place['name']}, {place.get('country', '')}: "
        f"temperature {current['temperature_2m']}°C; "
        f"humidity {current['relative_humidity_2m']}%; "
        f"wind {current['wind_speed_10m']} km/h; "
        f"conditions {description}."
    )


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """Get the current local time in an IANA timezone.

    Args:
        timezone: A timezone such as 'America/New_York' or 'Europe/London'.
    """
    try:
        local_time = dt.datetime.now(pytz.timezone(timezone))
    except pytz.UnknownTimeZoneError:
        return f"Unknown timezone: {timezone}"

    return f"The current local time in {timezone} is {local_time:%Y-%m-%d %H:%M:%S %Z}."


def build_tools() -> list:
    """Create the tools exposed to the code agent."""
    return [
        FinalAnswerTool(),
        DuckDuckGoSearchTool(max_results=5),
        get_weather,
        get_current_time_in_timezone,
    ]
