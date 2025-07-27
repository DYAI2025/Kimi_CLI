using Microsoft.VisualStudio.Shell;
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;

namespace KimiK2Coder
{
    /// <summary>
    /// Options page for Kimi K2 Coder configuration
    /// </summary>
    [ClassInterface(ClassInterfaceType.AutoDual)]
    [ComVisible(true)]
    [Guid("12345678-1234-1234-1234-123456789013")]
    public class KimiK2OptionsPage : DialogPage
    {
        [Category("Authentication")]
        [DisplayName("Moonshot API Key")]
        [Description("Your Moonshot AI API key for accessing Kimi K2 Instruct model")]
        [PasswordPropertyText(true)]
        public string ApiKey { get; set; } = "";

        [Category("Model Configuration")]
        [DisplayName("Model Name")]
        [Description("The Kimi K2 model to use (default: moonshotai/Kimi-K2-Instruct)")]
        public string ModelName { get; set; } = "moonshotai/Kimi-K2-Instruct";

        [Category("Model Configuration")]
        [DisplayName("Temperature")]
        [Description("Controls randomness in responses (0.0 = deterministic, 1.0 = very creative)")]
        public double Temperature { get; set; } = 0.3;

        [Category("Model Configuration")]
        [DisplayName("Max Tokens")]
        [Description("Maximum number of tokens in the response")]
        public int MaxTokens { get; set; } = 2048;

        [Category("Behavior")]
        [DisplayName("Auto-Complete Enabled")]
        [Description("Enable automatic code completion suggestions")]
        public bool AutoCompleteEnabled { get; set; } = true;

        [Category("Behavior")]
        [DisplayName("Auto-Complete Delay (ms)")]
        [Description("Delay before showing auto-completion suggestions")]
        public int AutoCompleteDelay { get; set; } = 1000;

        [Category("Behavior")]
        [DisplayName("Show Code Analysis")]
        [Description("Automatically analyze code for issues and suggestions")]
        public bool ShowCodeAnalysis { get; set; } = true;

        [Category("Shortcuts")]
        [DisplayName("Quick Completion Shortcut")]
        [Description("Keyboard shortcut for quick code completion")]
        public string QuickCompletionShortcut { get; set; } = "Ctrl+Shift+K";

        [Category("Shortcuts")]
        [DisplayName("Code Analysis Shortcut")]
        [Description("Keyboard shortcut for code analysis")]
        public string CodeAnalysisShortcut { get; set; } = "Ctrl+Shift+A";

        [Category("Shortcuts")]
        [DisplayName("Generate Tests Shortcut")]
        [Description("Keyboard shortcut for test generation")]
        public string GenerateTestsShortcut { get; set; } = "Ctrl+Shift+T";

        /// <summary>
        /// Validate the configuration
        /// </summary>
        public bool IsValid()
        {
            if (string.IsNullOrWhiteSpace(ApiKey))
                return false;

            if (Temperature < 0.0 || Temperature > 1.0)
                return false;

            if (MaxTokens < 1 || MaxTokens > 128000)
                return false;

            return true;
        }

        /// <summary>
        /// Get validation errors
        /// </summary>
        public string[] GetValidationErrors()
        {
            var errors = new System.Collections.Generic.List<string>();

            if (string.IsNullOrWhiteSpace(ApiKey))
                errors.Add("API Key is required");

            if (Temperature < 0.0 || Temperature > 1.0)
                errors.Add("Temperature must be between 0.0 and 1.0");

            if (MaxTokens < 1 || MaxTokens > 128000)
                errors.Add("Max Tokens must be between 1 and 128000");

            return errors.ToArray();
        }
    }
}