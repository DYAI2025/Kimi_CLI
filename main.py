#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kimi K2 Instruct - Einfacher Test
"""

import os
from kimi_client import KimiClient
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🚀 Teste Kimi K2 Instruct API...")
    
    try:
        # Client initialisieren
        kimi = KimiClient()
        
        print("✅ Kimi K2 Client erfolgreich initialisiert!")
        
        # Modell-Info anzeigen
        info = kimi.get_model_info()
        print(f"\n📋 Modell-Info:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        # Einfacher Test
        print(f"\n💬 Teste einfachen Chat...")
        response = kimi.simple_chat("Hallo! Kannst du auf Deutsch antworten?")
        print(f"\n🤖 Kimi antwortet:")
        print(response)
        
    except ValueError as e:
        print(f"❌ Konfigurationsfehler: {e}")
        print("\n💡 Setup-Hilfe:")
        print("1. Gehen Sie zu: https://api.together.xyz/settings/api-keys")
        print("2. Erstellen Sie einen API-Key")
        print("3. Setzen Sie TOGETHER_API_KEY in der .env-Datei")
        
    except Exception as e:
        print(f"❌ Fehler bei der API-Verbindung: {e}")

if __name__ == "__main__":
    main()
