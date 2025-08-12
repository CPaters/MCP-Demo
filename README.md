# MCP Demo 

This project is a Proof of Concept (PoC) to demonstrate how to work with the Model Context Protocol (MCP) using two different client implementations.  At the moment, they share the same MCP Server implementation

## Server Implementation 
Built using FastMCP in Python, this server exposes two mock APIs - hotels API and weather API.  And is available at the following location: 
- `./mcp-demo-python/mcp_server_fastmcp.py`
- **Hotel API** – `./mcp-demo-python/hotel_api.py` - Search hotels, book a hotel, retrieve booking
- **Weather API** – `./mcp-demo-python/weather_api.py` - Get forecasts and current weather

## Client Implementations

### Python Client
Built with FastMCP and Streamlit:
- connecting to the MCP server
- `./mcp-demo-python/streamlit_client_fastmcp` - Python MCP Client that uses ollama with a local Gemma model 

### C# MVC Client
Built using ASP.NET MVC and C#, integrating with:
- The same MCP server
- A local Ollama model for intent parsing

The MCP server for both clients can be run via:

```bash
python mcp_server_fastmcp.py
```

## 📂 Project Structure

- `/mcp-demo-python` – Python MCP Server + Streamlit MCP client  
  (See its own README.md for details)
- `/mcp-demo-csharp` – ASP.NET MVC MCP client with Ollama integration  
  (See its own README.md for details)  
- `/mcp-demo-python/mcp-server-fastmcp` – FastMCP server implementation wrapping the mock Hotel & Weather APIs. Contained within the mcp-demo-python folder

## How to Get Started

1. Start the MCP server:
   ```bash
   python mcp_server_fastmcp.py
   ```
   Make sure you are in the right environment and have pulled all required packages before running the MCP server

2. Open either the Python or C# client and follow the instructions in their respective README.md.
