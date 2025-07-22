#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Moonshot AI Test - Echter Kimi K2 Instruct Test
Testet die direkte Moonshot AI API-Verbindung
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_moonshot_api():
    print("🌙 Teste Moonshot AI Kimi K2 Instruct...")
    print("=" * 50)
    
    api_key = os.getenv("MOONSHOT_API_KEY", "")
    
    if not api_key or api_key == "sk-demo_key_please_replace":
        print("❌ Demo-API-Key aktiv - Echter Moonshot API-Key erforderlich")
        print("\n💡 Setup:")
        print("1. Besuchen Sie: https://platform.moonshot.ai")
        print("2. Registrieren Sie sich kostenlos")
        print("3. Erstellen Sie einen API-Key im Dashboard")
        print("4. Setzen Sie ihn in der .env-Datei:")
        print("   MOONSHOT_API_KEY=sk-your_actual_api_key_here")
        return False
    
    try:
        from kimi_client_moonshot import KimiMoonshotClient
        
        print("✅ Moonshot Client Import OK")
        print(f"✅ API-Key gefunden: {api_key[:15]}...{api_key[-8:]}")
        
        # Client testen
        client = KimiMoonshotClient()
        print("✅ Moonshot Client initialisiert")
        
        # Model-Info
        info = client.get_model_info()
        print(f"✅ Model: {info['model']}")
        print(f"✅ API Provider: {info['api_provider']}")
        print(f"✅ Base URL: {info['base_url']}")
        
        # Einfache Anfrage
        print("\n💬 Teste Chat...")
        response = client.chat("Hallo! Bitte antworte kurz auf Deutsch und stelle dich vor.")
        print("✅ Moonshot API-Verbindung erfolgreich!")
        print(f"\n🌙 Kimi antwortet:")
        print(f"   {response[:150]}{'...' if len(response) > 150 else ''}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        
        # Hilfreiche Fehlermeldungen
        error_str = str(e).lower()
        if "404" in error_str or "not found" in error_str:
            print("\n💡 Mögliche Ursachen:")
            print("   - API-Key ist ungültig")
            print("   - Model-Name ist falsch")
            print("   - Account hat keine Berechtigung für Kimi K2")
        elif "401" in error_str or "unauthorized" in error_str:
            print("\n💡 API-Key Problem:")
            print("   - Ungültiger oder abgelaufener API-Key")
            print("   - Falsche API-Key-Format")
        elif "429" in error_str or "rate limit" in error_str:
            print("\n💡 Rate Limit:")
            print("   - Zu viele Anfragen")
            print("   - Account-Limit erreicht")
        
        return False

if __name__ == "__main__":
    success = test_moonshot_api()
    
    if success:
        print("\n🎉 Moonshot AI funktioniert perfekt!")
        print("\n🚀 Starten Sie die moderne GUI:")
        print("   python3 kimi_gui_moonshot.py")
    else:
        print("\n⚠️  Setup erforderlich. Befolgen Sie die Anweisungen oben.")
        print("\n📚 Weitere Hilfe:")
        print("   - Moonshot AI Docs: https://platform.moonshot.ai/docs")
        print("   - Kimi K2 Model Card: https://huggingface.co/moonshotai/Kimi-K2-Instruct") 