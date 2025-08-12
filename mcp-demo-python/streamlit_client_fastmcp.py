import streamlit as st
import requests
import json
import re
import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

OLLAMA_URL = "http://localhost:11434"
MCP_SERVER_URL = "http://localhost:5000/mcp"   # FastMCP default mcp path


# Configure Streamlit page
st.set_page_config(
    page_title="Hotel & Weather Assistant",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)
if 'messages' not in st.session_state:
    st.session_state.messages = []


# Sidebar configuration
st.sidebar.title("🤖 Assistant Configuration")

# ✅ MCP server test function
async def test_mcp_connection():
    httptransport = StreamableHttpTransport(url=MCP_SERVER_URL)
    async with Client(httptransport) as mcp_client: 
        tools = await mcp_client.list_tools()
        if tools:
            return True, tools  
        else:
            return False, []

# ✅ Display server status in sidebar
server_connected, available_tools = asyncio.run(test_mcp_connection())

if server_connected:
    st.sidebar.success("✅ Server Connected")
else:
    st.sidebar.error("❌ Server Disconnected")
    st.sidebar.info("Make sure to run the MCP server")


st.title("🤖 MCP Demo: Hotels & Weather")
st.markdown("""
Welcome to the **Model Context Protocol (MCP)** demo!  
You can ask about:
- 📍 Hotel search and bookings  
- 🌤️ Current weather, forecasts, and alerts

This demo uses a mock API server and a local `gemma3` model via [Ollama](https://ollama.com/).
""")

# Chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        
# Show available tools
if st.button("🔍 Show Available Tools"):
    st.subheader("Available Tools")
    for tool in available_tools: #tools:
        st.markdown(f"- **{tool.name}**: {tool.description}")
        st.session_state.messages.append({"role": "system", "content": tool.name + ": " + tool.description})


st.subheader("Ask Something")

# Use gemma3 to parse intent
def parse_with_gemma3(prompt: str) -> dict:
    system_instruction = """You are an AI assistant that helps parse user requests for hotel bookings and weather information. 

Given a user message, determine the intent and extract relevant parameters. Respond ONLY with a JSON object.

Possible intents:
- "search_hotels": User wants to find hotels
- "book_hotel": User wants to book a specific hotel 
- "get_hotel": User wants details about a specific hotel 
- "get_booking": User wants to check booking details
- "get_current_weather": User wants current weather
- "get_weather_forecast": User wants weather forecast
- "get_weather_alerts": User wants weather alerts
- "general": General conversation or unclear intent

For hotel searches, extract: location, check_in (YYYY-MM-DD), check_out (YYYY-MM-DD), guests (number)
For hotel booking, extract: hotel_id, check_in, check_out, guests, guest_name, guest_email. if user provides a hotel name, find the hotel ID using the hotel name
For booking lookup, extract: booking_id
For weather requests, extract: location, days (for forecast, 1-7)

If dates are relative (like "tomorrow", "next week"), convert to YYYY-MM-DD format.
If information is missing, set the field to null.

Example responses:
{"tool": "search_hotels", "location": "New York", "check_in": "2024-02-15", "check_out": "2024-02-17", "guests": 2}
{"tool": "get_current_weather", "location": "Miami"}
{"tool": "general", "message": "I need more information to help you"}
"""

    full_prompt = system_instruction + "\n\nUser: " + prompt + "\n\nJSON:"
    response = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": "gemma3",
        "prompt": full_prompt,
        "stream": False
    }, timeout=60)

    call_result = response.json()  

    match = re.search(r'\{.*\}', call_result.get("response", ""), re.DOTALL)
    #return json.loads(match.group()) if match else {"tool": None, "params": {}}
    if match:
        parsed = json.loads(match.group())

        # Normalize structure: if tool and flat params, wrap them
        mcp_tool = parsed.get("tool")
        if mcp_tool and not isinstance(parsed.get("params"), dict):
            params = {k: v for k, v in parsed.items() if k != "tool"}
            return {"tool": mcp_tool, "params": params}
        return parsed
    
    return {"tool": None, "params": {}}


def unwrap_tool_result(resp):
    # FastMCP returns CallToolResult with content list of TextContent
    if resp.content:
        return "\n\n".join(tc.text for tc in resp.content)
    return str(resp)


# Process user input
if user_input:= st.chat_input("Ask me about hotels or weather!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    #st.markdown(f"**You asked:** {user_input}")
    with st.spinner("Parsing your question..."):
        intent = parse_with_gemma3(user_input)

        tool = intent.get("tool")
        params = intent.get("params", {})

    if not tool:
        st.warning("Sorry, I couldn't understand what you need.")
    else:
        st.markdown(f"🔧 **Tool:** `{tool}`")
        st.markdown(f"🧾 **Parameters:** `{json.dumps(params, indent=2)}`")

        if None in params.values():
            st.info("Please provide complete details for your request.")
        else:
            with st.spinner("Calling tool..."):
                transport = StreamableHttpTransport(url=MCP_SERVER_URL)
                async def call():
                    async with Client(transport) as client:

                        call_result = await client.call_tool(tool, params)
                        return unwrap_tool_result(call_result)
                result = asyncio.run(call())

            st.success("✅ Response:")
            st.markdown(result)
            st.session_state.messages.append({"role": "assistant", "content": result})



# Example queries sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("💡 Example Queries")
st.sidebar.markdown("""
**Hotel Booking:**
- "Find hotels in Miami for 2 guests from tomorrow to next week"
- "Book hotel_002 for John Doe for this weekend for 2 people, email john@email.com"

**Weather:**
- "What's the weather in Denver?"
- "Show me the 5-day forecast for Chicago"
- "Any weather alerts for New York?"

**Bookings:**
- "Look up my booking with ID ABC12345"
""")

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()