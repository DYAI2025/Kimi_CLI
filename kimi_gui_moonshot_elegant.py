#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kimi K2 Instruct - Elegante GUI im Void AI Chat Stil
Moderne, minimalistische Benutzeroberfläche mit dunklem Theme
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
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

class ElegantKimiMoonshotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌙 Kimi K2 Instruct - Moonshot AI")
        self.root.geometry("1600x1000")
        self.root.minsize(1200, 800)
        
        # Void AI Chat inspirierte Farben
        self.colors = {
            'bg_primary': '#0a0a0a',        # Sehr dunkler Haupthintergrund
            'bg_secondary': '#1a1a1a',      # Sekundärer Hintergrund
            'bg_tertiary': '#2a2a2a',       # Karten/Panel Hintergrund
            'bg_chat': '#1e1e1e',           # Chat-Bereich
            'accent_purple': '#a855f7',     # Lila Akzent
            'accent_blue': '#3b82f6',       # Blauer Akzent
            'accent_green': '#10b981',      # Grüner Akzent
            'text_primary': '#ffffff',      # Haupttext
            'text_secondary': '#a3a3a3',    # Sekundärer Text
            'text_muted': '#737373',        # Gedämpfter Text
            'border': '#374151',            # Rahmenfarbe
            'hover': '#374151',             # Hover-Effekt
            'success': '#10b981',           # Erfolg
            'warning': '#f59e0b',           # Warnung
            'error': '#ef4444'              # Fehler
        }
        
        # Moderne Fonts (ohne 'medium' style da nicht unterstützt)
        self.fonts = {
            'title': ('Inter', 24, 'bold'),
            'subtitle': ('Inter', 14, 'normal'),
            'body': ('Inter', 13, 'normal'),
            'chat': ('JetBrains Mono', 13, 'normal'),
            'button': ('Inter', 12, 'bold'),
            'small': ('Inter', 11, 'normal')
        }
        
        # Fallback fonts wenn Inter nicht verfügbar
        try:
            test_font = font.Font(family='Inter', size=12)
        except:
            self.fonts = {
                'title': ('SF Pro Display', 24, 'bold'),
                'subtitle': ('SF Pro Display', 14, 'normal'), 
                'body': ('SF Pro Display', 13, 'normal'),
                'chat': ('Monaco', 13, 'normal'),
                'button': ('SF Pro Display', 12, 'bold'),
                'small': ('SF Pro Display', 11, 'normal')
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
        
        # Style
        self.setup_style()
        
        # UI aufbauen
        self.setup_ui()
        self.setup_client()
        self.setup_tts_stt()
        
        print("🌙 Starte Elegante Kimi K2 GUI mit Moonshot AI...")
        
    def setup_style(self):
        """Moderne Styles konfigurieren"""
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Custom Style für ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button Styles
        style.configure('Accent.TButton',
                       background=self.colors['accent_purple'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Accent.TButton',
                 background=[('active', '#9333ea')])
                 
        style.configure('Secondary.TButton',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       focuscolor='none',
                       padding=(15, 8))
                       
        # Combobox Style
        style.configure('Dark.TCombobox',
                       fieldbackground=self.colors['bg_tertiary'],
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       relief='solid')
        
    def setup_ui(self):
        """Elegante Benutzeroberfläche im Void AI Chat Stil"""
        
        # Hauptcontainer mit Padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        # Header mit Navigation
        self.create_header(main_container)
        
        # Content Area
        content_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(24, 0))
        
        # Sidebar + Chat Layout
        self.create_sidebar_and_chat(content_frame)
        
    def create_header(self, parent):
        """Header mit Navigation wie Void AI Chat"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Logo/Title Bereich
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_frame.pack(side=tk.LEFT, anchor=tk.W, pady=20)
        
        # Logo Icon (simuliert)
        logo_frame = tk.Frame(title_frame, bg=self.colors['accent_purple'], width=32, height=32)
        logo_frame.pack(side=tk.LEFT, padx=(0, 12))
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(logo_frame, text="🌙", font=('SF Pro Display', 16), 
                             bg=self.colors['accent_purple'], fg='white')
        logo_label.pack(expand=True)
        
        # Title
        title_label = tk.Label(title_frame, text="Kimi K2 Instruct", 
                              font=self.fonts['title'],
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg_primary'])
        title_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Navigation Buttons (rechts)
        nav_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        nav_frame.pack(side=tk.RIGHT, anchor=tk.E, pady=20)
        
        # Status Badge
        self.status_badge = tk.Label(nav_frame, text="● Bereit", 
                                    font=self.fonts['small'],
                                    fg=self.colors['success'],
                                    bg=self.colors['bg_primary'])
        self.status_badge.pack(side=tk.RIGHT, padx=(0, 20))
        
        # Nav Buttons
        nav_buttons = [
            ("Chat Interface", True),
            ("Settings", False),
            ("Tools & Connectors", False)
        ]
        
        for btn_text, active in nav_buttons:
            btn_bg = self.colors['bg_tertiary'] if active else self.colors['bg_primary']
            btn_fg = self.colors['text_primary'] if active else self.colors['text_muted']
            
            nav_btn = tk.Label(nav_frame, text=btn_text,
                              font=self.fonts['button'],
                              fg=btn_fg, bg=btn_bg,
                              padx=16, pady=8,
                              cursor='hand2')
            nav_btn.pack(side=tk.RIGHT, padx=8)
            
            if active:
                # Aktiver Tab Indikator
                indicator = tk.Frame(nav_btn, bg=self.colors['accent_purple'], height=2)
                indicator.place(x=0, y=nav_btn.winfo_reqheight()-2, relwidth=1)
    
    def create_sidebar_and_chat(self, parent):
        """Sidebar und Chat-Bereich erstellen"""
        
        # Hauptlayout: Sidebar + Chat
        layout_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        layout_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar (links)
        self.create_sidebar(layout_frame)
        
        # Chat Area (rechts)
        self.create_chat_area(layout_frame)
    
    def create_sidebar(self, parent):
        """Elegante Sidebar mit Einstellungen"""
        sidebar_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], width=300)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 24))
        sidebar_frame.pack_propagate(False)
        
        # Sidebar Content mit Padding
        sidebar_content = tk.Frame(sidebar_frame, bg=self.colors['bg_secondary'])
        sidebar_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Model Configuration Card
        self.create_config_card(sidebar_content)
        
        # Voice Controls Card
        self.create_voice_card(sidebar_content)
        
        # Connection Status Card
        self.create_status_card(sidebar_content)
        
    def create_config_card(self, parent):
        """Model Configuration Card"""
        card_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'])
        card_frame.pack(fill=tk.X, pady=(0, 16))
        
        # Card Header
        header = tk.Frame(card_frame, bg=self.colors['bg_tertiary'], height=50)
        header.pack(fill=tk.X, padx=16, pady=(16, 0))
        header.pack_propagate(False)
        
        tk.Label(header, text="Model Configuration", 
                font=self.fonts['subtitle'],
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack(anchor=tk.W, pady=12)
        
        # Card Content
        content = tk.Frame(card_frame, bg=self.colors['bg_tertiary'])
        content.pack(fill=tk.X, padx=16, pady=(0, 16))
        
        # Model Selection
        tk.Label(content, text="Model:", 
                font=self.fonts['small'],
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_tertiary']).pack(anchor=tk.W, pady=(0, 4))
        
        self.model_var = tk.StringVar(value="moonshot-v1-128k")
        model_combo = ttk.Combobox(content, textvariable=self.model_var,
                                  values=["moonshot-v1-128k", "moonshot-v1-32k", "moonshot-v1-8k"],
                                  state="readonly", style='Dark.TCombobox',
                                  font=self.fonts['body'])
        model_combo.pack(fill=tk.X, pady=(0, 12))
        
        # Temperature Slider
        tk.Label(content, text="Temperature: 0.6", 
                font=self.fonts['small'],
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_tertiary']).pack(anchor=tk.W, pady=(0, 4))
        
        self.temp_var = tk.DoubleVar(value=0.6)
        temp_frame = tk.Frame(content, bg=self.colors['bg_tertiary'])
        temp_frame.pack(fill=tk.X, pady=(0, 8))
        
        temp_scale = tk.Scale(temp_frame, from_=0.0, to=1.0, resolution=0.1,
                             orient=tk.HORIZONTAL, variable=self.temp_var,
                             bg=self.colors['bg_tertiary'],
                             fg=self.colors['text_primary'],
                             highlightthickness=0,
                             troughcolor=self.colors['bg_primary'],
                             activebackground=self.colors['accent_purple'],
                             font=self.fonts['small'])
        temp_scale.pack(fill=tk.X)
        
    def create_voice_card(self, parent):
        """Voice Controls Card"""
        card_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'])
        card_frame.pack(fill=tk.X, pady=(0, 16))
        
        # Card Header
        header = tk.Frame(card_frame, bg=self.colors['bg_tertiary'], height=50)
        header.pack(fill=tk.X, padx=16, pady=(16, 0))
        header.pack_propagate(False)
        
        tk.Label(header, text="Voice Controls", 
                font=self.fonts['subtitle'],
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack(anchor=tk.W, pady=12)
        
        # Card Content
        content = tk.Frame(card_frame, bg=self.colors['bg_tertiary'])
        content.pack(fill=tk.X, padx=16, pady=(0, 16))
        
        # TTS Button
        self.tts_btn = self.create_modern_button(
            content, 
            "🔊 Text-to-Speech" if TTS_AVAILABLE else "🔊 TTS (Install Required)",
            self.toggle_tts,
            style='success' if TTS_AVAILABLE else 'warning'
        )
        self.tts_btn.pack(fill=tk.X, pady=(0, 8))
        
        # STT Button
        self.stt_btn = self.create_modern_button(
            content,
            "🎤 Speech-to-Text" if STT_AVAILABLE else "🎤 STT (Install Required)", 
            self.toggle_recording,
            style='accent' if STT_AVAILABLE else 'warning'
        )
        self.stt_btn.pack(fill=tk.X)
        
    def create_status_card(self, parent):
        """Connection Status Card"""
        card_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'])
        card_frame.pack(fill=tk.X, pady=(0, 16))
        
        # Card Header
        header = tk.Frame(card_frame, bg=self.colors['bg_tertiary'], height=50)
        header.pack(fill=tk.X, padx=16, pady=(16, 0))
        header.pack_propagate(False)
        
        tk.Label(header, text="Connection Status", 
                font=self.fonts['subtitle'],
                fg=self.colors['text_primary'],
                bg=self.colors['bg_tertiary']).pack(anchor=tk.W, pady=12)
        
        # Card Content
        content = tk.Frame(card_frame, bg=self.colors['bg_tertiary'])
        content.pack(fill=tk.X, padx=16, pady=(0, 16))
        
        # API Status
        self.api_status_label = tk.Label(content, text="API: Connecting...",
                                        font=self.fonts['small'],
                                        fg=self.colors['text_secondary'],
                                        bg=self.colors['bg_tertiary'])
        self.api_status_label.pack(anchor=tk.W, pady=(0, 4))
        
        # Model Info
        self.model_info_label = tk.Label(content, text="Model: Loading...",
                                        font=self.fonts['small'],
                                        fg=self.colors['text_secondary'],
                                        bg=self.colors['bg_tertiary'])
        self.model_info_label.pack(anchor=tk.W, pady=(0, 4))
        
        # Provider Info  
        self.provider_label = tk.Label(content, text="Provider: Moonshot AI",
                                      font=self.fonts['small'],
                                      fg=self.colors['text_secondary'],
                                      bg=self.colors['bg_tertiary'])
        self.provider_label.pack(anchor=tk.W)
        
    def create_chat_area(self, parent):
        """Hauptchat-Bereich im Void AI Chat Stil"""
        chat_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        chat_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat Header
        chat_header = tk.Frame(chat_container, bg=self.colors['bg_chat'], height=60)
        chat_header.pack(fill=tk.X, pady=(0, 16))
        chat_header.pack_propagate(False)
        
        header_content = tk.Frame(chat_header, bg=self.colors['bg_chat'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)
        
        chat_title = tk.Label(header_content, text="Chat Interface",
                             font=self.fonts['title'],
                             fg=self.colors['text_primary'],
                             bg=self.colors['bg_chat'])
        chat_title.pack(side=tk.LEFT)
        
        # Clear Button (rechts)
        clear_btn = self.create_modern_button(
            header_content, "🗑️ Clear", self.clear_chat, style='secondary'
        )
        clear_btn.pack(side=tk.RIGHT)
        
        # Chat Messages Area
        self.create_chat_messages(chat_container)
        
        # Input Area
        self.create_input_area(chat_container)
        
    def create_chat_messages(self, parent):
        """Chat Messages Display"""
        messages_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        messages_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 16))
        
        # Scrollable Chat Area
        self.chat_text = scrolledtext.ScrolledText(
            messages_frame,
            wrap=tk.WORD,
            font=self.fonts['chat'],
            bg=self.colors['bg_chat'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_purple'],
            selectbackground=self.colors['accent_purple'],
            selectforeground='white',
            borderwidth=0,
            highlightthickness=0,
            state=tk.DISABLED,
            padx=20,
            pady=20
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True)
        
        # Willkommens-Nachricht
        self.add_welcome_message()
        
    def create_input_area(self, parent):
        """Input Area mit modernem Design"""
        input_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        input_container.pack(fill=tk.X)
        
        # Input Card
        input_card = tk.Frame(input_container, bg=self.colors['bg_chat'])
        input_card.pack(fill=tk.X, pady=(0, 8))
        
        # Input Content
        input_content = tk.Frame(input_card, bg=self.colors['bg_chat'])
        input_content.pack(fill=tk.X, padx=20, pady=16)
        
        # Text Input
        self.input_text = tk.Text(
            input_content,
            height=3,
            font=self.fonts['body'],
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_purple'],
            selectbackground=self.colors['accent_purple'],
            borderwidth=0,
            highlightthickness=1,
            highlightcolor=self.colors['accent_purple'],
            wrap=tk.WORD,
            padx=16,
            pady=12
        )
        self.input_text.pack(fill=tk.X, pady=(0, 12))
        
        # Placeholder Text
        self.input_text.insert("1.0", "Type your message here...")
        self.input_text.bind("<FocusIn>", self.clear_placeholder)
        self.input_text.bind("<FocusOut>", self.add_placeholder)
        
        # Key Bindings
        self.input_text.bind('<Return>', lambda e: self.send_message() or "break")
        self.input_text.bind('<Shift-Return>', lambda e: None)
        
        # Button Area
        button_area = tk.Frame(input_content, bg=self.colors['bg_chat'])
        button_area.pack(fill=tk.X)
        
        # Send Button
        send_btn = self.create_modern_button(
            button_area, "Send Message", self.send_message, style='accent'
        )
        send_btn.pack(side=tk.RIGHT)
        
        # Input Info
        info_label = tk.Label(button_area, 
                             text="Press Enter to send • Shift+Enter for new line",
                             font=self.fonts['small'],
                             fg=self.colors['text_muted'],
                             bg=self.colors['bg_chat'])
        info_label.pack(side=tk.LEFT, anchor=tk.W)
        
    def create_modern_button(self, parent, text, command, style='primary'):
        """Moderne Button-Komponente"""
        colors = {
            'primary': (self.colors['accent_blue'], 'white'),
            'accent': (self.colors['accent_purple'], 'white'),
            'success': (self.colors['success'], 'white'),
            'warning': (self.colors['warning'], 'white'),
            'secondary': (self.colors['bg_tertiary'], self.colors['text_primary']),
            'error': (self.colors['error'], 'white')
        }
        
        bg_color, fg_color = colors.get(style, colors['primary'])
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=self.fonts['button'],
            borderwidth=0,
            relief=tk.FLAT,
            padx=16,
            pady=8,
            cursor='hand2'
        )
        
        # Hover-Effekt
        def on_enter(e):
            btn.configure(bg=self.lighten_color(bg_color))
        def on_leave(e):
            btn.configure(bg=bg_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
        
    def lighten_color(self, color):
        """Farbe aufhellen für Hover-Effekt"""
        if color == self.colors['accent_purple']:
            return '#9333ea'
        elif color == self.colors['accent_blue']:
            return '#2563eb'
        elif color == self.colors['success']:
            return '#059669'
        elif color == self.colors['bg_tertiary']:
            return '#374151'
        return color
        
    def clear_placeholder(self, event):
        """Placeholder Text entfernen"""
        if self.input_text.get("1.0", tk.END).strip() == "Type your message here...":
            self.input_text.delete("1.0", tk.END)
            self.input_text.configure(fg=self.colors['text_primary'])
            
    def add_placeholder(self, event):
        """Placeholder Text hinzufügen"""
        if not self.input_text.get("1.0", tk.END).strip():
            self.input_text.insert("1.0", "Type your message here...")
            self.input_text.configure(fg=self.colors['text_muted'])
    
    def add_welcome_message(self):
        """Willkommens-Nachricht im Chat"""
        welcome_text = """🌙 Welcome to Kimi K2 Instruct

Powered by Moonshot AI
• 1 Trillion Parameters (32B activated)  
• 128K Token Context
• Native Tool Calling
• Advanced Reasoning

Start chatting to experience the power of Kimi K2!"""
        
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, welcome_text + "\n\n")
        self.chat_text.config(state=tk.DISABLED)
        
    def setup_client(self):
        """Moonshot AI Client initialisieren"""
        try:
            self.client = KimiMoonshotClient()
            self.update_api_status("✅ Connected", self.colors['success'])
            self.model_info_label.configure(text=f"Model: {self.client.model}")
            self.status_badge.configure(text="● Ready", fg=self.colors['success'])
        except Exception as e:
            self.update_api_status("❌ Connection Failed", self.colors['error'])
            self.add_chat_message("system", f"❌ Setup Required: {str(e)}\n\n💡 Please configure MOONSHOT_API_KEY in .env file\nRegistration: https://platform.moonshot.ai")
            
    def setup_tts_stt(self):
        """TTS und STT initialisieren"""
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    for voice in voices:
                        if 'german' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                self.tts_engine.setProperty('rate', 180)
                self.tts_engine.setProperty('volume', 0.8)
            except Exception as e:
                print(f"TTS Error: {e}")
                
        if STT_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
            except Exception as e:
                print(f"STT Error: {e}")
    
    def send_message(self):
        """Nachricht senden"""
        if not self.client:
            self.add_chat_message("error", "❌ No Moonshot AI client available")
            return
            
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input or user_input == "Type your message here...":
            return
            
        # Input clearen
        self.input_text.delete("1.0", tk.END)
        self.add_placeholder(None)
        
        # User Message hinzufügen
        self.add_chat_message("user", user_input)
        
        # In Thread senden
        self.current_conversation.append({"role": "user", "content": user_input})
        threading.Thread(target=self._send_message_thread, args=(user_input,), daemon=True).start()
        self.update_status("🌙 Kimi is thinking...")
        
    def _send_message_thread(self, user_input):
        """Nachricht in separatem Thread senden"""
        try:
            self.client.model = self.model_var.get()
            self.client.temperature = self.temp_var.get()
            
            response_content = ""
            
            for chunk in self.client.chat_stream(self.current_conversation):
                if chunk:
                    response_content += chunk
                    
            self.root.after(0, lambda: self.add_chat_message("assistant", response_content))
            self.current_conversation.append({"role": "assistant", "content": response_content})
            
            if self.tts_enabled and self.tts_engine and response_content:
                threading.Thread(target=self._speak_text, args=(response_content,), daemon=True).start()
                
            self.root.after(0, lambda: self.update_status("● Ready"))
            
        except Exception as e:
            self.root.after(0, lambda: self.add_chat_message("error", f"❌ Error: {str(e)}"))
            self.root.after(0, lambda: self.update_status("● Error"))
    
    def add_chat_message(self, role, content):
        """Nachricht zum Chat hinzufügen"""
        self.chat_text.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if role == "user":
            self.chat_text.insert(tk.END, f"You [{timestamp}]\n", "user_header")
            self.chat_text.insert(tk.END, f"{content}\n\n")
        elif role == "assistant":
            self.chat_text.insert(tk.END, f"🌙 Kimi [{timestamp}]\n", "assistant_header")
            self.chat_text.insert(tk.END, f"{content}\n\n")
        elif role == "system":
            self.chat_text.insert(tk.END, f"System\n", "system_header")
            self.chat_text.insert(tk.END, f"{content}\n\n")
        elif role == "error":
            self.chat_text.insert(tk.END, f"Error\n", "error_header")
            self.chat_text.insert(tk.END, f"{content}\n\n")
            
        # Tag-Styles
        self.chat_text.tag_configure("user_header", foreground=self.colors['accent_blue'], font=self.fonts['button'])
        self.chat_text.tag_configure("assistant_header", foreground=self.colors['accent_purple'], font=self.fonts['button'])
        self.chat_text.tag_configure("system_header", foreground=self.colors['text_muted'], font=self.fonts['button'])
        self.chat_text.tag_configure("error_header", foreground=self.colors['error'], font=self.fonts['button'])
        
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
        
    def toggle_tts(self):
        """TTS ein-/ausschalten"""
        if not TTS_AVAILABLE:
            self.add_chat_message("error", "❌ Text-to-Speech not available! Install: pip3 install pyttsx3")
            return
            
        self.tts_enabled = not self.tts_enabled
        status = "ON" if self.tts_enabled else "OFF"
        self.tts_btn.configure(text=f"🔊 TTS ({status})")
        
    def toggle_recording(self):
        """Sprachaufnahme starten/stoppen"""
        if not STT_AVAILABLE:
            self.add_chat_message("error", "❌ Speech-to-Text not available! Install: pip3 install speechrecognition pyaudio")
            return
            
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Sprachaufnahme starten"""
        self.is_recording = True
        self.stt_btn.configure(text="⏹️ Stop Recording")
        threading.Thread(target=self._record_audio, daemon=True).start()
        
    def stop_recording(self):
        """Sprachaufnahme stoppen"""
        self.is_recording = False
        self.stt_btn.configure(text="🎤 Speech-to-Text")
        
    def _record_audio(self):
        """Audio aufnehmen und in Text umwandeln"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
            
            text = self.recognizer.recognize_google(audio, language='de-DE')
            self.root.after(0, lambda: self.input_text.insert(tk.END, text))
            self.root.after(0, self.stop_recording)
            
        except Exception as e:
            self.root.after(0, lambda: self.add_chat_message("error", f"❌ STT Error: {str(e)}"))
            self.root.after(0, self.stop_recording)
            
    def _speak_text(self, text):
        """Text vorlesen"""
        try:
            if len(text) > 500:
                text = text[:500] + "..."
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
            
    def clear_chat(self):
        """Chat löschen"""
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete("1.0", tk.END)
        self.chat_text.config(state=tk.DISABLED)
        
        self.current_conversation = []
        if self.client:
            self.client.clear_conversation()
            
        self.add_welcome_message()
        
    def update_api_status(self, text, color):
        """API Status aktualisieren"""
        self.api_status_label.configure(text=f"API: {text}", fg=color)
        
    def update_status(self, text):
        """Status Badge aktualisieren"""
        self.status_badge.configure(text=text)
        
    def run(self):
        """GUI starten"""
        self.root.mainloop()

def main():
    """Hauptfunktion"""
    
    # API-Key Check
    api_key = os.getenv("MOONSHOT_API_KEY", "")
    if not api_key or api_key == "sk-demo_key_please_replace":
        print("⚠️  Demo-API-Key detected. Please configure real API key in .env file:")
        print("   MOONSHOT_API_KEY=sk-your_actual_api_key_here")
        print("   Registration: https://platform.moonshot.ai")
        print()
    
    # GUI starten
    app = ElegantKimiMoonshotGUI()
    app.run()

if __name__ == "__main__":
    main() 