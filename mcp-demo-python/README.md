# MCP Hotel & Weather Demo

A comprehensive demonstration of the Model Context Protocol (MCP) featuring a hotel booking engine and weather service with a Streamlit chatbot interface powered by a local Gemma model with Ollama

## 🎯 Solution Overview

This demo showcases a complete MCP implementation that bridges AI language models with external APIs through a standardized protocol. The solution demonstrates how MCP enables AI assistants to interact with real-world services through structured tool calls, creating a more powerful and extensible AI experience.

### Key Concepts Demonstrated

- **MCP Protocol Implementation**: Shows how to expose APIs as MCP tools
- **AI Tool Integration**: Demonstrates AI models calling these tools
- **Natural Language to API**: Converts conversational requests into structured API calls
- **Multi-Service Architecture**: Integrates multiple APIs (hotel booking + weather) in one system
- **Local AI Deployment**: Uses locally-hosted Gemma models via Ollama

## 🏗️ Architecture

The demo consists of four main layers:

### 1. **Data Layer** - Mock APIs

- **`hotel_api.py`** - Simulates hotel booking system with inventory management
- **`weather_api.py`** - Generates realistic weather data with seasonal variations

### 2. **Protocol Layer** - MCP Server

- **`mcp_server_fastmcp.py`** - Uses Fastmcp package to expose functions as MCP tools

### 3. **AI Layer** - Language Model Integration

- **Ollama Integration** - Local deployment of Llama/Gemma models
- **Intent Recognition** - Natural language understanding for user requests
- **Parameter Extraction** - Structured data extraction from conversational input

### 4. **Presentation Layer** - User Interface

- **`streamlit_client_fastmcp.py`** - Streamlit web interface with chat functionality using fastmcp
- **Real-time Communication** - Live interaction between UI, AI, and backend services

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │    │   Llama/Gemma   │    │  MCP/HTTP API   │
│  (Natural Lang) │────│   (Intent AI)   │────│     Server      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                               ┌─────────────────┐
                                               │   Backend APIs  │
                                               │ Hotel + Weather │
                                               └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Ollama** - For running Llama/Gemma models locally
   ```bash
   # Install Ollama (visit https://ollama.ai for your platform)
   # Then pull a model
   ollama pull gemma:7b
   ```

### Installation

1. **Clone/Download the demo files**

   ```bash
   git clone <your-repo> mcp-demo-python
   cd mcp-demo-python
   ```
2. **Create your environement file**
 Before starting the MCP server, create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**

   ```bash
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Verify Ollama is working**
   ```bash
   ollama list
   ```

### Running the Demo

**⚠️ Important: You need to start the backend API server BEFORE running the Streamlit chat application.**

#### Step 1: Start the Backend API Server

Open a **first terminal** and run:

```bash
python mcp_server_fastmcp.py
```

You should see:

```
🚀 Starting Hotel & Weather API Server...
📡 Server will be available at http://localhost:5000/mcp
🛠️ Available endpoints:
   GET /tools - List available tools
   POST /call/<tool_name> - Call a specific tool
   GET /health - Health check
 * Running on all addresses (0.0.0.0)

```

**Keep this terminal running** - the APIs need to stay active for the chat application to work.

#### Step 2: Start the Streamlit Chat Application

Open a **second terminal** and run:

```bash
streamlit run streamlit_client_fastmcp.py
```

#### Step 3: Use the Application

1. **Open your browser** to `http://localhost:8501`

2. **Verify API connection** Check for message 'Server Connected'

3. **Start chatting!** Try example queries like:
   - "Find hotels in New York for 2 guests from 2024-03-01 to 2024-03-03"
   - "What's the weather in Miami?"
   - "Book hotel_001 for John Doe at john@email.com"

#### Troubleshooting

**If you get connection errors:**

- Make sure the API server (Step 1) is running first
- Check that `http://localhost:5000/health` returns a response
- Ensure no other applications are using port 5000

**For testing the APIs independently:**

```bash
# Test hotel API
python -c "from hotel_api import HotelAPI; api = HotelAPI(); print(api.search_hotels('Miami', '2024-03-01', '2024-03-03', 2))"

# Test weather API
python -c "from weather_api import WeatherAPI; api = WeatherAPI(); print(api.get_current_weather('Miami'))"
```

## 🛠️ Detailed Component Analysis

### 1. Hotel Booking API (`hotel_api.py`)

**Purpose**: Simulates a complete hotel reservation system with realistic business logic.

**Core Features**:

- **Hotel Search Engine**:
  - Location-based filtering with fuzzy matching
  - Date validation and availability checking
  - Dynamic pricing calculation based on stay duration
  - Guest capacity validation
