#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kimi K2 Instruct Client - ECHTE Moonshot AI API
Direkte Verbindung zur originalen Moonshot AI Plattform
"""

import os
from typing import Iterator, List, Dict, Any, Optional
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

# Environment laden
load_dotenv()

class ChatMessage(BaseModel):
    """Chat-Nachricht Model"""
    role: str  # "user", "assistant", "system"
    content: str

class KimiMoonshotClient:
    """
    Echter Kimi K2 Instruct Client über Moonshot AI
    
    Direkter Zugang zur originalen Moonshot AI API:
    - https://platform.moonshot.ai
    - Echtes Kimi K2 Instruct Modell
    - Native Tool Calling
    - 128K Kontext
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialisiere Moonshot AI Kimi K2 Client
        
        Args:
            api_key: Moonshot AI API Key (optional, wird aus .env geladen)
        """
        self.api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        if not self.api_key or self.api_key in ["sk-demo_key_please_replace", "your_moonshot_api_key_here"]:
            raise ValueError("MOONSHOT_API_KEY ist erforderlich. Bitte in .env-Datei konfigurieren.")
        
        # Moonshot AI Client (OpenAI-kompatibel)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.moonshot.ai/v1"
        )
        
        # Standard-Konfiguration
        self.model = os.getenv("KIMI_MODEL", "moonshot-v1-128k")  # Echte Moonshot Modelle
        self.temperature = float(os.getenv("TEMPERATURE", "0.6"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        
        # Conversation State
        self.conversation_history: List[Dict[str, str]] = []
        
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Einzelne Chat-Nachricht senden
        
        Args:
            message: User-Nachricht
            system_prompt: Optional system prompt
            
        Returns:
            AI-Antwort als String
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Moonshot Chat-Fehler: {str(e)}")
    
    def chat_stream(self, messages: List[Dict[str, str]]) -> Iterator[str]:
        """
        Streaming Chat - Antwort wird Stück für Stück geliefert
        
        Args:
            messages: Liste von Chat-Nachrichten
            
        Yields:
            Einzelne Text-Chunks der AI-Antwort
        """
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"❌ Moonshot Stream-Fehler: {str(e)}"
    
    def conversation_chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Chat mit Verlauf (Conversation Memory)
        
        Args:
            message: User-Nachricht
            system_prompt: Optional system prompt (nur beim ersten Aufruf)
            
        Returns:
            AI-Antwort als String
        """
        # System-Prompt nur beim ersten Mal hinzufügen
        if system_prompt and not self.conversation_history:
            self.conversation_history.append({"role": "system", "content": system_prompt})
        
        # User-Nachricht hinzufügen
        self.conversation_history.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            ai_response = response.choices[0].message.content
            
            # AI-Antwort zum Verlauf hinzufügen
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            raise Exception(f"Moonshot Conversation-Chat-Fehler: {str(e)}")
    
    def conversation_stream(self, message: str, system_prompt: Optional[str] = None) -> Iterator[str]:
        """
        Streaming Chat mit Verlauf
        
        Args:
            message: User-Nachricht
            system_prompt: Optional system prompt (nur beim ersten Aufruf)
            
        Yields:
            Einzelne Text-Chunks der AI-Antwort
        """
        # System-Prompt nur beim ersten Mal hinzufügen
        if system_prompt and not self.conversation_history:
            self.conversation_history.append({"role": "system", "content": system_prompt})
        
        # User-Nachricht hinzufügen
        self.conversation_history.append({"role": "user", "content": message})
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # Vollständige AI-Antwort zum Verlauf hinzufügen
            if full_response:
                self.conversation_history.append({"role": "assistant", "content": full_response})
                    
        except Exception as e:
            yield f"❌ Moonshot Conversation-Stream-Fehler: {str(e)}"
    
    def tool_call(self, message: str, tools: List[Dict[str, Any]], system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Tool Calling - Kimi K2 kann Tools verwenden
        
        Args:
            message: User-Nachricht
            tools: Liste von verfügbaren Tools (OpenAI Format)
            system_prompt: Optional system prompt
            
        Returns:
            Dict mit tool_calls oder finale Antwort
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                tools=tools,
                tool_choice="auto"
            )
            
            choice = response.choices[0]
            
            result = {
                "finish_reason": choice.finish_reason,
                "message": choice.message.content
            }
            
            if choice.finish_reason == "tool_calls":
                result["tool_calls"] = choice.message.tool_calls
                
            return result
            
        except Exception as e:
            return {"error": f"Tool Call Fehler: {str(e)}"}

    def execute_with_code_runner(self, prompt: str) -> str:
        """Use the CodeRunner tool with the preview model to execute code."""
        tools = [{
            "type": "function",
            "function": {
                "name": "code_runner",
                "description": "Execute Python or JavaScript code and return the result",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "language": {
                            "type": "string",
                            "enum": ["python", "javascript"]
                        },
                        "code": {
                            "type": "string",
                            "description": "Source code to execute"
                        }
                    },
                    "required": ["language", "code"]
                },
            }
        }]

        # Erste Anfrage an die API
        result = self.tool_call(prompt, tools, system_prompt=None)

        if "tool_calls" not in result:
            return result.get("message", "")

        from coderunner_tool import run_code

        # Nur den ersten Tool Call verarbeiten
        call = result["tool_calls"][0]
        args = json.loads(call.function.arguments)
        exec_result = run_code(args["language"], args["code"])

        follow_up = [
            {"role": "assistant", "tool_calls": [call]},
            {
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(exec_result),
            },
        ]

        response = self.client.chat.completions.create(
            model="kimi-k2-0711-preview",
            messages=follow_up,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        return response.choices[0].message.content
    
    def clear_conversation(self):
        """Conversation-Verlauf löschen"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Conversation-Verlauf abrufen"""
        return self.conversation_history.copy()
    
    def set_model(self, model: str):
        """Model ändern"""
        self.model = model
    
    def set_temperature(self, temperature: float):
        """Temperature ändern"""
        if 0.0 <= temperature <= 2.0:
            self.temperature = temperature
        else:
            raise ValueError("Temperature muss zwischen 0.0 und 2.0 liegen")
    
    def get_available_models(self) -> List[str]:
        """Verfügbare Moonshot Modelle"""
        return [
            "moonshot-v1-8k",    # 8K Kontext
            "moonshot-v1-32k",   # 32K Kontext  
            "moonshot-v1-128k",  # 128K Kontext (empfohlen)
            "kimi-k2-instruct",  # Neuestes Modell (falls verfügbar)
            "kimi-k2-base"       # Basis-Modell (falls verfügbar)
        ]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Aktuelle Model-Information"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_provider": "Moonshot AI",
            "base_url": "https://api.moonshot.ai/v1",
            "conversation_length": len(self.conversation_history),
            "context_length": "128K",
            "parameters": "1T (32B aktiviert)",
            "architecture": "Mixture-of-Experts (MoE)"
        }

def main():
    """Test-Hauptfunktion"""
    print("🌙 Moonshot AI Kimi K2 Instruct Client - Test")
    print("=" * 60)
    
    try:
        # Client initialisieren
        client = KimiMoonshotClient()
        
        # Model-Info anzeigen
        info = client.get_model_info()
        print("📋 Moonshot Client-Konfiguration:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        print()
        
        # Test-Chat
        print("💬 Test-Chat mit echtem Kimi K2:")
        response = client.chat("Hallo! Bitte stelle dich kurz vor und antworte auf Deutsch.")
        print(f"🌙 Kimi: {response}")
        
        print("\n✅ Moonshot AI Test erfolgreich!")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        print("\n🔧 Lösungsvorschläge:")
        print("1. Überprüfen Sie Ihren MOONSHOT_API_KEY in der .env-Datei")
        print("2. Registrieren Sie sich bei: https://platform.moonshot.ai")
        print("3. Erstellen Sie einen API-Key in Ihrem Moonshot Dashboard")
        print("4. Setzen Sie MOONSHOT_API_KEY=sk-... in der .env-Datei")

if __name__ == "__main__":
    main() 