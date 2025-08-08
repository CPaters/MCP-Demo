from pydantic import BaseModel, Field
from typing import Annotated
from fastmcp import FastMCP
from hotel_api import HotelAPI
from weather_api import WeatherAPI

mcp  = FastMCP(name="Hotel & Weather API Server")

hotel_api = HotelAPI()
weather_api = WeatherAPI()

# ------------------ HOTEL TOOLS ------------------ #

@mcp.tool
def search_hotels(location:Annotated[str, Field(..., description="city or location")], 
                 check_in: Annotated[str, Field(..., description="Check-in date YYYY-MM-DD")], 
                 check_out: Annotated[str, Field(..., description="Check-out date YYYY-MM-DD")], 
                 guests: Annotated[int, Field(..., ge=1, description="number of guests")] ) -> str:
    """Search for available hotels in a location for specific dates"""
    result = hotel_api.search_hotels(location, check_in, check_out, guests)
    if result["success"]:
        response_text = f"Found {result['hotels_found']} hotels in {result['location']}:\n\n"
        for hotel in result["hotels"]:
            response_text += f"🏨 **{hotel['name']}**\n"
            response_text += f"   📍 {hotel['location']}\n"
            response_text += f"   💰 ${hotel['price_per_night']}/night (Total: ${hotel['total_price']} for {hotel['nights']} nights)\n"
            response_text += f"   ⭐ Rating: {hotel['rating']}/5\n"
            response_text += f"   🛏️ Available rooms: {hotel['available_rooms']}\n"
            response_text += f"   🎯 Hotel ID: {hotel['id']}\n"
            response_text += f"   ✨ Amenities: {', '.join(hotel['amenities'])}\n\n"
            
        return response_text
    return f"❌ {result['error']}"


@mcp.tool
def book_hotel(hotel_id: str, check_in:str, check_out:str, guests:Annotated[int, Field(..., ge=1)], guest_name:str, guest_email:str) -> str:
    """Book a hotel room"""
    result = hotel_api.book_hotel(hotel_id, check_in, check_out, guests, guest_name, guest_email)
    if result["success"]:
        booking = result["booking"]
        response_text = f"🎉 **Booking Confirmed!**\n\n"
        response_text += f"📋 **Booking ID:** {booking['booking_id']}\n"
        response_text += f"🏨 **Hotel:** {booking['hotel_name']}\n"
        response_text += f"📍 **Location:** {booking['hotel_location']}\n"
        response_text += f"📅 **Check-in:** {booking['check_in']}\n"
        response_text += f"📅 **Check-out:** {booking['check_out']}\n"
        response_text += f"🌙 **Nights:** {booking['nights']}\n"
        response_text += f"👥 **Guests:** {booking['guests']}\n"
        response_text += f"👤 **Guest Name:** {booking['guest_name']}\n"
        response_text += f"📧 **Email:** {booking['guest_email']}\n"
        response_text += f"💰 **Total Price:** ${booking['total_price']}\n"
        return response_text
    return f"❌ Booking failed: {result['error']}"

@mcp.tool
def get_booking(booking_id : str) -> str:
    """Retrieve booking by ID"""
    result = hotel_api.get_booking(booking_id)
    if result["success"]:
        booking = result["booking"]
        response_text = f"📋 **Booking Details**\n\n"
        response_text += f"🆔 **Booking ID:** {booking['booking_id']}\n"
        response_text += f"🏨 **Hotel:** {booking['hotel_name']}\n"
        response_text += f"📍 **Location:** {booking['hotel_location']}\n"
        response_text += f"📅 **Check-in:** {booking['check_in']}\n"
        response_text += f"📅 **Check-out:** {booking['check_out']}\n"
        response_text += f"💰 **Total Price:** ${booking['total_price']}\n"
        return response_text
    return f"❌ {result['error']}"

# ------------------ WEATHER TOOLS ------------------ #

@mcp.tool
def get_current_weather(location:str) -> str:
    """Get current weather for a location"""
    result = weather_api.get_current_weather(location)
    if result["success"]:
        weather = result["weather"]
        response_text = f"🌤️ **Current Weather in {weather['location']}**\n\n"
        response_text += f"🌡️ **Temperature:** {weather['temperature_celsius']}°C ({weather['temperature_fahrenheit']}°F)\n"
        response_text += f"☁️ **Condition:** {weather['condition'].title()}\n"
        response_text += f"💧 **Humidity:** {weather['humidity']}%\n"
        response_text += f"💨 **Wind Speed:** {weather['wind_speed_kmh']} km/h\n"
        if weather.get('precipitation_mm', 0) > 0:
            response_text += f"🌧️ **Precipitation:** {weather['precipitation_mm']} mm\n"
        return response_text
    return f"❌ {result['error']}"


@mcp.tool
def get_weather_forecast(location: str, 
                         days: Annotated[int,Field(description="Number of days of forecast needed", ge=1, le=7)]=5 ) -> str:
    """Weather forecast for a location for given number of days. Defaults to 5 days."""
    result = weather_api.get_forecast(location, days)
    if result["success"]:
        response_text = f"📅 **{days}-Day Weather Forecast for {result['location']}**\n\n"
        for day in result["forecast"]:
            response_text += f"📆 **{day['day_of_week']}, {day['date']}**\n"
            response_text += f"   🌡️ High: {day['temperature_high_celsius']}°C ({day['temperature_high_fahrenheit']}°F)\n"
            response_text += f"   🌡️ Low: {day['temperature_low_celsius']}°C ({day['temperature_low_fahrenheit']}°F)\n"
            response_text += f"   ☁️ Condition: {day['condition'].title()}\n"
            response_text += f"   🌧️ Rain Chance: {day['precipitation_chance']}%\n\n"
    else: 
        response_text = f"❌ {result['error']}"
    return response_text

@mcp.tool
def get_weather_alerts(location:str) -> str:
    """Weather alerts for a location"""
    result = weather_api.get_weather_alerts(location)
    if result["success"]:
        if result["alert_count"] > 0:
            response_text = f"⚠️ **Weather Alerts for {result['location']}** ({result['alert_count']} active)\n\n"
            for alert in result["alerts"]:
                severity_emoji = {"Minor": "🟡", "Moderate": "🟠", "Severe": "🔴"}.get(alert["severity"], "⚠️")
                response_text += f"{severity_emoji} **{alert['type']}** ({alert['severity']})\n"
                response_text += f"   📄 {alert['description']}\n\n"
            return response_text
        else:
            return f"✅ **No Weather Alerts** for {result['location']}\n\nAll clear!"
    return f"❌ {result['error']}"

if __name__ == '__main__':
    print("🚀 Starting Hotel & Weather API Server...")
    print("📡 Server will be available at http://localhost:5000/mcp")
    print("🛠️ Available endpoints:")
    print("   GET /tools - List available tools")
    print("   POST /call/<tool_name> - Call a specific tool")
    print("   GET /health - Health check")
    mcp.run(transport="http", host="127.0.0.1", port=5000)
