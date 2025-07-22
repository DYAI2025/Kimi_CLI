#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste verschiedene Kimi API Endpoints
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def test_api_endpoint(base_url, description):
    """Teste einen spezifischen API-Endpoint"""
    print(f"\n🔍 Teste {description}: {base_url}")
    
    try:
        client = OpenAI(
            api_key=os.getenv("MOONSHOT_API_KEY"),
            base_url=base_url
        )
        
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[{"role": "user", "content": "Hallo"}],
            max_tokens=50
        )
        
        print(f"✅ {description} funktioniert!")
        print(f"   Antwort: {response.choices[0].message.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ {description} fehlgeschlagen: {e}")
        return False

def main():
    print("🚀 Kimi API Endpoint Test")
    print("=" * 50)
    
    # API-Key prüfen
    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        print("❌ Kein MOONSHOT_API_KEY in .env gefunden!")
        return
    
    print(f"🔑 API-Key: {api_key[:20]}...")
    
    # Verschiedene Endpoints testen
    endpoints = [
        ("https://api.moonshot.cn/v1", "Moonshot CN (Standard)"),
        ("https://api.moonshot.ai/v1", "Moonshot AI (Alternative)"),
    ]
    
    for base_url, description in endpoints:
        success = test_api_endpoint(base_url, description)
        if success:
            print(f"\n🎉 Erfolgreich! Verwende: {base_url}")
            break
    else:
        print(f"\n❌ Alle Endpoints fehlgeschlagen!")
        print("💡 Überprüfen Sie:")
        print("   - API-Key Gültigkeit")
        print("   - Internetverbindung")
        print("   - Moonshot Service Status")

if __name__ == "__main__":
    main() 