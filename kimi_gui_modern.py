#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kimi K2 Instruct - Moderne GUI mit TTS/STT
Farbenfrohe, minimalistische Benutzeroberfläche mit Spracheingabe und -ausgabe
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
import os
from datetime import datetime
from kimi_client import KimiClient
from dotenv import load_dotenv

# TTS/STT Imports
try:
    import pyttsx3
    import speech_recognition as sr
    TTS_AVAILABLE = True
    STT_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    STT_AVAILABLE = False
    print("⚠️  TTS/STT nicht verfügbar. Installieren Sie: pip install pyttsx3 speechrecognition pyaudio")

load_dotenv()

class ModernKimiGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styling()
        self.create_widgets()
        self.setup_client()
        self.setup_tts_stt()
        
        # Chat-Verlauf
        self.chat_history = []
        self.current_conversation = []
        
        # Status
        self.is_recording = False
        self.is_speaking = False
        
    def setup_window(self):
        """Fenster-Konfiguration"""
        self.root.title("🤖 Kimi K2 Instruct - Modern Chat")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        
        # Modernes Icon (falls vorhanden)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
            
    def setup_styling(self):
        """Moderne Farben und Styling"""
        # Farbschema: Moderne Blau-/Grau-Töne mit Akzenten
        self.colors = {
            'bg_primary': '#1a1a2e',      # Dunkelblau
            'bg_secondary': '#16213e',     # Mittleres Blau  
            'bg_tertiary': '#0f3460',      # Helles Blau
            'accent': '#e94560',           # Rot-Akzent
            'accent_light': '#f39c12',     # Orange-Akzent
            'text_primary': '#eee',        # Heller Text
            'text_secondary': '#bbb',      # Grauer Text
            'success': '#27ae60',          # Grün
            'warning': '#f39c12',          # Orange
            'error': '#e74c3c',           # Rot
            'chat_user': '#2980b9',       # User-Nachrichten
            'chat_ai': '#8e44ad',         # AI-Nachrichten
        }
        
        # Style konfigurieren
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom Styles
        style.configure('Modern.TFrame', background=self.colors['bg_primary'])
        style.configure('Header.TLabel', 
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 16, 'bold'))
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 11),
                       borderwidth=0,
                       focuscolor='none')
        style.map('Modern.TButton',
                 background=[('active', self.colors['accent_light'])])
        
        self.root.configure(bg=self.colors['bg_primary'])
        
    def create_widgets(self):
        """Erstelle alle GUI-Elemente"""
        # Haupt-Container
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Chat-Bereich
        self.create_chat_area(main_frame)
        
        # Eingabe-Bereich
        self.create_input_area(main_frame)
        
        # Status-Bar
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        """Header mit Titel und Kontrollen"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Titel
        title_label = tk.Label(header_frame,
                              text="🤖 Kimi K2 Instruct",
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT, pady=20)
        
        # Kontroll-Buttons
        controls_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        controls_frame.pack(side=tk.RIGHT, pady=20)
        
        # Model-Auswahl
        tk.Label(controls_frame, text="Model:", 
                font=('Segoe UI', 12),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=(0, 5))
        
        self.model_var = tk.StringVar(value=os.getenv("KIMI_MODEL", "Kimi-K2-Instruct"))
        model_combo = ttk.Combobox(controls_frame, textvariable=self.model_var,
                                  values=["Kimi-K2-Instruct", "meta-llama/Llama-3.1-8B-Instruct-Turbo"],
                                  state="readonly", width=25,
                                  font=('Segoe UI', 10))
        model_combo.pack(side=tk.LEFT, padx=5)
        
        # Temperature
        tk.Label(controls_frame, text="Temp:", 
                font=('Segoe UI', 12),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=(10, 5))
        
        self.temp_var = tk.DoubleVar(value=float(os.getenv("TEMPERATURE", "0.6")))
        temp_scale = tk.Scale(controls_frame, from_=0.1, to=2.0, resolution=0.1,
                             orient=tk.HORIZONTAL, variable=self.temp_var,
                             bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                             highlightthickness=0, length=100,
                             font=('Segoe UI', 9))
        temp_scale.pack(side=tk.LEFT, padx=5)
        
    def create_chat_area(self, parent):
        """Chat-Anzeige-Bereich"""
        chat_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=2)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Chat-Text mit Scrollbar
        self.chat_text = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Consolas', 14),  # Größere Schrift!
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            relief=tk.FLAT,
            padx=20,
            pady=20
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text-Tags für farbige Nachrichten
        self.chat_text.tag_configure("user", foreground=self.colors['chat_user'], font=('Consolas', 14, 'bold'))
        self.chat_text.tag_configure("assistant", foreground=self.colors['chat_ai'], font=('Consolas', 14))
        self.chat_text.tag_configure("system", foreground=self.colors['warning'], font=('Consolas', 12, 'italic'))
        self.chat_text.tag_configure("error", foreground=self.colors['error'], font=('Consolas', 12, 'bold'))
        
        # Willkommens-Nachricht
        self.add_message("system", "🤖 Kimi K2 Instruct bereit!\n📝 Geben Sie Ihre Nachricht ein oder nutzen Sie 🎤 für Spracheingabe.\n" + "="*60 + "\n")
        
    def create_input_area(self, parent):
        """Eingabe-Bereich mit Buttons"""
        input_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Eingabe-Text (größere Schrift)
        self.input_text = tk.Text(input_frame,
                                 height=4,
                                 font=('Segoe UI', 16),  # Größere Eingabe-Schrift!
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['text_primary'],
                                 insertbackground=self.colors['text_primary'],
                                 relief=tk.FLAT,
                                 padx=15,
                                 pady=10)
        self.input_text.pack(fill=tk.X, pady=(0, 10))
        
        # Tastenkürzel
        self.input_text.bind('<Return>', lambda e: self.send_message() or "break")
        self.input_text.bind('<Shift-Return>', lambda e: None)  # Neue Zeile mit Shift
        self.input_text.bind('<Control-Return>', lambda e: self.send_message() or "break")
        
        # Button-Leiste
        button_frame = tk.Frame(input_frame, bg=self.colors['bg_primary'])
        button_frame.pack(fill=tk.X)
        
        # Senden-Button
        send_btn = tk.Button(button_frame,
                           text="🚀 Senden (Enter)",
                           command=self.send_message,
                           bg=self.colors['accent'],
                           fg='white',
                           font=('Segoe UI', 12, 'bold'),
                           relief=tk.FLAT,
                           padx=20,
                           pady=8)
        send_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # TTS-Button (immer anzeigen)
        tts_text = "🔊 Sprechen" if TTS_AVAILABLE else "🔊 TTS (nicht verfügbar)"
        tts_color = self.colors['success'] if TTS_AVAILABLE else self.colors['bg_secondary']
        self.tts_btn = tk.Button(button_frame,
                               text=tts_text,
                               command=self.toggle_tts,
                               bg=tts_color,
                               fg='white',
                               font=('Segoe UI', 12),
                               relief=tk.FLAT,
                               padx=15,
                               pady=8)
        self.tts_btn.pack(side=tk.LEFT, padx=5)
        
        # STT-Button (immer anzeigen)
        stt_text = "🎤 Aufnehmen" if STT_AVAILABLE else "🎤 STT (nicht verfügbar)"
        stt_color = self.colors['warning'] if STT_AVAILABLE else self.colors['bg_secondary']
        self.stt_btn = tk.Button(button_frame,
                               text=stt_text,
                               command=self.toggle_recording,
                               bg=stt_color,
                               fg='white',
                               font=('Segoe UI', 12),
                               relief=tk.FLAT,
                               padx=15,
                               pady=8)
        self.stt_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear-Button
        clear_btn = tk.Button(button_frame,
                            text="🗑️ Leeren",
                            command=self.clear_chat,
                            bg=self.colors['bg_secondary'],
                            fg=self.colors['text_secondary'],
                            font=('Segoe UI', 12),
                            relief=tk.FLAT,
                            padx=15,
                            pady=8)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Speichern-Button
        save_btn = tk.Button(button_frame,
                           text="💾 Speichern",
                           command=self.save_chat,
                           bg=self.colors['bg_secondary'],
                           fg=self.colors['text_secondary'],
                           font=('Segoe UI', 12),
                           relief=tk.FLAT,
                           padx=15,
                           pady=8)
        save_btn.pack(side=tk.RIGHT, padx=5)
        
    def create_status_bar(self, parent):
        """Status-Leiste"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=30)
        status_frame.pack(fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame,
                                   text="Bereit",
                                   font=('Segoe UI', 10),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_secondary'],
                                   anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # API-Status
        api_key = os.getenv("TOGETHER_API_KEY", "")
        if not api_key or api_key in ["demo_key_please_replace", "your_api_key_here"]:
            api_status = "❌ API-Key Setup erforderlich"
            color = self.colors['error']
        else:
            api_status = "✅ API-Key konfiguriert"
            color = self.colors['success']
            
        self.api_status = tk.Label(status_frame,
                                 text=api_status,
                                 font=('Segoe UI', 10),
                                 bg=self.colors['bg_secondary'],
                                 fg=color,
                                 anchor=tk.E)
        self.api_status.pack(side=tk.RIGHT, padx=10, pady=5)
        
    def setup_client(self):
        """Kimi-Client initialisieren"""
        try:
            self.client = KimiClient()
            self.update_status("Kimi K2 Client initialisiert")
        except Exception as e:
            self.add_message("error", f"❌ Fehler beim Initialisieren: {str(e)}\n")
            self.client = None
            
    def setup_tts_stt(self):
        """TTS und STT initialisieren"""
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Stimme konfigurieren
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # Deutsche Stimme bevorzugen
                    for voice in voices:
                        if 'german' in voice.name.lower() or 'deutsch' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                
                self.tts_engine.setProperty('rate', int(os.getenv('VOICE_RATE', '180')))
                self.tts_engine.setProperty('volume', float(os.getenv('VOICE_VOLUME', '0.8')))
                self.update_status("TTS initialisiert")
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
                self.update_status("STT initialisiert")
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
            self.chat_text.insert(tk.END, f"🤖 Kimi [{timestamp}]:\n", "assistant")
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
            self.add_message("error", "❌ Kein Kimi-Client verfügbar. Bitte API-Key konfigurieren.\n")
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
        self.update_status("Sende Nachricht...")
        
    def _send_message_thread(self, user_input):
        """Nachricht in separatem Thread senden"""
        try:
            # Client konfigurieren
            self.client.model = self.model_var.get()
            self.client.temperature = self.temp_var.get()
            
            # Stream-Response verarbeiten
            response_content = ""
            
            for chunk in self.client.chat_stream(self.current_conversation):
                if chunk:
                    response_content += chunk
                    # UI in Main-Thread aktualisieren
                    self.root.after(0, self._update_streaming_response, response_content)
            
            # Vollständige Antwort zum Verlauf hinzufügen
            self.current_conversation.append({"role": "assistant", "content": response_content})
            
            # TTS abspielen (falls aktiviert)
            if hasattr(self, 'tts_enabled') and self.tts_enabled and self.tts_engine:
                threading.Thread(target=self._speak_text, args=(response_content,), daemon=True).start()
                
            self.root.after(0, self.update_status, "Bereit")
            
        except Exception as e:
            error_msg = f"❌ Fehler: {str(e)}\n"
            self.root.after(0, self.add_message, "error", error_msg)
            self.root.after(0, self.update_status, "Fehler aufgetreten")
            
    def _update_streaming_response(self, content):
        """Streaming-Response in Echtzeit anzeigen"""
        # Letzte AI-Nachricht finden und aktualisieren
        self.chat_text.config(state=tk.NORMAL)
        
        # Text-Widget Inhalt analysieren
        full_text = self.chat_text.get("1.0", tk.END)
        
        # Prüfen ob bereits eine AI-Antwort gestartet wurde
        if "🤖 Kimi [" in full_text and full_text.count("🤖 Kimi [") > 0:
            # Letzte AI-Nachricht finden und ersetzen
            lines = full_text.split('\n')
            last_ai_index = -1
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].startswith("🤖 Kimi ["):
                    last_ai_index = i
                    break
            
            if last_ai_index >= 0:
                # Alles nach der letzten AI-Nachricht löschen
                line_count = last_ai_index + 2  # Header + eine Zeile
                self.chat_text.delete(f"{line_count}.0", tk.END)
                self.chat_text.insert(tk.END, f"{content}\n\n")
        else:
            # Erste AI-Antwort - neue hinzufügen
            timestamp = datetime.now().strftime("%H:%M")
            self.chat_text.insert(tk.END, f"🤖 Kimi [{timestamp}]:\n", "assistant")
            self.chat_text.insert(tk.END, f"{content}\n\n")
        
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
        
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
        self.stt_btn.configure(text="⏹️ Stop", bg=self.colors['error'])
        self.update_status("🎤 Aufnahme läuft...")
        
        threading.Thread(target=self._record_audio, daemon=True).start()
        
    def _record_audio(self):
        """Audio in separatem Thread aufnehmen"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
            
            # Speech-to-Text
            self.root.after(0, self.update_status, "🔄 Verarbeite Sprache...")
            
            try:
                # Deutsch bevorzugen, Englisch als Fallback
                text = self.recognizer.recognize_google(audio, language='de-DE')
            except:
                try:
                    text = self.recognizer.recognize_google(audio, language='en-US')
                except:
                    text = None
            
            if text:
                # Erkannten Text in Eingabefeld einfügen
                self.root.after(0, self._insert_recognized_text, text)
                self.root.after(0, self.update_status, f"✅ Erkannt: {text[:30]}...")
            else:
                self.root.after(0, self.add_message, "error", "❌ Sprache nicht erkannt\n")
                self.root.after(0, self.update_status, "Sprache nicht erkannt")
                
        except Exception as e:
            self.root.after(0, self.add_message, "error", f"❌ Aufnahme-Fehler: {str(e)}\n")
            self.root.after(0, self.update_status, "Aufnahme-Fehler")
        finally:
            self.root.after(0, self.stop_recording)
            
    def _insert_recognized_text(self, text):
        """Erkannten Text in Eingabefeld einfügen"""
        current_text = self.input_text.get("1.0", tk.END).strip()
        if current_text:
            self.input_text.insert(tk.END, f" {text}")
        else:
            self.input_text.insert("1.0", text)
            
    def stop_recording(self):
        """Sprachaufnahme stoppen"""
        self.is_recording = False
        if hasattr(self, 'stt_btn'):
            self.stt_btn.configure(text="🎤 Aufnehmen", bg=self.colors['warning'])
        
    def toggle_tts(self):
        """TTS ein-/ausschalten"""
        if not TTS_AVAILABLE:
            self.add_message("error", "❌ Text-to-Speech nicht verfügbar!\n💡 Installieren Sie: pip3 install pyttsx3\n")
            return
            
        if not hasattr(self, 'tts_enabled'):
            self.tts_enabled = False
            
        self.tts_enabled = not self.tts_enabled
        
        if self.tts_enabled:
            self.tts_btn.configure(text="🔇 Stumm", bg=self.colors['error'])
            self.update_status("TTS aktiviert")
        else:
            self.tts_btn.configure(text="🔊 Sprechen", bg=self.colors['success'])
            self.update_status("TTS deaktiviert")
            
    def _speak_text(self, text):
        """Text per TTS ausgeben"""
        if self.tts_engine and not self.is_speaking:
            try:
                self.is_speaking = True
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS Fehler: {e}")
            finally:
                self.is_speaking = False
                
    def clear_chat(self):
        """Chat leeren"""
        if messagebox.askyesno("Chat leeren", "Möchten Sie den Chat-Verlauf wirklich löschen?"):
            self.chat_text.config(state=tk.NORMAL)
            self.chat_text.delete("1.0", tk.END)
            self.chat_text.config(state=tk.DISABLED)
            
            self.current_conversation = []
            self.add_message("system", "🔄 Chat geleert. Neues Gespräch gestartet.\n" + "="*60 + "\n")
            self.update_status("Chat geleert")
            
    def save_chat(self):
        """Chat speichern"""
        if not self.current_conversation:
            messagebox.showinfo("Info", "Kein Chat-Verlauf zum Speichern vorhanden.")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
            title="Chat speichern"
        )
        
        if filename:
            try:
                chat_data = {
                    "timestamp": datetime.now().isoformat(),
                    "model": self.model_var.get(),
                    "temperature": self.temp_var.get(),
                    "conversation": self.current_conversation
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    if filename.endswith('.json'):
                        json.dump(chat_data, f, ensure_ascii=False, indent=2)
                    else:
                        # Text-Format
                        f.write(f"# Kimi K2 Chat - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                        for msg in self.current_conversation:
                            role = "🙋 Du" if msg["role"] == "user" else "🤖 Kimi"
                            f.write(f"{role}:\n{msg['content']}\n\n{'='*60}\n\n")
                
                self.update_status(f"Chat gespeichert: {filename}")
                messagebox.showinfo("Erfolg", f"Chat gespeichert:\n{filename}")
                
            except Exception as e:
                self.add_message("error", f"❌ Speichern fehlgeschlagen: {str(e)}\n")
                
    def update_status(self, message):
        """Status aktualisieren"""
        self.status_label.configure(text=message)
        
    def run(self):
        """GUI starten"""
        # Fenster zentrieren
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.root.mainloop()

def main():
    """Hauptfunktion"""
    print("🚀 Starte Moderne Kimi K2 GUI...")
    
    # API-Key prüfen
    api_key = os.getenv("TOGETHER_API_KEY", "")
    if not api_key or api_key in ["demo_key_please_replace", "your_api_key_here"]:
        print("⚠️  Demo-API-Key erkannt. Bitte konfigurieren Sie einen echten API-Key in der .env-Datei:")
        print("   TOGETHER_API_KEY=your_actual_api_key_here")
        print("   Registrierung: https://api.together.xyz/settings/api-keys")
    
    app = ModernKimiGUI()
    app.run()

if __name__ == "__main__":
    main() 