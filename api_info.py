#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kimi K2 Instruct - API Setup Info
Zeigt Informationen zur API-Konfiguration ohne gültigen Key zu benötigen
"""

import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🤖 Kimi K2 Instruct - API Setup Information")
    print("━" * 60)
    
    # API-Key Status prüfen
    api_key = os.getenv("MOONSHOT_API_KEY", "")
    
    if not api_key:
        print("❌ Kein MOONSHOT_API_KEY in .env gefunden")
        status = "❌ Nicht konfiguriert"
    elif api_key == "sk-demo_key_please_replace":
        print("⚠️  Demo-API-Key gefunden - Setup erforderlich")
        status = "⚠️ Setup erforderlich"
    else:
        print("✅ API-Key konfiguriert")
        status = "✅ Konfiguriert"
    
    print()
    print("📋 Konfiguration:")
    print(f"   Status: {status}")
    print(f"   Model: {os.getenv('KIMI_MODEL', 'moonshotai/Kimi-K2-Instruct')}")
    print(f"   Temperature: {os.getenv('TEMPERATURE', '0.6')}")
    
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"   API-Key: {masked_key}")
    
    print()
    print("🛠️ Setup-Anleitung:")
    print("1. Besuchen Sie https://platform.moonshot.ai")
    print("2. Registrieren Sie sich kostenlos")
    print("3. Erstellen Sie einen neuen API-Key")
    print("4. Bearbeiten Sie die .env-Datei:")
    print("   MOONSHOT_API_KEY=sk-your_actual_api_key_here")
    print()
    print("🎯 Über Kimi K2 Instruct:")
    print("• State-of-the-Art MoE Modell mit 1 Trillion Parametern")
    print("• 32B Parameter aktiviert pro Forward Pass")
    print("• 128K Token Kontext für umfangreiche Dokumente")
    print("• Spezialisiert auf Coding, Reasoning und Tool Use")
    print("• Powered by Moonshot AI")
    print()
    print("🚀 Starten:")
    print("• CLI Chat: python3 kimi_chat.py")
    print("• GUI Chat: python3 kimi_gui.py")
    print("• One-Click: ./start_kimi.command")
    print("━" * 60)

if __name__ == "__main__":
    main() 