#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kimi K2 Instruct - Moderne GUI mit ECHTER Moonshot AI
Farbenfrohe, minimalistische Benutzeroberfläche mit Spracheingabe und -ausgabe
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
import os
from datetime import datetime
from kimi_client_moonshot import KimiMoonshotClient
from dotenv import load_dotenv

# TTS/STT Imports
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False

load_dotenv()

class ModernKimiMoonshotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌙 Kimi K2 Instruct - Moonshot AI")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')
        
        # Moderne Farben
        self.colors = {
            'bg_primary': '#2c3e50',      # Dunkler Haupthintergrund
            'bg_secondary': '#34495e',     # Sekundärer Hintergrund
            'accent': '#3498db',           # Blaue Akzentfarbe
            'success': '#2ecc71',          # Grün für Erfolg
            'warning': '#f39c12',          # Orange für Warnung
            'error': '#e74c3c',            # Rot für Fehler
            'text': '#ecf0f1',             # Heller Text
            'text_dark': '#34495e'         # Dunkler Text
        }
        
        # Variablen
        self.current_conversation = []
        self.tts_enabled = False
        self.is_recording = False
        
        # Client und TTS/STT
        self.client = None
        self.tts_engine = None
        self.recognizer = None
        self.microphone = None
        
        # Setup
        self.setup_ui()
        self.setup_client()
        self.setup_tts_stt()
        
        print("🚀 Starte Moderne Kimi K2 GUI mit Moonshot AI...")
        
    def setup_ui(self):
        """Moderne Benutzeroberfläche erstellen"""
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Titel
        title_label = tk.Label(header_frame,
                              text="🌙 Kimi K2 Instruct",
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg_primary'])
        title_label.pack(side=tk.LEFT, anchor=tk.W, pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="Powered by Moonshot AI • 1T Parameter MoE • 128K Kontext",
                                 font=('Segoe UI', 12),
                                 fg=self.colors['text'],
                                 bg=self.colors['bg_primary'])
        subtitle_label.pack(side=tk.LEFT, anchor=tk.W, padx=(20, 0), pady=20)
        
        # Haupt-Container
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Linke Seite - Chat
        chat_frame = tk.Frame(main_container, bg=self.colors['bg_secondary'])
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Chat Header
        chat_header = tk.Frame(chat_frame, bg=self.colors['bg_secondary'], height=50)
        chat_header.pack(fill=tk.X, padx=15, pady=15)
        
        chat_title = tk.Label(chat_header,
                             text="💬 Chat mit Kimi K2",
                             font=('Segoe UI', 16, 'bold'),
                             fg=self.colors['text'],
                             bg=self.colors['bg_secondary'])
        chat_title.pack(side=tk.LEFT)
        
        # Chat-Display (große Schrift!)
        self.chat_text = scrolledtext.ScrolledText(chat_frame,
                                                  wrap=tk.WORD,
                                                  width=70,
                                                  height=20,
                                                  font=('Consolas', 14),  # Große Schrift!
                                                  bg='#1a252f',
                                                  fg=self.colors['text'],
                                                  insertbackground=self.colors['accent'],
                                                  selectbackground=self.colors['accent'],
                                                  state=tk.DISABLED)
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Eingabe-Bereich
        input_frame = tk.Frame(chat_frame, bg=self.colors['bg_secondary'])
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Eingabe-Text (große Schrift!)
        self.input_text = tk.Text(input_frame,
                                 height=3,
                                 font=('Segoe UI', 14),  # Große Schrift!
                                 bg='#1a252f',
                                 fg=self.colors['text'],
                                 insertbackground=self.colors['accent'],
                                 wrap=tk.WORD)
        self.input_text.pack(fill=tk.X, pady=(0, 10))
        
        # Tastenkürzel - Enter soll senden!
        self.input_text.bind('<Return>', lambda e: self.send_message() or "break")
        self.input_text.bind('<Shift-Return>', lambda e: None)  # Neue Zeile mit Shift
        
        # Button-Bereich
        button_frame = tk.Frame(input_frame, bg=self.colors['bg_secondary'])
        button_frame.pack(fill=tk.X)
        
        # Senden-Button (große Schrift!)
        send_btn = tk.Button(button_frame,
                           text="🚀 Senden (Enter)",
                           command=self.send_message,
                           bg=self.colors['accent'],
                           fg='white',
                           font=('Segoe UI', 14, 'bold'),  # Große Schrift!
                           relief=tk.FLAT,
                           padx=25,
                           pady=10,
                           cursor='hand2')
        send_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # TTS-Button (immer sichtbar)
        self.tts_btn = tk.Button(button_frame,
                               text="🔊 Sprechen" if TTS_AVAILABLE else "🔊 TTS (nicht verfügbar)",
                               command=self.toggle_tts,
                               bg=self.colors['success'] if TTS_AVAILABLE else self.colors['warning'],
                               fg='white',
                               font=('Segoe UI', 12),
                               relief=tk.FLAT,
                               padx=20,
                               pady=10,
                               cursor='hand2')
        self.tts_btn.pack(side=tk.LEFT, padx=5)
        
        # STT-Button (immer sichtbar)
        self.stt_btn = tk.Button(button_frame,
                               text="🎤 Aufnehmen" if STT_AVAILABLE else "🎤 STT (nicht verfügbar)",
                               command=self.toggle_recording,
                               bg=self.colors['warning'] if STT_AVAILABLE else self.colors['error'],
                               fg='white',
                               font=('Segoe UI', 12),
                               relief=tk.FLAT,
                               padx=20,
                               pady=10,
                               cursor='hand2')
        self.stt_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear Button
        clear_btn = tk.Button(button_frame,
                             text="🗑️ Löschen",
                             command=self.clear_chat,
                             bg=self.colors['error'],
                             fg='white',
                             font=('Segoe UI', 12),
                             relief=tk.FLAT,
                             padx=20,
                             pady=10,
                             cursor='hand2')
        clear_btn.pack(side=tk.RIGHT)
        
        # Rechte Seite - Konfiguration
        config_frame = tk.Frame(main_container, bg=self.colors['bg_secondary'], width=350)
        config_frame.pack(side=tk.RIGHT, fill=tk.Y)
        config_frame.pack_propagate(False)
        
        # Config Header
        config_header = tk.Frame(config_frame, bg=self.colors['bg_secondary'], height=50)
        config_header.pack(fill=tk.X, padx=15, pady=15)
        
        config_title = tk.Label(config_header,
                               text="⚙️ Konfiguration",
                               font=('Segoe UI', 16, 'bold'),
                               fg=self.colors['text'],
                               bg=self.colors['bg_secondary'])
        config_title.pack(side=tk.LEFT)
        
        # Model-Auswahl
        model_frame = tk.Frame(config_frame, bg=self.colors['bg_secondary'])
        model_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(model_frame,
                text="Model:",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.model_var = tk.StringVar(value="kimi-k2-instruct")
        model_combo = ttk.Combobox(model_frame,
                                  textvariable=self.model_var,
                                  values=["kimi-k2-instruct", "kimi-k2-base", "moonshot-v1-128k"],
                                  state="readonly",
                                  font=('Segoe UI', 11))
        model_combo.pack(fill=tk.X, pady=5)
        
        # Temperature
        temp_frame = tk.Frame(config_frame, bg=self.colors['bg_secondary'])
        temp_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(temp_frame,
                text="Temperature: 0.6",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.temp_var = tk.DoubleVar(value=0.6)
        temp_scale = tk.Scale(temp_frame,
                             from_=0.0,
                             to=1.0,
                             resolution=0.1,
                             orient=tk.HORIZONTAL,
                             variable=self.temp_var,
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text'],
                             highlightthickness=0,
                             font=('Segoe UI', 10))
        temp_scale.pack(fill=tk.X, pady=5)
        
        # Status-Bereich
        status_frame = tk.Frame(config_frame, bg=self.colors['bg_secondary'])
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=15)
        
        tk.Label(status_frame,
                text="Status:",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.status_label = tk.Label(status_frame,
                                    text="Initialisiere...",
                                    font=('Segoe UI', 11),
                                    fg=self.colors['warning'],
                                    bg=self.colors['bg_secondary'],
                                    wraplength=300)
        self.status_label.pack(anchor=tk.W, pady=5)
        
        # API-Status
        self.api_status = tk.Label(status_frame,
                                  text="API: Nicht verbunden",
                                  font=('Segoe UI', 10),
                                  fg=self.colors['error'],
                                  bg=self.colors['bg_secondary'])
        self.api_status.pack(anchor=tk.W, pady=2)
        
        # Willkommens-Nachricht
        self.add_message("system", "🌙 Willkommen bei Kimi K2 Instruct von Moonshot AI!\n\n✨ 1 Trillion Parameter MoE Modell\n🧠 32B aktivierte Parameter\n📚 128K Token Kontext\n🛠️ Native Tool Calling\n\n💡 Drücken Sie Enter zum Senden oder nutzen Sie die Mikrofon-Taste für Spracheingabe!\n")
        
    def setup_client(self):
        """Moonshot AI Kimi-Client initialisieren"""
        try:
            self.client = KimiMoonshotClient()
            self.update_status("✅ Moonshot AI Client initialisiert")
            self.api_status.configure(text="API: Moonshot AI verbunden", fg=self.colors['success'])
        except Exception as e:
            self.add_message("error", f"❌ Fehler beim Initialisieren: {str(e)}\n\n💡 Setup erforderlich:\n1. Registrieren Sie sich bei: https://platform.moonshot.ai\n2. Erstellen Sie einen API-Key\n3. Setzen Sie MOONSHOT_API_KEY in der .env-Datei\n")
            self.client = None
            self.api_status.configure(text="API: Fehler", fg=self.colors['error'])
            
    def setup_tts_stt(self):
        """TTS und STT initialisieren"""
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Deutsche Stimme bevorzugen
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    for voice in voices:
                        if 'german' in voice.name.lower() or 'deutsch' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                
                self.tts_engine.setProperty('rate', int(os.getenv('VOICE_RATE', '180')))
                self.tts_engine.setProperty('volume', float(os.getenv('VOICE_VOLUME', '0.8')))
                self.update_status("🔊 TTS initialisiert")
            except Exception as e:
                print(f"TTS Fehler: {e}")
                self.tts_engine = None
        
        if STT_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                # Mikrofon kalibrieren
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                self.update_status("🎤 STT initialisiert")
            except Exception as e:
                print(f"STT Fehler: {e}")
                self.recognizer = None
                self.microphone = None
                
    def add_message(self, role, content):
        """Nachricht zum Chat hinzufügen"""
        self.chat_text.config(state=tk.NORMAL)
        
        if role == "user":
            timestamp = datetime.now().strftime("%H:%M")
            self.chat_text.insert(tk.END, f"🙋 Du [{timestamp}]:\n", "user")
            self.chat_text.insert(tk.END, f"{content}\n\n")
        elif role == "assistant":
            timestamp = datetime.now().strftime("%H:%M")
            self.chat_text.insert(tk.END, f"🌙 Kimi [{timestamp}]:\n", "assistant")
            self.chat_text.insert(tk.END, f"{content}\n\n")
        elif role == "system":
            self.chat_text.insert(tk.END, content, "system")
        elif role == "error":
            self.chat_text.insert(tk.END, content, "error")
            
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
        
    def send_message(self):
        """Nachricht senden"""
        if not self.client:
            self.add_message("error", "❌ Kein Moonshot AI Client verfügbar.\n💡 Bitte konfigurieren Sie MOONSHOT_API_KEY in der .env-Datei\n")
            return
            
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            return
            
        # User-Nachricht anzeigen
        self.add_message("user", user_input)
        self.input_text.delete("1.0", tk.END)
        
        # Chat-Verlauf aktualisieren
        self.current_conversation.append({"role": "user", "content": user_input})
        
        # In Thread senden (UI nicht blockieren)
        threading.Thread(target=self._send_message_thread, args=(user_input,), daemon=True).start()
        self.update_status("🌙 Kimi antwortet...")
        
    def _send_message_thread(self, user_input):
        """Nachricht in separatem Thread senden"""
        try:
            # Client konfigurieren
            self.client.model = self.model_var.get()
            self.client.temperature = self.temp_var.get()
            
            # Stream-Response verarbeiten
            response_content = ""
            
            # Placeholder für Response
            self.root.after(0, lambda: self.add_message("assistant", ""))
            
            for chunk in self.client.chat_stream(self.current_conversation):
                if chunk:
                    response_content += chunk
                    # UI in Main-Thread aktualisieren
                    self.root.after(0, self._update_streaming_response, response_content)
            
            # Vollständige Antwort zum Verlauf hinzufügen
            self.current_conversation.append({"role": "assistant", "content": response_content})
            
            # TTS abspielen (falls aktiviert)
            if self.tts_enabled and self.tts_engine and response_content:
                threading.Thread(target=self._speak_text, args=(response_content,), daemon=True).start()
                
            self.root.after(0, self.update_status, "✅ Bereit")
            
        except Exception as e:
            self.root.after(0, lambda: self.add_message("error", f"❌ Fehler: {str(e)}\n"))
            self.root.after(0, self.update_status, "❌ Fehler")
    
    def _update_streaming_response(self, content):
        """Streaming-Response im Chat aktualisieren"""
        self.chat_text.config(state=tk.NORMAL)
        
        # Letzte assistant-Nachricht finden und aktualisieren
        text_content = self.chat_text.get("1.0", tk.END)
        lines = text_content.split('\n')
        
        # Finde die letzte Kimi-Nachricht und ersetze sie
        for i in range(len(lines)-1, -1, -1):
            if lines[i].startswith("🌙 Kimi ["):
                # Alles nach dieser Zeile löschen
                line_start = text_content.find(lines[i])
                char_pos = f"1.0+{line_start}c"
                self.chat_text.delete(char_pos, tk.END)
                
                # Neue Antwort einfügen
                timestamp = datetime.now().strftime("%H:%M")
                self.chat_text.insert(tk.END, f"🌙 Kimi [{timestamp}]:\n{content}\n\n")
                break
        
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
    
    def toggle_tts(self):
        """TTS ein-/ausschalten"""
        if not TTS_AVAILABLE:
            self.add_message("error", "❌ Text-to-Speech nicht verfügbar!\n💡 Installieren Sie: pip3 install pyttsx3\n")
            return
            
        self.tts_enabled = not self.tts_enabled
        
        if self.tts_enabled:
            self.tts_btn.configure(text="🔇 Stumm", bg=self.colors['error'])
            self.update_status("🔊 TTS aktiviert")
        else:
            self.tts_btn.configure(text="🔊 Sprechen", bg=self.colors['success'])
            self.update_status("🔇 TTS deaktiviert")
    
    def toggle_recording(self):
        """Sprachaufnahme starten/stoppen"""
        if not STT_AVAILABLE:
            self.add_message("error", "❌ Speech-to-Text nicht verfügbar!\n💡 Installieren Sie: pip3 install speechrecognition pyaudio\n")
            return
            
        if not self.recognizer or not self.microphone:
            self.add_message("error", "❌ Mikrofon nicht verfügbar\n")
            return
            
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Sprachaufnahme starten"""
        self.is_recording = True
        self.stt_btn.configure(text="⏹️ Stopp", bg=self.colors['error'])
        self.update_status("🎤 Aufnahme läuft...")
        
        threading.Thread(target=self._record_audio, daemon=True).start()
    
    def stop_recording(self):
        """Sprachaufnahme stoppen"""
        self.is_recording = False
        self.stt_btn.configure(text="🎤 Aufnehmen", bg=self.colors['warning'])
        self.update_status("⏹️ Aufnahme gestoppt")
    
    def _record_audio(self):
        """Audio aufnehmen und in Text umwandeln"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
            
            # Spracherkennung
            text = self.recognizer.recognize_google(audio, language='de-DE')
            
            # Text in Eingabefeld einfügen
            self.root.after(0, lambda: self.input_text.insert(tk.END, text))
            self.root.after(0, self.stop_recording)
            
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.add_message("error", "❌ Aufnahme-Timeout\n"))
            self.root.after(0, self.stop_recording)
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.add_message("error", "❌ Sprache nicht verstanden\n"))
            self.root.after(0, self.stop_recording)
        except Exception as e:
            self.root.after(0, lambda: self.add_message("error", f"❌ STT-Fehler: {str(e)}\n"))
            self.root.after(0, self.stop_recording)
    
    def _speak_text(self, text):
        """Text vorlesen"""
        try:
            # Nur die ersten 500 Zeichen vorlesen (zu lange Texte sind nervig)
            if len(text) > 500:
                text = text[:500] + "..."
            
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS-Fehler: {e}")
    
    def clear_chat(self):
        """Chat löschen"""
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete("1.0", tk.END)
        self.chat_text.config(state=tk.DISABLED)
        
        self.current_conversation = []
        if self.client:
            self.client.clear_conversation()
        
        # Willkommens-Nachricht erneut anzeigen
        self.add_message("system", "🌙 Chat gelöscht. Bereit für neue Unterhaltung!\n")
        self.update_status("✅ Chat gelöscht")
    
    def update_status(self, message):
        """Status aktualisieren"""
        self.status_label.configure(text=message)
    
    def run(self):
        """GUI starten"""
        self.root.mainloop()

def main():
    """Hauptfunktion"""
    
    # API-Key-Check
    api_key = os.getenv("MOONSHOT_API_KEY", "")
    if not api_key or api_key == "sk-demo_key_please_replace":
        print("⚠️  Demo-API-Key erkannt. Bitte konfigurieren Sie einen echten API-Key in der .env-Datei:")
        print("   MOONSHOT_API_KEY=sk-your_actual_api_key_here")
        print("   Registrierung: https://platform.moonshot.ai")
        print()
    
    # GUI starten
    app = ModernKimiMoonshotGUI()
    app.run()

if __name__ == "__main__":
    main() 