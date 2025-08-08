
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol;
using System.Text;
using System.Text.Json;

namespace MCPClient.Services
{
    public class McpClientService
    {
        private readonly HttpClient _httpClient;
        private const string McpUrl = "http://localhost:5000/mcp";

        public McpClientService()
        {
            _httpClient = new HttpClient();
        }

        public async Task<string> CallToolAsync(string toolName, Dictionary<string, object> parameters)
        {
            var clientTransport = new SseClientTransport(
                new SseClientTransportOptions { Endpoint = new Uri(McpUrl) }
            );

            var client = await McpClientFactory.CreateAsync(clientTransport);

            // Execute a tool (this would normally be driven by LLM tool invocations).
            var result = await client.CallToolAsync(
                toolName,
                parameters,
                cancellationToken: CancellationToken.None);

            var textContent = result.Content.FirstOrDefault(c => c.Type == "text");
            string responseText = null;
            if (textContent != null)
            {
                var prop = textContent.GetType().GetProperty("Text");
                if (prop != null)
                {
                    responseText = prop.GetValue(textContent) as string;
                }
            }

            return textContent != null
                ? JsonSerializer.Serialize(responseText, new JsonSerializerOptions { WriteIndented = true })
                : "No content returned";
        }

        public async Task<List<string>> GetAvailableToolsAsync()
        {
            var clientTransport = new SseClientTransport(
                new SseClientTransportOptions { Endpoint = new Uri(McpUrl) }
            );

            var client = await McpClientFactory.CreateAsync(clientTransport);

            var tools = await client.ListToolsAsync();
            return tools.Select(t => $"{t.Name} - {t.Description}").ToList();
        }
    }
}