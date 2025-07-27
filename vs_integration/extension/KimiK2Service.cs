using System;
using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace KimiK2Coder
{
    /// <summary>
    /// Core service for interacting with Kimi K2 Instruct API
    /// </summary>
    public class KimiK2Service
    {
        private readonly HttpClient _httpClient;
        private readonly string _apiKey;
        private readonly string _baseUrl = "https://api.moonshot.ai/v1";
        private readonly string _model = "moonshotai/Kimi-K2-Instruct";

        public KimiK2Service(string apiKey)
        {
            _apiKey = apiKey ?? throw new ArgumentNullException(nameof(apiKey));
            _httpClient = new HttpClient();
            _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {_apiKey}");
        }

        /// <summary>
        /// Generate code completion using Kimi K2
        /// </summary>
        public async Task<string> GetCodeCompletionAsync(string prompt, string context = "")
        {
            try
            {
                var systemPrompt = "You are Kimi K2, a world-class programming assistant. " +
                                 "Generate clean, efficient, and well-documented code. " +
                                 "Focus on best practices and modern coding standards.";

                var messages = new[]
                {
                    new { role = "system", content = systemPrompt },
                    new { role = "user", content = $"Context: {context}\n\nRequest: {prompt}" }
                };

                var requestBody = new
                {
                    model = _model,
                    messages = messages,
                    temperature = 0.3,
                    max_tokens = 2048,
                    stream = false
                };

                var json = JsonSerializer.Serialize(requestBody);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync($"{_baseUrl}/chat/completions", content);
                response.EnsureSuccessStatusCode();

                var responseJson = await response.Content.ReadAsStringAsync();
                var result = JsonSerializer.Deserialize<ChatCompletionResponse>(responseJson);

                return result?.choices?[0]?.message?.content ?? "No response generated";
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error in GetCodeCompletionAsync: {ex.Message}");
                return $"Error: {ex.Message}";
            }
        }

        /// <summary>
        /// Analyze code for bugs and improvements
        /// </summary>
        public async Task<string> AnalyzeCodeAsync(string code, string language = "")
        {
            try
            {
                var systemPrompt = "You are Kimi K2, an expert code analyzer. " +
                                 "Analyze the provided code for bugs, performance issues, security vulnerabilities, " +
                                 "and suggest improvements with clear explanations.";

                var userPrompt = $"Language: {language}\n\nCode to analyze:\n```{language}\n{code}\n```\n\n" +
                               "Please provide:\n1. Bug analysis\n2. Performance suggestions\n3. Code quality improvements\n4. Security considerations";

                return await GetCodeCompletionAsync(userPrompt);
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error in AnalyzeCodeAsync: {ex.Message}");
                return $"Error analyzing code: {ex.Message}";
            }
        }

        /// <summary>
        /// Generate unit tests for given code
        /// </summary>
        public async Task<string> GenerateTestsAsync(string code, string language = "", string framework = "")
        {
            try
            {
                var systemPrompt = "You are Kimi K2, an expert test engineer. " +
                                 "Generate comprehensive unit tests with good coverage, edge cases, and clear assertions.";

                var userPrompt = $"Language: {language}\nFramework: {framework}\n\n" +
                               $"Generate unit tests for this code:\n```{language}\n{code}\n```\n\n" +
                               "Include:\n1. Happy path tests\n2. Edge cases\n3. Error conditions\n4. Mocking if needed";

                return await GetCodeCompletionAsync(userPrompt);
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error in GenerateTestsAsync: {ex.Message}");
                return $"Error generating tests: {ex.Message}";
            }
        }

        /// <summary>
        /// Explain code functionality
        /// </summary>
        public async Task<string> ExplainCodeAsync(string code, string language = "")
        {
            try
            {
                var systemPrompt = "You are Kimi K2, a technical documentation expert. " +
                                 "Explain code in clear, educational terms suitable for developers at all levels.";

                var userPrompt = $"Language: {language}\n\n" +
                               $"Explain this code:\n```{language}\n{code}\n```\n\n" +
                               "Provide:\n1. High-level overview\n2. Step-by-step breakdown\n3. Key concepts used\n4. Potential use cases";

                return await GetCodeCompletionAsync(userPrompt);
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error in ExplainCodeAsync: {ex.Message}");
                return $"Error explaining code: {ex.Message}";
            }
        }

        public void Dispose()
        {
            _httpClient?.Dispose();
        }
    }

    /// <summary>
    /// Response model for chat completions
    /// </summary>
    public class ChatCompletionResponse
    {
        public Choice[] choices { get; set; }
    }

    public class Choice
    {
        public Message message { get; set; }
    }

    public class Message
    {
        public string content { get; set; }
    }
}