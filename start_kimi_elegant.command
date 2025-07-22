#!/bin/bash

# Kimi K2 Instruct - Elegant GUI Starter
# Moonshot AI powered with Void AI Chat inspired design

# Farben für elegante Ausgabe
PURPLE='\033[0;35m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'
CYAN='\033[0;36m'

# Script Directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Banner
clear
echo -e "${PURPLE}${BOLD}"
echo "🌙 ═══════════════════════════════════════════════════════════════"
echo "   Kimi K2 Instruct - Elegant GUI (Void AI Chat Style)"
echo "   Powered by Moonshot AI"
echo "═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Funktion für gestylte Menüs
print_menu_item() {
    local number=$1
    local icon=$2
    local text=$3
    local description=$4
    
    echo -e "${BLUE}${BOLD}${number})${NC} ${icon} ${BOLD}${text}${NC}"
    echo -e "   ${description}"
    echo ""
}

# API-Key Check
check_api_key() {
    if [ -f ".env" ]; then
        if grep -q "sk-demo_key_please_replace" .env || ! grep -q "MOONSHOT_API_KEY=" .env; then
            echo -e "${YELLOW}⚠️  Setup Required:${NC}"
            echo "   Please configure your Moonshot AI API key in .env file"
            echo "   Registration: https://api.moonshot.ai/settings/api-keys"
            echo ""
        else
            echo -e "${GREEN}✅ API Configuration: Ready${NC}"
            echo ""
        fi
    else
        echo -e "${RED}❌ .env file not found${NC}"
        echo ""
    fi
}

# Dependencies check
check_dependencies() {
    echo -e "${BLUE}🔍 Checking Dependencies...${NC}"
    
    # Python Check
    if command -v python3 &> /dev/null; then
        echo -e "   ✅ Python 3: $(python3 --version)"
    else
        echo -e "   ❌ Python 3: Not found"
        return 1
    fi
    
    # Package Checks
    local packages=("together" "python-dotenv" "pydantic")
    local optional=("pyttsx3" "speechrecognition" "pyaudio")
    
    for pkg in "${packages[@]}"; do
        if python3 -c "import $pkg" 2>/dev/null; then
            echo -e "   ✅ $pkg: Installed"
        else
            echo -e "   ❌ $pkg: Missing"
            echo -e "      Install with: ${YELLOW}pip3 install $pkg${NC}"
            return 1
        fi
    done
    
    for pkg in "${optional[@]}"; do
        if python3 -c "import $pkg" 2>/dev/null; then
            echo -e "   ✅ $pkg: Installed (Voice features enabled)"
        else
            echo -e "   ⚠️  $pkg: Optional (Voice features disabled)"
        fi
    done
    
    echo ""
    return 0
}

# Hauptmenü
show_menu() {
    echo -e "${PURPLE}${BOLD}🎨 Choose Your Interface:${NC}"
    echo ""
    
    echo -e "   ${CYAN}1) �� Start Elegant Kimi GUI (Moonshot AI)${NC}"
    echo -e "   ${CYAN}2) 💬 Start Kimi CLI Chat (Moonshot AI)${NC}"
    echo -e "   ${CYAN}3) 🧪 Test Moonshot AI Connection${NC}"
    echo -e "   ${CYAN}4) ⚙️ Show Configuration${NC}"
    echo -e "   ${CYAN}5) 📦 Install/Update Dependencies${NC}"
    
    echo -e "${BLUE}${BOLD}q)${NC} 🚪 ${BOLD}Exit${NC}"
    echo ""
    echo -e "${PURPLE}══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Dependency Installation
install_dependencies() {
    echo -e "${YELLOW}📦 Installing Dependencies...${NC}"
    echo ""
    
    # Required packages
    echo -e "${BLUE}Installing required packages:${NC}"
    pip3 install together python-dotenv pydantic
    
    echo ""
    echo -e "${BLUE}Installing optional voice packages:${NC}"
    echo -e "${YELLOW}Note: This may require additional system dependencies${NC}"
    
    # Voice packages (may fail on some systems)
    pip3 install pyttsx3 speechrecognition pyaudio || {
        echo -e "${YELLOW}⚠️  Some voice packages failed to install${NC}"
        echo "   Voice features may not be available"
        echo "   This is normal on some systems"
    }
    
    echo ""
    echo -e "${GREEN}✅ Installation completed${NC}"
    echo ""
}

# Haupt-Loop
main_loop() {
    while true; do
        check_api_key
        check_dependencies || {
            echo -e "${RED}❌ Missing dependencies detected${NC}"
            echo ""
        }
        
        show_menu
        
        echo -ne "${BLUE}Your choice [1-5/q]: ${NC}"
        read choice
        
        case $choice in
            1)
                echo -e "${GREEN}🚀 Starting Elegant Kimi GUI...${NC}"
                python3 kimi_gui_moonshot_elegant.py
                ;;
            2)
                echo -e "${GREEN}💬 Starting Kimi CLI Chat...${NC}"
                python3 kimi_chat.py
                ;;
            3)
                echo -e "${GREEN}🧪 Testing Moonshot AI Connection...${NC}"
                python3 test_moonshot.py
                ;;
            4)
                echo -e "${BLUE}⚙️ Configuration Information:${NC}"
                echo ""
                python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

print('🌙 Moonshot AI Configuration:')
print(f'   API Key: {\"✅ Configured\" if os.getenv(\"MOONSHOT_API_KEY\", \"\") and os.getenv(\"MOONSHOT_API_KEY\") != \"sk-demo_key_please_replace\" else \"❌ Not configured\"}')
print(f'   Model: {os.getenv(\"KIMI_MODEL\", \"moonshot-v1-128k\")}')
print(f'   Temperature: {os.getenv(\"TEMPERATURE\", \"0.6\")}')
print(f'   Max Tokens: {os.getenv(\"MAX_TOKENS\", \"4096\")}')
print()
print('🎙️ Voice Configuration:')
print(f'   TTS Enabled: {os.getenv(\"TTS_ENABLED\", \"true\")}')
print(f'   STT Enabled: {os.getenv(\"STT_ENABLED\", \"true\")}')
print(f'   Voice Rate: {os.getenv(\"VOICE_RATE\", \"180\")}')
print(f'   Voice Volume: {os.getenv(\"VOICE_VOLUME\", \"0.8\")}')
"
                echo ""
                ;;
            5)
                install_dependencies
                ;;
            q|Q)
                echo -e "${PURPLE}👋 Goodbye! Thanks for using Kimi K2 Instruct${NC}"
                echo ""
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Invalid choice. Please select 1-5 or q${NC}"
                echo ""
                ;;
        esac
        
        if [ "$choice" != "4" ] && [ "$choice" != "5" ]; then
            echo ""
            echo -e "${BLUE}Press Enter to return to menu...${NC}"
            read
            clear
        fi
    done
}

# Feature Highlights
echo -e "${GREEN}✨ Features:${NC}"
echo "   • Elegant Void AI Chat inspired design"
echo "   • Dark theme with modern typography"
echo "   • Real-time streaming responses"
echo "   • Voice input/output support"
echo "   • 128K context window"
echo "   • Native tool calling"
echo ""

# Start
main_loop 