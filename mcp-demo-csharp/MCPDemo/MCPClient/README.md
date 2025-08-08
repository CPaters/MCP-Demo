# MCP Demo: Hotels & Weather

This project is a demonstration of the **Model Context Protocol (MCP)**, showcasing how a conversational AI can interact with multiple APIs to provide useful services. The demo uses a local [gemma3](https://ollama.com/library/gemma3) language model (downloaded and run via [Ollama](https://ollama.com/)) and integrates with an MCP server that wraps two mock APIs - weather api and a hotel api.  The MCP server is written in python and so are the APIs.  You can find them in the folder mcp-demo-python.  

## Features

- **Conversational UI** for interacting with the AI assistant.
- **Hotel API**:  
  - Search for hotels  
  - Make hotel bookings  
  - Retrieve existing bookings
- **Weather API**:  
  - Get weather forecasts for a location  
  - Check current weather  
  - View weather alerts

## Prerequisites

Before running this project, ensure the following are set up and running **locally**:

1. **Ollama with gemma3 model**
   - [Install Ollama](https://ollama.com/download)
   - Download and run the `gemma3` model:
     ```
     ollama run gemma3
     ```
   - By default, Ollama runs on `http://localhost:11434`.

2. **MCP Server for the Hotel and Weather API**
   - Start the mcp server by opening a terminal and running the command below:

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

   - The project assumes it will be available at a hardcoded `localhost` URL.

> **Note:** The URLs for the APIs and Ollama are currently hardcoded in the project and must be running on your local machine.

## Running the Project

1. Ensure all prerequisites above are running.
2. Open the solution in Visual Studio 2022 or your favourite IDE.
3. Build and run the project.
4. Navigate to the chat page to interact with the demo.

## Example Queries

- **Hotel Booking:**  
  - "Find hotels in Miami for 2 guests from tomorrow to next week"
  - "Book hotel_002 for John Doe, email john@email.com"
- **Weather:**  
  - "What's the weather in Denver?"
  - "Show me the 5-day forecast for Chicago"
  - "Any weather alerts for New York?"
- **Bookings:**  
  - "Look up my booking with ID ABC12345"

---

**Note:**  
This project is for demonstration purposes. The APIs and model endpoints are assumed to be running locally and are not secured for production use.
