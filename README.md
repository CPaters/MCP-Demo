# MCP Demo 

This project is a Proof of Concept (PoC) to demonstrate how to work with the Model Context Protocol (MCP) using two different client implementations.  At the moment, they share the same MCP Server implementation

## Server Implementation 
Built using FastMCP in Python, this server exposes two mock APIs - hotels API and weather API.  And is available at the following location: 
- **MCP Server**- `./mcp-demo-python/mcp_server_fastmcp.py`


There are two APIs which are exposed using FastAPI.  
- **FastAPI Apis for hotels and weather** – `./mcp-demo-python/hotel_and_weather_api.py` - Search hotels, book a hotel, retrieve booking

## Client Implementations

### Python Client
Built with FastMCP and Streamlit:
- connecting to the MCP server
- Uses a local Ollama model (Gemma3) for intent parsing
- `./mcp-demo-python/streamlit_client_fastmcp` - Python MCP Client that uses ollama with a local Gemma model 

### C# MVC Client
Built using ASP.NET MVC and C#, integrating with:
- The same MCP server
- A local Ollama model (Gemma3) for intent parsing



## 📂 Project Structure

- `/mcp-demo-python` – Includes the Python MCP Server + APIs + Streamlit MCP client  
  (See its own README.md for details)
- `/mcp-demo-csharp` – ASP.NET MVC MCP client with Ollama integration  
  (See its own README.md for details)  


### Running the code 
Expose the APIs by running: 
```bash
uvicorn hotel_and_weather_api:app --port 8000
```

The MCP server for both clients can be run via:

```bash
python mcp_server_fastmcp.py
```

The Python MCP client can be run via: 
```bash
streamlit run streamlit_client_fastmcp.py
```

Run the C# MVC Client through Visual Studio
