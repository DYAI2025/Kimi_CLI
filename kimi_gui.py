#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kimi K2 Instruct - GUI Client
Moderne grafische Benutzeroberfläche für Kimi K2 Instruct
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
import os
from datetime import datetime
from kimi_client import KimiClient
from dotenv import load_dotenv

load_dotenv()

class KimiGUI:
    def __init__(self, root):
        self.root = root
        self.kimi = None
        self.setup_ui()
        self.setup_client()
        
    def setup_ui(self):
        """Initialisiert die Benutzeroberfläche"""
        self.root.title("Kimi K2 Instruct - GUI Client")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Titel
        title_label = ttk.Label(main_frame, text="🤖 Kimi K2 Instruct", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Konfiguration Frame
        config_frame = ttk.LabelFrame(main_frame, text="Konfiguration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Modell-Auswahl
        ttk.Label(config_frame, text="Modell:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.model_var = tk.StringVar(value="moonshotai/Kimi-K2-Instruct")
        model_combo = ttk.Combobox(config_frame, textvariable=self.model_var, 
                                  values=["moonshotai/Kimi-K2-Instruct", "moonshotai/Kimi-K2-Base"],
                                  state="readonly", width=30)
        model_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        # Temperature
        ttk.Label(config_frame, text="Temperature:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.temp_var = tk.DoubleVar(value=0.6)
        temp_scale = ttk.Scale(config_frame, from_=0.0, to=1.0, variable=self.temp_var, 
                              orient=tk.HORIZONTAL, length=100)
        temp_scale.grid(row=0, column=3, sticky=tk.W, padx=(0, 5))
        self.temp_label = ttk.Label(config_frame, text="0.6")
        self.temp_label.grid(row=0, column=4, sticky=tk.W)
        temp_scale.configure(command=self.update_temp_label)
        
        # Max Tokens
        ttk.Label(config_frame, text="Max Tokens:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.max_tokens_var = tk.IntVar(value=4096)
        max_tokens_entry = ttk.Entry(config_frame, textvariable=self.max_tokens_var, width=10)
        max_tokens_entry.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Streaming
        self.streaming_var = tk.BooleanVar(value=True)
        streaming_check = ttk.Checkbutton(config_frame, text="Streaming", variable=self.streaming_var)
        streaming_check.grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        
        # System Prompt
        system_frame = ttk.LabelFrame(main_frame, text="System Prompt", padding="10")
        system_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        main_frame.columnconfigure(0, weight=1)
        
        self.system_prompt_var = tk.StringVar(value="You are Kimi, an AI assistant created by Moonshot AI.")
        system_entry = ttk.Entry(system_frame, textvariable=self.system_prompt_var, width=80)
        system_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        system_frame.columnconfigure(0, weight=1)
        
        ttk.Button(system_frame, text="Reset", command=self.reset_system_prompt).grid(row=0, column=1)
        
        # Chat Bereich
        chat_frame = ttk.LabelFrame(main_frame, text="Chat", padding="10")
        chat_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(3, weight=1)
        
        # Chat Display
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=80, height=20,
                                                     font=('Consolas', 10))
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        # Input Bereich
        input_frame = ttk.Frame(chat_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.input_text = tk.Text(input_frame, height=3, wrap=tk.WORD, font=('Arial', 10))
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.send_button = ttk.Button(button_frame, text="Senden", command=self.send_message)
        self.send_button.grid(row=0, column=0, pady=(0, 5))
        
        ttk.Button(button_frame, text="Löschen", command=self.clear_chat).grid(row=1, column=0, pady=(0, 5))
        ttk.Button(button_frame, text="Speichern", command=self.save_chat).grid(row=2, column=0, pady=(0, 5))
        ttk.Button(button_frame, text="Laden", command=self.load_chat).grid(row=3, column=0)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Bereit")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Keyboard Bindings
        self.input_text.bind('<Control-Return>', lambda e: self.send_message())
        self.root.bind('<F1>', lambda e: self.show_help())
        
    def setup_client(self):
        """Initialisiert den Kimi Client"""
        try:
            self.kimi = KimiClient()
            self.status_var.set("✅ Kimi K2 Client bereit")
            self.add_to_chat("System", "Kimi K2 Instruct Client initialisiert!", "system")
        except Exception as e:
            self.status_var.set(f"❌ Fehler: {e}")
            self.add_to_chat("Fehler", f"Kimi Client konnte nicht initialisiert werden: {e}", "error")
            messagebox.showerror("Initialisierungsfehler", 
                               f"Fehler beim Laden des Kimi Clients:\n\n{e}\n\n"
                               "Stellen Sie sicher, dass MOONSHOT_API_KEY in der .env-Datei gesetzt ist.")
    
    def update_temp_label(self, value):
        """Aktualisiert das Temperature Label"""
        self.temp_label.config(text=f"{float(value):.1f}")
    
    def reset_system_prompt(self):
        """Setzt den System Prompt zurück"""
        self.system_prompt_var.set("You are Kimi, an AI assistant created by Moonshot AI.")
    
    def add_to_chat(self, sender, message, msg_type="user"):
        """Fügt eine Nachricht zum Chat hinzu"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Farben je nach Typ
        colors = {
            "user": "#2563eb",      # Blau
            "assistant": "#059669", # Grün  
            "system": "#7c3aed",    # Lila
            "error": "#dc2626"      # Rot
        }
        
        self.chat_display.configure(state=tk.NORMAL)
        
        # Sender und Timestamp
        self.chat_display.insert(tk.END, f"\n[{timestamp}] {sender}:\n", f"sender_{msg_type}")
        self.chat_display.insert(tk.END, f"{message}\n", f"message_{msg_type}")
        
        # Text-Tags für Farben
        self.chat_display.tag_config(f"sender_{msg_type}", foreground=colors.get(msg_type, "#000000"), 
                                    font=('Arial', 10, 'bold'))
        self.chat_display.tag_config(f"message_{msg_type}", foreground="#000000", font=('Arial', 10))
        
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self):
        """Sendet eine Nachricht an Kimi"""
        if not self.kimi:
            messagebox.showerror("Fehler", "Kimi Client nicht verfügbar!")
            return
            
        message = self.input_text.get("1.0", tk.END).strip()
        if not message:
            return
            
        # Benutzer-Nachricht anzeigen
        self.add_to_chat("Sie", message, "user")
        self.input_text.delete("1.0", tk.END)
        
        # Senden-Button deaktivieren
        self.send_button.configure(state="disabled")
        self.status_var.set("🤖 Kimi denkt...")
        
        # In separatem Thread ausführen
        thread = threading.Thread(target=self.get_response, args=(message,))
        thread.daemon = True
        thread.start()
    
    def get_response(self, message):
        """Holt die Antwort von Kimi (in separatem Thread)"""
        try:
            # Client-Parameter aktualisieren
            self.kimi.model = self.model_var.get()
            self.kimi.temperature = self.temp_var.get()
            self.kimi.max_tokens = self.max_tokens_var.get()
            
            system_prompt = self.system_prompt_var.get()
            
            if self.streaming_var.get():
                # Streaming-Modus
                self.root.after(0, lambda: self.add_to_chat("Kimi", "", "assistant"))
                
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": message})
                
                full_response = ""
                for chunk in self.kimi.chat_stream(messages):
                    full_response += chunk
                    self.root.after(0, lambda c=chunk: self.append_to_last_message(c))
                
            else:
                # Normaler Modus
                response = self.kimi.conversation_chat(message, system_prompt)
                self.root.after(0, lambda: self.add_to_chat("Kimi", response, "assistant"))
                
        except Exception as e:
            self.root.after(0, lambda: self.add_to_chat("Fehler", f"Fehler beim Senden: {e}", "error"))
        finally:
            self.root.after(0, self.enable_send_button)
    
    def append_to_last_message(self, chunk):
        """Fügt Text zur letzten Nachricht hinzu (für Streaming)"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, chunk)
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def enable_send_button(self):
        """Aktiviert den Senden-Button wieder"""
        self.send_button.configure(state="normal")
        self.status_var.set("✅ Bereit")
    
    def clear_chat(self):
        """Löscht den Chat"""
        if messagebox.askyesno("Chat löschen", "Möchten Sie den Chat wirklich löschen?"):
            self.chat_display.configure(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.configure(state=tk.DISABLED)
            if self.kimi:
                self.kimi.clear_history()
            self.add_to_chat("System", "Chat gelöscht", "system")
    
    def save_chat(self):
        """Speichert den Chat in eine Datei"""
        try:
            filename = filedialog.asksaveasfilename(
                title="Chat speichern",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    content = self.chat_display.get("1.0", tk.END)
                    f.write(content)
                self.status_var.set(f"Chat gespeichert: {filename}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Chat konnte nicht gespeichert werden: {e}")
    
    def load_chat(self):
        """Lädt einen Chat aus einer Datei"""
        try:
            filename = filedialog.askopenfilename(
                title="Chat laden",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.chat_display.configure(state=tk.NORMAL)
                self.chat_display.delete("1.0", tk.END)
                self.chat_display.insert("1.0", content)
                self.chat_display.configure(state=tk.DISABLED)
                self.status_var.set(f"Chat geladen: {filename}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Chat konnte nicht geladen werden: {e}")
    
    def show_help(self):
        """Zeigt die Hilfe an"""
        help_text = """
Kimi K2 Instruct - GUI Client Hilfe

Tastenkürzel:
• Ctrl+Enter: Nachricht senden
• F1: Diese Hilfe anzeigen

Konfiguration:
• Modell: Wählen Sie zwischen Kimi-K2-Instruct und Kimi-K2-Base
• Temperature: Steuert die Kreativität (0.0 = deterministisch, 1.0 = sehr kreativ)
• Max Tokens: Maximale Länge der Antwort
• Streaming: Live-Ausgabe der Antwort

System Prompt:
• Bestimmt das Verhalten von Kimi
• Standard: "You are Kimi, an AI assistant created by Moonshot AI."

Chat-Funktionen:
• Senden: Sendet Ihre Nachricht an Kimi
• Löschen: Löscht den gesamten Chat-Verlauf
• Speichern: Speichert den Chat in eine Textdatei
• Laden: Lädt einen gespeicherten Chat

Über Kimi K2 Instruct:
• 1 Trillion Parameter (32B aktiviert)
• 128K Token Kontext
• Spezialisiert auf Coding, Reasoning und Tool Use
• Angetrieben von Together AI
        """
        messagebox.showinfo("Hilfe", help_text)

def main():
    """Hauptfunktion"""
    root = tk.Tk()
    app = KimiGUI(root)
    
    # Theme setzen (falls verfügbar)
    try:
        style = ttk.Style()
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    main() 