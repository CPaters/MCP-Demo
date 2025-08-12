from pydantic import Field
from typing import Annotated
from fastmcp import FastMCP
import httpx

mcp  = FastMCP(name="Hotel & Weather API MCP Server")

API_BASE = "http://127.0.0.1:8000"


def _fmt_hotels(data: dict) -> str:
    if not data.get("success"):
        return f"❌ {data.get('error', 'Unknown error')}"
    lines = [f"Found {data['hotels_found']} hotels in {data['location']}:\n"]
    for hotel in data.get("hotels", []):
        lines.append(f"🏨 **{hotel['name']}**")
        lines.append(f"   📍 {hotel['location']}")
        lines.append(    f"   💰 ${hotel['price_per_night']}/night (Total: ${hotel['total_price']} for {hotel['nights']} nights)")
        lines.append(    f"   ⭐ Rating: {hotel['rating']}/5")
        lines.append(    f"   🛏️ Available rooms: {hotel['available_rooms']}")
        lines.append(    f"   🎯 Hotel ID: {hotel['id']}")
        lines.append(    f"   ✨ Amenities: {', '.join(hotel.get('amenities', []))}\n")

    return "\n".join([ln for ln in lines if ln])

def _fmt_booking(data: dict) -> str:
    if not data.get("success"):
        return f"❌ {data.get('error', 'Unknown error')}"
    b = data["booking"]
    lines = [
        "🎉 **Booking Confirmed!**\n",
        f"📋 **Booking ID:** {b['booking_id']}",
        f"🏨 **Hotel:** {b['hotel_name']}",
        f"📍 **Location:** {b['hotel_location']}",
        f"📅 **Check-in:** {b['check_in']}",
        f"📅 **Check-out:** {b['check_out']}",
        f"🌙 **Nights:** {b.get('nights', '')}",
        f"👥 **Guests:** {b['guests']}",
        f"👤 **Guest Name:** {b.get('guest_name','')}",
        f"📧 **Email:** {b.get('guest_email','')}",
        f"💰 **Total Price:** ${b['total_price']}",
    ]
    return "\n".join([ln for ln in lines if ln])

def _format_current_weather(data: dict) -> str:
    if not data.get("success"):
        return f"❌ {data.get('error', 'Unknown error')}"
    weather = data["weather"]
    lines = [
        f"🌤️ **Current Weather in {weather['location']}**",
        f"🌡️ **Temperature:** {weather['temperature_celsius']}°C ({weather['temperature_fahrenheit']}°F)\n",
        f"☁️ **Condition:** {weather['condition'].title()}\n",
        f"💧 **Humidity:** {weather['humidity']}%\n",
        f"💨 **Wind Speed:** {weather['wind_speed_kmh']} km/h\n"
    ]
    if weather.get('precipitation_mm', 0) > 0:
        lines.append(f"🌧️ **Precipitation:** {weather['precipitation_mm']} mm\n")
    
    return "\n".join([ln for ln in lines if ln])

def _format_weather_forecast(data: dict, days: int) -> str:
    if not data.get("success"):
        return f"❌ {data.get('error', 'Unknown error')}"
    
    location = data["location"]
    days = data["forecast_days"]  #Prefer API's value
    items = data["forecast"]

    lines = [f"🌤️ **Weather Forecast for {location}** ({days} days):\n"]
    
    for day in items:
        lines.append(f"📅 **{day['date']}**")
        lines.append(f"   🌡️ **Temperature (low):** {day['temperature_low_celsius']}°C ({day['temperature_low_fahrenheit']}°F)")
        lines.append(f"   🌡️ **Temperature (high):** {day['temperature_high_celsius']}°C ({day['temperature_high_fahrenheit']}°F)")
        lines.append(f"   ☁️ **Condition:** {day['condition'].title()}")
        if day.get('precipitation_mm', 0) > 0:
            lines.append(f"   🌧️ **Precipitation:** {day['precipitation_mm']} mm")
        lines.append("")  # Blank line for separation
    
    return "\n".join(lines)
    
