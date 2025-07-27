#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kimi K2 Agent Implementation
Advanced AI agent with code execution and analysis capabilities
"""

import os
import threading
from typing import Optional, List, Dict, Any
from openai import OpenAI
from tools.execution_toolkit import execute_shell_command, read_file, write_file


class KimiK2Agent:
    """
    Advanced Kimi K2 Agent with autonomous execution capabilities
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "moonshotai/Kimi-K2-Instruct", temperature: float = 0.6):
        """
        Initialize the Kimi K2 Agent
        
        Args:
            api_key: Moonshot AI API key
            model: Model name to use
            temperature: Response temperature (0.0-1.0)
        """
        self.api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        if not self.api_key or self.api_key == "sk-demo_key_please_replace":
            raise ValueError("Valid MOONSHOT_API_KEY is required")
        
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.moonshot.ai/v1")
        self.model = model
        self.temperature = temperature
        self.conversation_history = []
        self.stop_requested = False
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Chat with Kimi K2 and get a response
        
        Args:
            message: User message
            system_prompt: Optional system prompt override
            
        Returns:
            AI response
        """
        try:
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": message})
            
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            elif not any(msg["role"] == "system" for msg in self.conversation_history):
                messages.append({
                    "role": "system", 
                    "content": "You are Kimi K2, an advanced AI coding assistant. Help with programming, analysis, and development tasks."
                })
            
            messages.extend(self.conversation_history)
            
            # Get response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=4096
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add to history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            return f"Error communicating with Kimi K2: {e}"
    
    def analyze_code(self, code: str, filename: str = "") -> str:
        """
        Analyze code for bugs, improvements, and best practices
        
        Args:
            code: Code to analyze
            filename: Optional filename for context
            
        Returns:
            Analysis results
        """
        prompt = f"""
Analyze the following code for:
1. Potential bugs and issues
2. Performance improvements
3. Code quality and best practices
4. Security considerations
5. Suggestions for optimization

File: {filename}
Code:
```
{code}
```

Provide a detailed analysis with specific recommendations.
"""
        return self.chat(prompt, "You are an expert code reviewer and security analyst.")
    
    def generate_tests(self, code: str, language: str = "python") -> str:
        """
        Generate comprehensive unit tests for the given code
        
        Args:
            code: Code to generate tests for
            language: Programming language
            
        Returns:
            Generated test code
        """
        prompt = f"""
Generate comprehensive unit tests for the following {language} code:

```{language}
{code}
```

Include:
1. Happy path tests
2. Edge cases
3. Error conditions
4. Mock objects where appropriate
5. Clear test names and assertions

Use appropriate testing framework for {language}.
"""
        return self.chat(prompt, f"You are an expert test engineer specializing in {language} testing.")
    
    def execute_command(self, command: str) -> str:
        """
        Execute a shell command safely
        
        Args:
            command: Command to execute
            
        Returns:
            Command output
        """
        result = execute_shell_command(command)
        output = []
        
        if result["stdout"]:
            output.append(f"STDOUT:\n{result['stdout']}")
        if result["stderr"]:
            output.append(f"STDERR:\n{result['stderr']}")
        output.append(f"EXIT CODE: {result['exit_code']}")
        
        return "\n".join(output)
    
    def execute_plan(self, plan_file: str):
        """
        Execute a plan from a file containing commands
        
        Args:
            plan_file: Path to plan file
        """
        try:
            plan_content = read_file(plan_file)
            print(f"📋 Executing plan from {plan_file}")
            
            for line_num, line in enumerate(plan_content.splitlines(), 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                if self.stop_requested:
                    print("⏹️ Plan execution stopped by user")
                    break
                
                print(f"\n📍 Step {line_num}: {line}")
                
                # Execute the command
                result = self.execute_command(line)
                print(result)
                
        except Exception as e:
            print(f"❌ Error executing plan: {e}")
    
    def stop(self):
        """Stop the agent execution"""
        self.stop_requested = True
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def save_conversation(self, filename: str):
        """Save conversation history to file"""
        try:
            import json
            with open(filename, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
            print(f"💾 Conversation saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving conversation: {e}")
    
    def load_conversation(self, filename: str):
        """Load conversation history from file"""
        try:
            import json
            with open(filename, 'r') as f:
                self.conversation_history = json.load(f)
            print(f"📂 Conversation loaded from {filename}")
        except Exception as e:
            print(f"❌ Error loading conversation: {e}")