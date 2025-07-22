#!/bin/bash

# Kimi K2 Instruct - One-Click-Starter
# Moderne, interaktive Auswahl zwischen CLI, Standard-GUI und moderner GUI

cd "$(dirname "$0")"

# Farben für bessere Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}🤖 ============================================${NC}"
echo -e "${PURPLE}   Kimi K2 Instruct - One-Click-Starter${NC}"
echo -e "${PURPLE}   State-of-the-Art MoE mit 1T Parametern${NC}"
echo -e "${PURPLE}============================================${NC}"
echo

# Dependencies prüfen
echo -e "${BLUE}🔧 Prüfe Dependencies...${NC}"
python3 -c "import together, dotenv, pydantic" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Installiere fehlende Dependencies...${NC}"
    pip3 install together python-dotenv pydantic --quiet
    echo -e "${GREEN}✅ Dependencies installiert${NC}"
fi

# TTS/STT Dependencies prüfen (optional)
python3 -c "import pyttsx3, speech_recognition" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  TTS/STT nicht verfügbar (optional)${NC}"
    echo -e "${CYAN}💡 Für Spracheingabe/-ausgabe: pip3 install pyttsx3 speechrecognition pyaudio${NC}"
fi

# API-Key Status prüfen
echo -e "${BLUE}🔑 Prüfe API-Konfiguration...${NC}"
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('TOGETHER_API_KEY', '')
if not api_key or api_key in ['demo_key_please_replace', 'your_api_key_here']:
    print('❌ Demo-API-Key erkannt - Setup erforderlich!')
    print('📋 Anleitung:')
    print('   1. Gehen Sie zu: https://api.together.xyz/settings/api-keys')
    print('   2. Registrieren Sie sich kostenlos')
    print('   3. Erstellen Sie einen API-Key')
    print('   4. Bearbeiten Sie .env: TOGETHER_API_KEY=your_actual_key')
    print()
else:
    print('✅ API-Key konfiguriert')
"

echo

# Interaktive Auswahl
echo -e "${CYAN}🚀 Wählen Sie Ihren bevorzugten Kimi K2 Client:${NC}"
echo
echo -e "${GREEN}1)${NC} 💻 CLI Chat (Terminal-basiert)"
echo -e "${GREEN}2)${NC} 🖥️  Standard GUI (einfache Oberfläche)"
echo -e "${GREEN}3)${NC} 🎨 Moderne GUI (große Schrift, Enter=Senden, Mikrofon)"
echo -e "${GREEN}4)${NC} 🧪 API-Verbindung testen"
echo -e "${GREEN}5)${NC} 📊 API Info anzeigen"
echo -e "${GREEN}q)${NC} ❌ Beenden"
echo

read -p "Ihre Wahl [1-5/q]: " choice

case $choice in
    1)
        echo -e "${BLUE}🚀 Starte CLI Chat...${NC}"
        python3 kimi_chat.py
        ;;
    2)
        echo -e "${BLUE}🚀 Starte Standard GUI...${NC}"
        python3 kimi_gui.py
        ;;
    3)
        echo -e "${BLUE}🚀 Starte Moderne GUI...${NC}"
        python3 kimi_gui_modern.py
        ;;
    4)
        echo -e "${BLUE}🧪 API-Verbindung testen:${NC}"
        python3 test_simple.py
        ;;
    5)
        echo -e "${BLUE}📊 API Information:${NC}"
        python3 api_info.py
        ;;
    q|Q)
        echo -e "${YELLOW}👋 Auf Wiedersehen!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Ungültige Auswahl. Bitte 1-5 oder q wählen.${NC}"
        exit 1
        ;;
esac

echo
echo -e "${PURPLE}🎯 Kimi K2 Instruct Features:${NC}"
echo -e "${CYAN}• 1 Trillion Parameter (32B aktiviert)${NC}"
echo -e "${CYAN}• 128K Token Kontext${NC}"
echo -e "${CYAN}• Spezialisiert auf Coding & Reasoning${NC}"
echo -e "${CYAN}• Tool Use & Function Calling${NC}"
echo -e "${CYAN}• Angetrieben von Together AI${NC}" 