def _format_weather_alerts(data: dict) -> str:
    if not data.get("success"):
        return f"❌ {data.get('error', 'Unknown error')}"
    
    lines = [f"⚠️ **Weather Alerts for {data['location']}** ({data['alert_count']} active)\n\n"]
    for alert in data["alerts"]:
        severity_emoji = {"Minor": "🟡", "Moderate": "🟠", "Severe": "🔴"}.get(alert["severity"], "⚠️")
        lines.append(f"{severity_emoji} **{alert['type']}** ({alert['severity']})\n")
        lines.append(f"   📄 {alert['description']}\n\n")
    return "\n".join([ln for ln in lines if ln])


# ------------------ HOTEL TOOLS ------------------ #

@mcp.tool
def search_hotels(location:Annotated[str, Field(..., description="city or location")], 
                 check_in: Annotated[str, Field(..., description="Check-in date YYYY-MM-DD")], 
                 check_out: Annotated[str, Field(..., description="Check-out date YYYY-MM-DD")], 
                 guests: Annotated[int, Field(..., ge=1, description="number of guests")] ) -> str:
    """Search for available hotels in a location for specific dates and number of guests."""
    with httpx.Client(base_url=API_BASE, timeout=30.0) as http:
        r = http.post("/hotel/search", json={
            "location": location, "check_in": check_in, "check_out": check_out, "guests": guests
        })
        data = r.json() 
    return _fmt_hotels(data)


@mcp.tool
def book_hotel(hotel_id: str, check_in:str, check_out:str, guests:Annotated[int, Field(..., ge=1)], guest_name:str, guest_email:str) -> str:
    """Book a hotel room"""
    with httpx.Client(base_url=API_BASE, timeout=30.0) as http:
        r = http.post("/hotel/book", json={
            "hotel_id": hotel_id, "check_in": check_in, "check_out": check_out, 
            "guests": guests, "guest_name": guest_name, "guest_email": guest_email
        })
        data = r.json()
    return _fmt_booking(data) if data.get("success") else f"❌ Booking failed: {data.get('error','Unknown error')}"


@mcp.tool
def get_booking(booking_id : str) -> str:
    """Retrieve booking by ID"""
    with httpx.Client(base_url=API_BASE, timeout=30.0) as http:
        r = http.post(f"/hotel/booking/{booking_id}")
        data = r.json()
    return _fmt_booking(data) if data.get("success") else f"❌ {data.get('error', 'Unknown error')}"

# ------------------ WEATHER TOOLS ------------------ #

@mcp.tool
def get_current_weather(location:str) -> str:
    """Get current weather for a location"""
    with httpx.Client(base_url=API_BASE, timeout=30.0) as http:
        r = http.get("/weather/current", params={"location": location})
        data = r.json()
    return _format_current_weather(data) if data.get("success") else f"❌ {data.get('error', 'Unknown error')}"




@mcp.tool
def get_weather_forecast(location: str, 
                         days: Annotated[int,Field(description="Number of days of forecast needed", ge=1, le=7)]=5 ) -> str:
    """Weather forecast for a location for given number of days. Defaults to 5 days."""
    with httpx.Client(base_url=API_BASE, timeout=30.0) as http:
        r = http.get("/weather/forecast", params={"location": location, "days": days})
        data = r.json()
    return _format_weather_forecast(data, days) if data.get("success") else f"❌ {data.get('error', 'Unknown error')}"


@mcp.tool
def get_weather_alerts(location:str) -> str:
    """Weather alerts for a location"""
    with httpx.Client(base_url=API_BASE, timeout=30.0) as http:
        r = http.get("/weather/alerts", params={"location": location})
        data = r.json()
    return _format_weather_alerts(data) if data.get("success") else f"❌ {data.get('error', 'Unknown error')}"


if __name__ == '__main__':
    print("🚀 Starting Hotel & Weather API Server...")
    print("📡 Server will be available at http://localhost:5000/mcp")
    mcp.run(transport="http", host="127.0.0.1", port=5000)
