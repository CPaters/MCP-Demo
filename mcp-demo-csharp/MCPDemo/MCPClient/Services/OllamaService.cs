using MCPClient.Models;
using System.ComponentModel;
using System.Net.Http;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace MCPClient.Services
{
    public class OllamaService
    {
        private readonly HttpClient _httpClient;
        private const string OllamaUrl = "http://localhost:11434/api/generate";

        public OllamaService()
        {
            _httpClient = new HttpClient();
        }

        public async Task<IntentResult?> ParseIntentAsync(string userInput)
        {
            string prompt = $"""
You are an AI assistant that helps parse user requests for hotel bookings and weather information. 

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
"tool": "search_hotels", "location": "New York", "check_in": "2024-02-15", "check_out": "2024-02-17", "guests": 2
"tool": "get_current_weather", "location": "Miami"
"tool": "general", "message": "I need more information to help you"

User: {userInput}
JSON:
""";

            var response = await _httpClient.PostAsJsonAsync(OllamaUrl, new
            {
                model = "gemma3",
                prompt = prompt,
                stream = false
            });

            var content = await response.Content.ReadAsStringAsync();
            var match = Regex.Match(content, @"\{.*\}", RegexOptions.Singleline);


            if (match.Success)
            {
                var dict = JsonSerializer.Deserialize<Dictionary<string, object>>(match.Value);
                if (dict != null && dict.ContainsKey("response"))
                {

                    // The response is a string that contains JSON, possibly wrapped in markdown
                    var responseString = dict["response"]?.ToString();

                    // Remove markdown formatting if present
                    var innerMatch = Regex.Match(responseString ?? "", @"\{.*\}", RegexOptions.Singleline);
                    if (innerMatch.Success)
                    {
                        var innerDict = JsonSerializer.Deserialize<Dictionary<string, object>>(innerMatch.Value);
                        if (innerDict != null && innerDict.ContainsKey("tool"))
                        {
                            string tool = innerDict["tool"].ToString();
                            innerDict.Remove("tool");

                            return new IntentResult { Tool = tool, Params = innerDict };
                        }
                    }
                }
            }
            return null;
        }
    }
}
