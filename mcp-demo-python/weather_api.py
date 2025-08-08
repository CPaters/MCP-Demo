"""
Dummy Weather API
Simulates a weather service with current conditions and forecasts
"""

from datetime import datetime, timedelta
import random
from typing import Dict, List

class WeatherAPI:
    def __init__(self):
        self.weather_conditions = [
            "sunny", "partly cloudy", "cloudy", "light rain", 
            "heavy rain", "thunderstorm", "snow", "foggy"
        ]
        self.city_base_temps = {
            "new york": {"base": 15, "variation": 15},
            "miami": {"base": 25, "variation": 8},
            "denver": {"base": 10, "variation": 20},
            "chicago": {"base": 12, "variation": 18},
            "los angeles": {"base": 22, "variation": 10},
            "seattle": {"base": 13, "variation": 12},
            "phoenix": {"base": 30, "variation": 15},
            "boston": {"base": 14, "variation": 16},
            "san francisco": {"base": 18, "variation": 8},
            "atlanta": {"base": 20, "variation": 12}
        }
    
    def _generate_temperature(self, location: str, season_modifier: float = 0) -> int:
        """Generate realistic temperature for a location"""
        location_lower = location.lower()
        
        # Find matching city or use default
        city_data = None
        for city, data in self.city_base_temps.items():
            if city in location_lower:
                city_data = data
                break
        
        if not city_data:
            city_data = {"base": 20, "variation": 15}  # Default moderate climate
        
        base_temp = city_data["base"] + season_modifier
        variation = city_data["variation"]
        
        return int(base_temp + random.uniform(-variation, variation))
    
    def _get_season_modifier(self) -> float:
        """Get seasonal temperature modifier based on current month"""
        month = datetime.now().month
        if month in [12, 1, 2]:  # Winter
            return -8
        elif month in [3, 4, 5]:  # Spring
            return 2
        elif month in [6, 7, 8]:  # Summer
            return 8
        else:  # Fall
            return -2
    
    def get_current_weather(self, location: str) -> Dict:
        """
        Get current weather for a location
        
        Args:
            location: City name or location
            
        Returns:
            Dictionary with current weather data
        """
        try:
            season_modifier = self._get_season_modifier()
            
            current_weather = {
                "location": location,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "temperature_celsius": self._generate_temperature(location, season_modifier),
                "condition": random.choice(self.weather_conditions),
                "humidity": random.randint(30, 90),
                "wind_speed_kmh": random.randint(0, 40),
                "visibility_km": random.randint(5, 20),
                "uv_index": random.randint(1, 11)
            }
            
            # Convert to Fahrenheit
            current_weather["temperature_fahrenheit"] = int(
                current_weather["temperature_celsius"] * 9/5 + 32
            )
            
            # Add weather-specific details
            if "rain" in current_weather["condition"]:
                current_weather["precipitation_mm"] = random.randint(1, 15)
            elif current_weather["condition"] == "snow":
                current_weather["precipitation_mm"] = random.randint(2, 25)
            else:
                current_weather["precipitation_mm"] = 0
            
            return {
                "success": True,
                "weather": current_weather
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get weather data: {str(e)}"
            }
    
    def get_forecast(self, location: str, days: int = 5) -> Dict:
        """
        Get weather forecast for a location
        
        Args:
            location: City name or location
            days: Number of days to forecast (1-7)
            
        Returns:
            Dictionary with forecast data
        """
        try:
            if days < 1 or days > 7:
                return {
                    "success": False,
                    "error": "Forecast days must be between 1 and 7"
                }
            
            season_modifier = self._get_season_modifier()
            forecast = []
            
            for day in range(days):
                date = datetime.now() + timedelta(days=day)
                
                # Add some day-to-day variation
                daily_variation = random.uniform(-3, 3)
                
                day_weather = {
                    "date": date.strftime("%Y-%m-%d"),
                    "day_of_week": date.strftime("%A"),
                    "temperature_high_celsius": self._generate_temperature(
                        location, season_modifier + daily_variation + 3
                    ),
                    "temperature_low_celsius": self._generate_temperature(
                        location, season_modifier + daily_variation - 3
                    ),
                    "condition": random.choice(self.weather_conditions),
                    "humidity": random.randint(30, 90),
                    "wind_speed_kmh": random.randint(0, 35),
                    "precipitation_chance": random.randint(0, 100)
                }
                
                # Convert to Fahrenheit
                day_weather["temperature_high_fahrenheit"] = int(
                    day_weather["temperature_high_celsius"] * 9/5 + 32
                )
                day_weather["temperature_low_fahrenheit"] = int(
                    day_weather["temperature_low_celsius"] * 9/5 + 32
                )
                
                # Add precipitation amount if chance is high
                if day_weather["precipitation_chance"] > 60:
                    if "rain" in day_weather["condition"]:
                        day_weather["precipitation_mm"] = random.randint(1, 12)
                    elif day_weather["condition"] == "snow":
                        day_weather["precipitation_mm"] = random.randint(2, 20)
                    else:
                        day_weather["precipitation_mm"] = 0
                else:
                    day_weather["precipitation_mm"] = 0
                
                forecast.append(day_weather)
            
            return {
                "success": True,
                "location": location,
                "forecast_days": days,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "forecast": forecast
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get forecast data: {str(e)}"
            }
    
    def get_weather_alerts(self, location: str) -> Dict:
        """
        Get weather alerts for a location
        
        Args:
            location: City name or location
            
        Returns:
            Dictionary with weather alerts
        """
        try:
            # Simulate occasional alerts
            alerts = []
            
            if random.random() < 0.2:  # 20% chance of alerts
                alert_types = [
                    "Severe Thunderstorm Warning",
                    "Heavy Rain Advisory", 
                    "High Wind Warning",
                    "Heat Advisory",
                    "Winter Weather Advisory"
                ]
                
                alert = {
                    "type": random.choice(alert_types),
                    "severity": random.choice(["Minor", "Moderate", "Severe"]),
                    "issued_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "expires_at": (datetime.now() + timedelta(hours=random.randint(6, 48))).strftime("%Y-%m-%d %H:%M:%S"),
                    "description": f"Weather advisory for {location} area. Please take appropriate precautions."
                }
                alerts.append(alert)
            
            return {
                "success": True,
                "location": location,
                "alert_count": len(alerts),
                "alerts": alerts
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get weather alerts: {str(e)}"
            }