- **Reservation System**:
  - UUID-based booking confirmation IDs
  - Guest information management
  - Inventory tracking (reduces available rooms on booking)
  - Booking status management
- **Data Retrieval**: Lookup existing reservations by confirmation ID

**Technical Implementation**:

```python
# Example hotel data structure
{
    "id": "hotel_001",
    "name": "Grand Plaza Hotel",
    "location": "New York",
    "price_per_night": 299.99,
    "rating": 4.5,
    "amenities": ["WiFi", "Pool", "Gym", "Room Service"],
    "available_rooms": 15
}
```

**Sample Hotel Inventory** (5 properties):

- **Grand Plaza Hotel** (New York) - Premium business hotel, $299.99/night
- **Sunset Beach Resort** (Miami) - Beach resort with spa, $199.99/night
- **Mountain View Lodge** (Denver) - Outdoor adventure lodge, $149.99/night
- **City Center Inn** (Chicago) - Budget-friendly downtown, $179.99/night
- **Luxury Suites** (Los Angeles) - High-end luxury, $399.99/night

### 2. Weather API (`weather_api.py`)

**Purpose**: Provides weather data with realistic geographical and seasonal variation.

**Core Features**:

- **Current Conditions**: Temperature, humidity, wind speed, visibility, UV index
- **Multi-Day Forecasts**: Up to 7-day predictions with detailed daily breakdowns
- **Alert System**: Simulated weather warnings and advisories
- **Geographic Intelligence**: City-specific base temperatures and climate patterns

**Technical Implementation**:

- **Seasonal Adjustments**: Automatic temperature modification based on current month
- **Location-Aware**: Pre-configured climate data for major US cities
- **Realistic Variability**: Random variations within climatologically appropriate ranges
- **Weather Correlation**: Precipitation amounts correlate with weather conditions

**Supported Locations**: New York, Miami, Denver, Chicago, Los Angeles, Seattle, Phoenix, Boston, San Francisco, Atlanta

### 3. MCP Protocol Server (`mcp_server_fastmcp.py`)

**Purpose**: Exposes backend APIs through standardized MCP protocol for AI model consumption.

**Two Implementation Approaches**:

#### Full MCP Server (`mcp_server_fastmcp.py`)

- **Protocol Compliance**: Full MCP specification implementation
- **Tool Definition**: JSON Schema-based parameter validation

**Available MCP Tools**:

1. **`search_hotels`** - Multi-parameter hotel discovery
2. **`book_hotel`** - Complete reservation workflow
3. **`get_booking`** - Reservation lookup and management
4. **`get_current_weather`** - Real-time weather conditions
5. **`get_weather_forecast`** - Extended weather predictions
6. **`get_weather_alerts`** - Emergency weather notifications

### 4. AI Integration Layer

**Natural Language Understanding**:

- **Intent Classification**: Determines user's goal (search, book, weather, etc.)
- **Parameter Extraction**: Pulls structured data from conversational text
- **Date Processing**: Converts relative dates ("tomorrow", "next week") to ISO format
- **Validation Logic**: Ensures required parameters are present before API calls

**LLM Integration via Ollama**:

- **Local Deployment**: No external API dependencies
- **Model Flexibility**: Supports various Llama and Gemma variants
- **Prompt Engineering**: Structured prompts for consistent JSON responses
- **Error Handling**: Graceful degradation when models are unavailable

### 5. Streamlit Client (`streamlit_client_fastmcp.py`)

**User Experience Features**:

- **Real-time Chat**: WebSocket-like communication for instant responses
- **Example Queries**: Built-in suggestions for user guidance
- **Chat History**: Persistent conversation memory within session

**Technical Architecture**:

- **Async Processing**: Non-blocking API calls with loading indicators
- **State Management**: Streamlit session state for conversation persistence

## 🔄 MCP Protocol Implementation Details

### Protocol Flow Architecture

```
User Message → Intent Parser → Parameter Extraction → MCP Tool Call → API Response → Formatted Output
     ↓              ↓                    ↓                  ↓              ↓              ↓
"Find hotels   hotel_search      {location: "Miami",   search_hotels   Hotel API     Rich formatted
 in Miami"     intent detected   check_in: "2024-...",   tool called   returns data   response with
                                 guests: 2}                                            emojis & structure
```

### Tool Schema Definition

Each MCP tool includes comprehensive JSON Schema validation:

```json
{
  "name": "search_hotels",
  "description": "Search for available hotels in a location for specific dates",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": { "type": "string", "description": "City or location" },
      "check_in": {
        "type": "string",
        "description": "Check-in date (YYYY-MM-DD)"
      },
      "check_out": {
        "type": "string",
        "description": "Check-out date (YYYY-MM-DD)"
      },
      "guests": {
        "type": "integer",
        "minimum": 1,
        "description": "Number of guests"
      }
    },
    "required": ["location", "check_in", "check_out", "guests"]
  }
}
```

