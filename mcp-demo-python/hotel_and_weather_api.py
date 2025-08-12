from fastapi import FastAPI 
from pydantic import BaseModel, Field
from hotel import Hotel 
from weather import Weather

app = FastAPI(title="Hotel Booking API", description="API for searching and booking hotels")
_hotel = Hotel()
_weather = Weather()

class SearchHotelsRequest(BaseModel):
    location: str = Field(..., description="City or location")
    check_in: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    check_out: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    guests: int = Field(..., ge=1)

class BookHotelRequest(BaseModel):
    hotel_id: str
    check_in: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    check_out: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    guests: int = Field(..., ge=1)
    guest_name: str
    guest_email: str


@app.get("/hotel/health")
def hotel_health():
    """Health check endpoint"""
    return {
        "ok": True,
        "status": "ok"
    }

@app.post("/hotel/search")
def search_hotels(request: SearchHotelsRequest):
    """Search for available hotels in a location for specific dates"""
    return _hotel.search_hotels(request.location, request.check_in, request.check_out, request.guests)

@app.post("/hotel/book")
def book_hotel(request: BookHotelRequest):
    """Book a hotel room"""
    return _hotel.book_hotel(
        request.hotel_id, 
        request.check_in, 
        request.check_out, 
        request.guests, 
        request.guest_name, 
        request.guest_email
    )

@app.post("/hotel/booking/{booking_id}")
def get_booking(booking_id: str):
    """Retrieve booking details by booking ID"""
    return _hotel.get_booking(booking_id)

# ------------------ WEATHER APIs ------------------ #

@app.get("/weather/health")
def weather_health():
    """Health check endpoint"""
    return {
        "ok": True,
        "status": "ok"
    }

@app.get("/weather/current")
def get_current_weather(location: str):
    """Get current weather for a location"""
    return _weather.get_current_weather(location)

@app.get("/weather/forecast")
def get_weather_forecast(location: str, days: int = 5):
    """Weather forecast for a location for given number of days. Defaults to 5 days."""
    print("In API: Getting weather forecast for", location, "for", days, "days")
    return _weather.get_forecast(location, days)    

@app.get("/weather/alerts")
def get_weather_alerts(location: str):
    """Weather alerts for a location"""
    return _weather.get_weather_alerts(location)    