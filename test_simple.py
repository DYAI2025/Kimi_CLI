#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Einfacher Kimi K2 Test
Testet ob die API-Verbindung funktioniert
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_api():
    print("🧪 Teste Kimi K2 API-Verbindung...")
    
    api_key = os.getenv("TOGETHER_API_KEY", "")
    
    if not api_key or api_key == "demo_key_please_replace":
        print("❌ Demo-API-Key aktiv - Echter API-Key erforderlich")
        print("\n💡 Setup:")
        print("1. Besuchen Sie: https://api.together.xyz/settings/api-keys")
        print("2. Erstellen Sie einen API-Key")
        print("3. Setzen Sie ihn in der .env-Datei:")
        print("   TOGETHER_API_KEY=your_actual_api_key_here")
        return False
    
    try:
        from kimi_client import KimiClient
        
        print("✅ Dependencies OK")
        print(f"✅ API-Key gefunden: {api_key[:8]}...{api_key[-4:]}")
        
        # Client testen
        client = KimiClient()
        print("✅ Client initialisiert")
        
        # Einfache Anfrage
        response = client.chat("Hallo! Antworte kurz auf Deutsch.")
        print("✅ API-Verbindung erfolgreich!")
        print(f"\n🤖 Kimi antwortet:")
        print(f"   {response[:100]}{'...' if len(response) > 100 else ''}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    
    if success:
        print("\n🎉 Alles funktioniert! Sie können jetzt die GUI oder CLI starten.")
        print("\n🚀 Starten:")
        print("   ./start_kimi.command")
        print("   python3 kimi_gui_modern.py")
        print("   python3 kimi_chat.py")
    else:
        print("\n⚠️  Setup erforderlich. Befolgen Sie die Anweisungen oben.") 