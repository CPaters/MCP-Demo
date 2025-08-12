"""
Dummy Hotel Booking API
Simulates a hotel booking system with search and booking capabilities
"""

from datetime import datetime
from typing import List, Dict, Optional
import random
import uuid

class Hotel:
    def __init__(self):
        self.hotels = self._generate_dummy_hotels()
        self.bookings = {}
   
    def _generate_dummy_hotels(self) -> List[Dict]:
        """Generate dummy hotel data"""
        hotels = [
            {
                "id": "hotel_001",
                "name": "Grand Plaza Hotel",
                "location": "New York",
                "price_per_night": 299.99,
                "rating": 4.5,
                "amenities": ["WiFi", "Pool", "Gym", "Room Service"],
                "available_rooms": 15
            },
            {
                "id": "hotel_002", 
                "name": "Sunset Beach Resort",
                "location": "Miami",
                "price_per_night": 199.99,
                "rating": 4.2,
                "amenities": ["Beach Access", "WiFi", "Pool", "Spa"],
                "available_rooms": 8
            },
            {
                "id": "hotel_003",
                "name": "Mountain View Lodge",
                "location": "Denver",
                "price_per_night": 149.99,
                "rating": 4.0,
                "amenities": ["WiFi", "Fireplace", "Hiking Trails"],
                "available_rooms": 12
            },
            {
                "id": "hotel_004",
                "name": "City Center Inn",
                "location": "Chicago",
                "price_per_night": 179.99,
                "rating": 3.8,
                "amenities": ["WiFi", "Business Center", "Parking"],
                "available_rooms": 20
            },
            {
                "id": "hotel_005",
                "name": "Luxury Suites",
                "location": "Los Angeles",
                "price_per_night": 399.99,
                "rating": 4.8,
                "amenities": ["WiFi", "Pool", "Spa", "Concierge", "Valet"],
                "available_rooms": 5
            },
             {
                "id": "hotel_005",
                "name": "Marriot Hotel",
                "location": "New York",
                "price_per_night": 399.99,
                "rating": 4.7,
                "amenities": ["WiFi", "Gym", "Room Service"],
                "available_rooms": 15
            }
        ]
        return hotels

  
    def search_hotels(self, location: str, check_in: str, check_out: str, guests: int) -> Dict:
        """
        Search for available hotels
        
        Args:
            location: City name
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)
            guests: Number of guests
        
        Returns:
            Dictionary with search results
        """
        try:
            # Parse dates
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
           
            if check_out_date <= check_in_date:
                return {
                    "success": False,
                    "error": "Check-out date must be after check-in date"
                }
            
            nights = (check_out_date - check_in_date).days
            
            # Filter hotels by location (case insensitive)
            matching_hotels = [
                hotel for hotel in self.hotels 
                if location.lower() in hotel["location"].lower()
            ]
            
            # Simulate availability based on guests and random factors
            available_hotels = []
            for hotel in matching_hotels:
                if hotel["available_rooms"] >= guests and random.random() > 0.1:  
                    total_price = hotel["price_per_night"] * nights
                    available_hotels.append({
                        **hotel,
                        "total_price": total_price,
                        "nights": nights,
                        "price_breakdown": f"${hotel['price_per_night']}/night x {nights} nights"
                    })
            
            return {
                "success": True,
                "location": location,
                "check_in": check_in,
                "check_out": check_out,
                "guests": guests,
                "nights": nights,
                "hotels_found": len(available_hotels),
                "hotels": available_hotels
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Search failed: {str(e)}"
            }
        
    def get_hotel(self, hotel: str) -> Optional[Dict]:
        """
        Get hotel details by ID
        
        Args:
            hotel: Hotel name
        
        Returns:
            Hotel id
        """
        hotel_lower = hotel.lower()
        return next((h for h in self.hotels if hotel_lower in h["name"].lower()), None)
    
    
    def book_hotel(self, hotel_id: str, check_in: str, check_out: str, 
                   guests: int, guest_name: str, guest_email: str) -> Dict:
        """
        Book a hotel room
        
        Args:
            hotel_id: Hotel ID
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)
            guests: Number of guests
            guest_name: Guest name
            guest_email: Guest email
        
        Returns:
            Dictionary with booking confirmation
        """
        try:
            # Find hotel
            hotel = next((h for h in self.hotels if h["id"] == hotel_id), None)
            if not hotel:
                return {
                    "success": False,
                    "error": "Hotel not found"
                }
            
            # Parse dates
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
            
            if check_out_date <= check_in_date:
                return {
                    "success": False,
                    "error": "Check-out date must be after check-in date"
                }
            
            nights = (check_out_date - check_in_date).days
            total_price = hotel["price_per_night"] * nights
            
            # Check availability
            if hotel["available_rooms"] < guests:
                return {
                    "success": False,
                    "error": "Not enough rooms available"
                }
            
            # Generate booking confirmation
            booking_id = str(uuid.uuid4())[:8].upper()
            
            booking_details = {
                "booking_id": booking_id,
                "hotel_name": hotel["name"],
                "hotel_location": hotel["location"],
                "check_in": check_in,
                "check_out": check_out,
                "nights": nights,
                "guests": guests,
                "guest_name": guest_name,
                "guest_email": guest_email,
                "total_price": total_price,
                "price_per_night": hotel["price_per_night"],
                "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "confirmed"
            }
            
            # Store booking
            self.bookings[booking_id] = booking_details
            
            # Update hotel availability (simulate)
            hotel["available_rooms"] -= 1
            
            return {
                "success": True,
                "message": "Booking confirmed successfully!",
                "booking": booking_details
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Booking failed: {str(e)}"
            }
    
    def get_booking(self, booking_id: str) -> Dict:
        """Get booking details by booking ID"""
        booking = self.bookings.get(booking_id)
        if booking:
            return {
                "success": True,
                "booking": booking
            }
        return {
            "success": False,
            "error": "Booking not found"
        }