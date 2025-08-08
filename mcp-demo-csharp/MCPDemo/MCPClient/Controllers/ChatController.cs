using MCPClient.Models;
using MCPClient.Services;
using Microsoft.AspNetCore.Mvc;

namespace MCPClient.Controllers
{  
        public class ChatController : Controller
        {
            private readonly OllamaService _ollamaService;
            private readonly McpClientService _mcpClientService;

            public ChatController(OllamaService ollamaService, McpClientService mcpClientService)
            {
                _ollamaService = ollamaService;
                _mcpClientService = mcpClientService;
            }

            [HttpGet]
            public IActionResult Index()
            {
                if (HttpContext.Session.GetObject<List<ChatMessage>>("ChatHistory") == null)
                    HttpContext.Session.SetObject("ChatHistory", new List<ChatMessage>());

                return View(HttpContext.Session.GetObject<List<ChatMessage>>("ChatHistory"));
            }

            [HttpPost]
            public async Task<IActionResult> Index(string userInput)
            {
                var history = HttpContext.Session.GetObject<List<ChatMessage>>("ChatHistory") ?? new List<ChatMessage>();
                history.Add(new ChatMessage { Role = "user", Content = userInput });

                var intent = await _ollamaService.ParseIntentAsync(userInput);
                if (intent == null || string.IsNullOrWhiteSpace(intent.Tool))
                {
                    history.Add(new ChatMessage { Role = "assistant", Content = "❌ Sorry, I couldn't understand your request." });
                }
                else
                {
                    var result = await _mcpClientService.CallToolAsync(intent.Tool, intent.Params);
                    string decodedResult = result;
                    if (!string.IsNullOrEmpty(result) && result.StartsWith("\"") && result.EndsWith("\""))
                    {
                    decodedResult = System.Text.Json.JsonSerializer.Deserialize<string>(result);
                    }
                    else
                    {
                        decodedResult = result; // Use the raw result if it doesn't look like a JSON string 
                }
                    history.Add(new ChatMessage { Role = "assistant", Content = decodedResult });
                }

                HttpContext.Session.SetObject("ChatHistory", history);
                return View(history);
            }

        [HttpGet]
        public async Task<IActionResult> GetTools()
        {
            var tools = await _mcpClientService.GetAvailableToolsAsync();
            return Json(tools);
        }
    }
    }


