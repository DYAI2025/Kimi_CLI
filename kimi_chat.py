#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kimi K2 Instruct - Interaktiver Chat (CLI)
Kommandozeilen-Chat-Interface für Kimi K2 Instruct
"""

import cmd
import sys
from kimi_client import KimiClient

class KimiChatCLI(cmd.Cmd):
    """Interaktiver Chat für Kimi K2 Instruct"""
    
    intro = '''
🤖 Willkommen bei Kimi K2 Instruct!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

State-of-the-Art MoE Modell mit 1T Parametern (32B aktiviert)
✨ Spezialisiert auf Coding, Reasoning und Tool Use
🌐 128K Token Kontext
⚡ Angetrieben von Together AI

Geben Sie 'help' ein für Kommandos oder chatten Sie direkt los!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    '''
    
    prompt = '> '
    
    def __init__(self):
        super().__init__()
        self.kimi = None
        self.streaming = True
        self.system_prompt = "You are Kimi, an AI assistant created by Moonshot AI."
        self.setup_client()
    
    def setup_client(self):
        """Initialisiert den Kimi Client"""
        try:
            self.kimi = KimiClient()
            print("✅ Kimi K2 Client erfolgreich initialisiert!")
            
            # Modell-Info anzeigen
            info = self.kimi.get_model_info()
            print(f"\n📋 Aktuelle Konfiguration:")
            print(f"   Modell: {info['model']}")
            print(f"   Temperature: {info['temperature']}")
            print(f"   Max Tokens: {info['max_tokens']}")
            print(f"   API Provider: {info['api_provider']}")
            print(f"   Kontext: 128K Token")
            print(f"   Parameter: 1T (32B aktiviert)")
            print()
            
        except Exception as e:
            print(f"❌ Fehler beim Initialisieren: {e}")
            print("\n💡 Setup-Hilfe:")
            print("1. Gehen Sie zu: https://api.together.xyz/settings/api-keys")
            print("2. Erstellen Sie einen API-Key")
            print("3. Setzen Sie TOGETHER_API_KEY in der .env-Datei")
            sys.exit(1)
    
    def default(self, line):
        """Behandelt normale Chat-Nachrichten"""
        if not line.strip():
            return
            
        if not self.kimi:
            print("❌ Kimi Client nicht verfügbar!")
            return
            
        print(f"\n🤖 Kimi:")
        print("─" * 50)
        
        try:
            if self.streaming:
                # Streaming-Modus
                messages = [{"role": "system", "content": self.system_prompt}]
                messages.append({"role": "user", "content": line})
                
                full_response = ""
                for chunk in self.kimi.chat_stream(messages):
                    print(chunk, end="", flush=True)
                    full_response += chunk
                print("\n")
            else:
                # Normaler Modus
                response = self.kimi.conversation_chat(line, self.system_prompt)
                print(response)
                print()
                
        except Exception as e:
            print(f"❌ Fehler: {e}")
        
        print("─" * 50)
    
    def do_model(self, args):
        """Wechselt das Modell: model <modell-name>"""
        if not args:
            models = self.kimi.get_models()
            print("Verfügbare Modelle:")
            for i, model in enumerate(models, 1):
                marker = "★" if model == self.kimi.model else " "
                print(f"  {marker} {i}. {model}")
            return
            
        try:
            self.kimi.set_model(args.strip())
            print(f"✅ Modell gewechselt zu: {args.strip()}")
        except ValueError as e:
            print(f"❌ {e}")
    
    def do_temp(self, args):
        """Setzt die Temperature: temp <0.0-1.0>"""
        if not args:
            print(f"Aktuelle Temperature: {self.kimi.temperature}")
            return
            
        try:
            temp = float(args.strip())
            if 0.0 <= temp <= 1.0:
                self.kimi.temperature = temp
                print(f"✅ Temperature gesetzt auf: {temp}")
            else:
                print("❌ Temperature muss zwischen 0.0 und 1.0 liegen")
        except ValueError:
            print("❌ Ungültiger Wert für Temperature")
    
    def do_tokens(self, args):
        """Setzt max_tokens: tokens <anzahl>"""
        if not args:
            print(f"Aktuelle Max Tokens: {self.kimi.max_tokens}")
            return
            
        try:
            tokens = int(args.strip())
            if tokens > 0:
                self.kimi.max_tokens = tokens
                print(f"✅ Max Tokens gesetzt auf: {tokens}")
            else:
                print("❌ Max Tokens muss größer als 0 sein")
        except ValueError:
            print("❌ Ungültiger Wert für Max Tokens")
    
    def do_stream(self, args):
        """Schaltet Streaming ein/aus: stream"""
        self.streaming = not self.streaming
        status = "ein" if self.streaming else "aus"
        print(f"✅ Streaming {status}geschaltet")
    
    def do_system(self, args):
        """Setzt System Prompt: system <prompt>"""
        if not args:
            print(f"Aktueller System Prompt:\n{self.system_prompt}")
            return
            
        self.system_prompt = args.strip()
        if self.kimi:
            self.kimi.clear_history()  # Verlauf löschen bei System Prompt Änderung
        print("✅ System Prompt aktualisiert (Chat-Verlauf gelöscht)")
    
    def do_clear(self, args):
        """Löscht den Chat-Verlauf: clear"""
        if self.kimi:
            self.kimi.clear_history()
        print("✅ Chat-Verlauf gelöscht")
    
    def do_info(self, args):
        """Zeigt Modell-Informationen: info"""
        if self.kimi:
            info = self.kimi.get_model_info()
            print("\n📋 Kimi K2 Instruct - Modell-Info:")
            print("━" * 40)
            for key, value in info.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
            print("━" * 40)
    
    def do_quit(self, args):
        """Beendet den Chat: quit oder q"""
        print("\n👋 Auf Wiedersehen!")
        return True
    
    def do_q(self, args):
        """Kurzform für quit: q"""
        return self.do_quit(args)
    
    def do_exit(self, args):
        """Beendet den Chat: exit"""
        return self.do_quit(args)
    
    def help_help(self):
        """Hilfe-Text"""
        print("""
Verfügbare Kommandos:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Chat:
  <nachricht>     - Chatte direkt mit Kimi
  clear           - Löscht den Chat-Verlauf

Konfiguration:
  model [name]    - Zeigt/wechselt Modell
  temp [wert]     - Zeigt/setzt Temperature (0.0-1.0)
  tokens [anzahl] - Zeigt/setzt Max Tokens
  stream          - Schaltet Streaming ein/aus
  system [prompt] - Zeigt/setzt System Prompt
  info            - Zeigt Modell-Informationen

Allgemein:
  help            - Zeigt diese Hilfe
  quit / q / exit - Beendet den Chat

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Über Kimi K2 Instruct:
• State-of-the-Art MoE Modell mit 1 Trillion Parametern (32B aktiviert)
• 128K Token Kontext für umfangreiche Dokumente
• Spezialisiert auf autonome Aufgaben, Coding und Tool Use
• Angetrieben von Together AI
        """)

def main():
    """Hauptfunktion"""
    try:
        chat = KimiChatCLI()
        chat.cmdloop()
    except KeyboardInterrupt:
        print("\n\n👋 Chat durch Benutzer beendet. Auf Wiedersehen!")
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    main() 