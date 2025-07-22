#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kimi K2 Instruct Client
Moderne Python-Client für Kimi K2 Instruct über Together AI
"""

import os
from typing import Iterator, List, Dict, Any, Optional
from together import Together
from dotenv import load_dotenv
from pydantic import BaseModel

# Environment laden
load_dotenv()

class ChatMessage(BaseModel):
    """Chat-Nachricht Model"""
    role: str  # "user", "assistant", "system"
    content: str

class KimiClient:
    """
    Kimi K2 Instruct Client
    
    Erweiterte Funktionalitäten:
    - Streaming Support
    - Conversation Management
    - Tool Calling (falls unterstützt)
    - Konfigurierbares Model & Temperature
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialisiere Kimi K2 Client
        
        Args:
            api_key: Together AI API Key (optional, wird aus .env geladen)
        """
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")
        if not self.api_key or self.api_key in ["demo_key_please_replace", "your_api_key_here"]:
            raise ValueError("TOGETHER_API_KEY ist erforderlich. Bitte in .env-Datei konfigurieren.")
        
        # Together AI Client
        self.client = Together(api_key=self.api_key)
        
        # Standard-Konfiguration
        self.model = os.getenv("KIMI_MODEL", "moonshotai/Kimi-K2-Instruct")  # Korrigiert mit moonshotai/ Prefix
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
            raise Exception(f"Chat-Fehler: {str(e)}")
    
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
            yield f"❌ Stream-Fehler: {str(e)}"
    
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
            raise Exception(f"Conversation-Chat-Fehler: {str(e)}")
    
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
            yield f"❌ Conversation-Stream-Fehler: {str(e)}"
    
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
        """Verfügbare Modelle abrufen"""
        return [
            "moonshotai/Kimi-K2-Instruct",
            "meta-llama/Llama-3.1-8B-Instruct-Turbo",
            "meta-llama/Llama-3.1-70B-Instruct-Turbo",
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "microsoft/DialoGPT-medium"
        ]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Aktuelle Model-Information"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_provider": "Together AI",
            "conversation_length": len(self.conversation_history)
        }

# Utility-Funktionen
def test_connection() -> bool:
    """Teste die Verbindung zu Together AI"""
    try:
        client = KimiClient()
        response = client.chat("Hallo, kannst du mich hören?")
        return bool(response and len(response) > 0)
    except Exception as e:
        print(f"Verbindungstest fehlgeschlagen: {e}")
        return False

def main():
    """Test-Hauptfunktion"""
    print("🤖 Kimi K2 Instruct Client - Test")
    print("=" * 50)
    
    try:
        # Client initialisieren
        client = KimiClient()
        
        # Model-Info anzeigen
        info = client.get_model_info()
        print("📋 Client-Konfiguration:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        print()
        
        # Test-Chat
        print("💬 Test-Chat:")
        response = client.chat("Hallo! Stelle dich kurz vor.")
        print(f"🤖 Kimi: {response}")
        
        print("\n✅ Test erfolgreich!")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        print("\n🔧 Lösungsvorschläge:")
        print("1. Überprüfen Sie Ihren TOGETHER_API_KEY in der .env-Datei")
        print("2. Registrieren Sie sich bei: https://api.together.xyz/settings/api-keys")
        print("3. Installieren Sie Dependencies: pip install together python-dotenv")

if __name__ == "__main__":
    main()