### Response Formatting Strategy

The system employs rich text formatting for enhanced user experience:

- **Emojis for Visual Appeal**: 🏨 for hotels, 🌤️ for weather, 📋 for bookings
- **Structured Information**: Clear hierarchical presentation of data
- **Contextual Information**: Relevant details based on the specific request type

## 🧠 AI Integration & Natural Language Processing

### Intent Recognition System

The AI layer uses sophisticated prompt engineering to classify user intents:

```python
# System prompt structure for intent classification
system_prompt = """
You are an AI assistant that helps parse user requests for hotel bookings and weather information.
Given a user message, determine the intent and extract relevant parameters.
Respond ONLY with a JSON object.

Possible intents:
- "search_hotels": User wants to find hotels
- "book_hotel": User wants to book a specific hotel
- "get_weather": User wants current weather
[... additional intents]
"""
```

### Parameter Extraction Logic

**Date Processing Intelligence**:

- Relative dates: "tomorrow" → calculates next day
- Date ranges: "next week" → derives check-in/check-out dates
- Natural language: "March 1st to 3rd" → converts to ISO format

**Entity Recognition**:

- Location extraction from various formats
- Guest count inference from context
- Email and name validation for bookings

## 💬 Example Conversation Flows

### Hotel Booking Journey

```
User: "I need a hotel in Miami for 2 people from March 1st to March 3rd"

AI Processing:
├── Intent: search_hotels
├── Parameters: {location: "Miami", check_in: "2024-03-01",
│                check_out: "2024-03-03", guests: 2}
├── MCP Tool Call: search_hotels(parameters)
├── API Response: 2 available hotels
└── Formatted Output: Rich hotel listing with prices and amenities

Assistant Response:
🏨 Found 2 hotels in Miami:

**Sunset Beach Resort**
📍 Miami
💰 $199.99/night (Total: $399.98 for 2 nights)
⭐ Rating: 4.2/5
🎯 Hotel ID: hotel_002
✨ Amenities: Beach Access, WiFi, Pool, Spa

**[Additional hotel details...]**

```

### Weather Information Request

```
User: "What's the weather like in Denver?"

AI Processing:
├── Intent: get_weather
├── Parameters: {location: "Denver"}
├── MCP Tool Call: get_current_weather(parameters)
├── API Response: Current conditions
└── Formatted Output: Comprehensive weather display

Assistant Response:
🌤️ **Current Weather in Denver**
🌡️ **Temperature:** 12°C (54°F)
☁️ **Condition:** Partly Cloudy
💧 **Humidity:** 45%
💨 **Wind Speed:** 15 km/h
👁️ **Visibility:** 18 km
☀️ **UV Index:** 6
```

**Ollama Model Management**:

```bash
# Install recommended models for different use cases
ollama pull llama2:7b      # General purpose, good balance
ollama pull gemma:2b       # Lightweight, faster responses
ollama pull llama2:13b     # Higher accuracy, slower
ollama pull codellama:7b   # Better for technical queries
```




## 🐛 Troubleshooting

### Common Issues

**"No models found"**

- Install Ollama: https://ollama.ai
- Pull a model: `ollama pull llama2`

**"Failed to connect to MCP server"**

- Ensure Python dependencies are installed
- Check that `mcp_server.py` runs without errors

**"Module not found" errors**

- Install requirements: `pip install -r requirements.txt`
- Verify Python 3.8+ is being used

**Chat responses are slow**

- Try a smaller model: `ollama pull gemma:2b`
- Ensure sufficient RAM for the model

### Debug Mode

Run components separately for debugging:

```bash
# Test hotel API
python -c "from hotel_api import HotelAPI; api = HotelAPI(); print(api.search_hotels('Miami', '2024-03-01', '2024-03-03', 2))"

# Test weather API
python -c "from weather_api import WeatherAPI; api = WeatherAPI(); print(api.get_current_weather('Miami'))"

# Test MCP server
python mcp_server.py
```

## 📁 Complete File Structure

```
mcp-demo/
├── 📄 README.md                        # This comprehensive documentation
├── 📄 requirements.txt                 # Python dependencies
├── 🏨 hotel_api.py                     # Hotel booking API with 5 sample hotels
├── 🌤️ weather_api.py                   # Weather service with forecasts & alerts
├── 🖥️ mcp_server_fastmcp.py            # Full MCP protocol server (Python 3.10+)
└── 🧪 streamlit_client_fastmcp.py      # Full MCP client (requires Python 3.10+)
```

