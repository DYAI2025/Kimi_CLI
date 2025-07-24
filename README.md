HEAD
# Kimi_CLI
=======
# 🤖 Kimi K2 Instruct Client

Vollständiger Client für **Kimi K2 Instruct** - das State-of-the-Art MoE Modell mit 1 Trillion Parametern (32B aktiviert).

## ✨ Features

- **🎯 Echtes Kimi K2 Instruct Modell** über Together AI
- **💻 CLI Chat** - Interaktive Kommandozeilen-Oberfläche
- **🖥️ GUI Chat** - Moderne grafische Benutzeroberfläche
- **⚡ Streaming Support** - Live-Antworten
- **🛠️ Tool Calling** - Function Calling Unterstützung
- **📋 128K Kontext** - Verarbeitung umfangreicher Dokumente
- **🎛️ Vollständige Kontrolle** - Temperature, Max Tokens, System Prompts

## 🚀 Quick Start

### 1. API-Key einrichten

1. **Erstellen Sie einen API-Key bei Together AI:**
   ```
   https://api.together.xyz/settings/api-keys
   ```

2. **Setzen Sie den API-Key in der `.env`-Datei:**
   ```bash
   TOGETHER_API_KEY=your_api_key_here
   ```

### 2. Starten

**One-Click-Start (empfohlen):**
```bash
./start_kimi.command
```

**Oder manuell:**
```bash
# CLI Chat (Terminal-basiert)
python3 kimi_chat.py

# Standard GUI (einfache Oberfläche)
python3 kimi_gui.py

# 🎨 Moderne GUI (mit TTS/STT, große Schrift)
python3 kimi_gui_modern.py

# API-Information anzeigen
python3 api_info.py

# Client-Test ausführen
python3 kimi_client.py
```

## 📋 Verwendung

### CLI Chat

```
🤖 Willkommen bei Kimi K2 Instruct!

> Hallo Kimi! Kannst du mir beim Programmieren helfen?
```

**Verfügbare Kommandos:**
- `model [name]` - Modell wechseln
- `temp [0.0-1.0]` - Temperature setzen
- `tokens [anzahl]` - Max Tokens setzen
- `stream` - Streaming ein/aus
- `system [prompt]` - System Prompt setzen
- `clear` - Chat-Verlauf löschen
- `info` - Modell-Informationen
- `help` - Hilfe anzeigen
- `quit` / `q` / `exit` - Beenden

### GUI Chat

**Standard GUI:**
- ⚙️ **Konfiguration** - Modell, Temperature, Max Tokens
- 💬 **Chat-Bereich** - Farbkodierte Nachrichten
- 🎛️ **System Prompt** - Anpassbare Rolle für Kimi
- 💾 **Chat-Verwaltung** - Speichern/Laden von Gesprächen
- ⌨️ **Tastenkürzel** - Ctrl+Enter zum Senden, F1 für Hilfe

**🎨 Moderne GUI (Empfohlen):**
- 🔤 **Große Schrift** - Gut lesbare 14-16pt Fonts
- 🎨 **Farbenfrohes Design** - Modernes, minimalistisches UI
- 🎤 **Speech-to-Text** - Spracheingabe per Mikrofon
- 🔊 **Text-to-Speech** - Vorlesen der AI-Antworten
- ⚡ **Live-Streaming** - Antworten erscheinen in Echtzeit
- 📱 **Responsive** - Skalierbare Oberfläche
- 🎛️ **Live-Konfiguration** - Modell & Temperature ohne Neustart ändern

### Programmierung (Python)

```python
from kimi_client import KimiClient

# Client initialisieren
kimi = KimiClient()

# Einfacher Chat
response = kimi.simple_chat("Hallo Kimi!")
print(response)

# Chat mit Verlauf
response = kimi.chat_with_history("Was ist Python?")
print(response)

# Streaming Chat
for chunk in kimi.chat_stream("Erkläre Machine Learning"):
    print(chunk, end="", flush=True)

# Tool Calling
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Retrieve weather information",
        "parameters": {
            "type": "object",
            "required": ["city"],
            "properties": {
                "city": {"type": "string", "description": "City name"}
            }
        }
    }
}]

result = kimi.tool_call("What's the weather in Berlin?", tools)
print(result)
```

## �� Konfiguration

### Modelle

- **`Kimi-K2-Instruct`** - Hauptmodell (empfohlen)
- **`meta-llama/Llama-3.1-8B-Instruct-Turbo`** - Alternative für schnelle Antworten
- **`meta-llama/Llama-3.1-70B-Instruct-Turbo`** - Hochleistungsmodell

### Parameter

- **Temperature:** `0.0-1.0` (empfohlen: `0.6`)
- **Max Tokens:** Bis zu `128K` Token
- **Context Length:** `128K` Token

### System Prompts

```python
# Standard
"You are Kimi, an AI assistant created by Moonshot AI."

# Spezialisiert für Coding
"You are Kimi, a world-class programming assistant. Help with code, debugging, and architecture."

# Deutscher Assistent
"Du bist Kimi, ein hilfreicher KI-Assistent. Antworte immer auf Deutsch."
```

## 🛠️ Tool Calling

Kimi K2 Instruct unterstützt natives Function Calling:

```python
def get_weather(city: str) -> dict:
    return {"weather": "Sunny", "temperature": "22°C"}

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a city",
        "parameters": {
            "type": "object",
            "required": ["city"],
            "properties": {
                "city": {"type": "string", "description": "Name of the city"}
            }
        }
    }
}]

result = kimi.tool_call("What's the weather in Tokyo?", tools)

if result["finish_reason"] == "tool_calls":
    for tool_call in result["tool_calls"]:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        # Führe die Funktion aus
        result = get_weather(**arguments)
```

## 📊 Modell-Spezifikationen

| Eigenschaft | Wert |
|-------------|------|
| **Parameter** | 1 Trillion (32B aktiviert) |
| **Architektur** | Mixture-of-Experts (MoE) |
| **Kontext** | 128K Token |
| **Spezialisierung** | Coding, Reasoning, Tool Use |
| **Provider** | Together AI |
| **Training** | 15.5T Token mit Muon Optimizer |

## 🎯 Anwendungsfälle

### Coding & Development
- **Code-Generierung** - Vollständige Programme
- **Debugging** - Fehleranalyse und -behebung
- **Code Review** - Qualitätsprüfung
- **Architektur** - System-Design

### Reasoning & Analyse
- **Mathematik** - Komplexe Berechnungen
- **Logik** - Problemlösung
- **Analyse** - Datenauswertung
- **Forschung** - Literatur-Review

### Tool Use & Automation
- **API-Integration** - Externe Services
- **Workflow-Automation** - Prozess-Optimierung
- **Data Processing** - Datenverarbeitung
- **System-Integration** - Tool-Orchestrierung

## 🔍 Fehlerbehebung

### API-Key Probleme

```bash
❌ Fehler: Bitte setzen Sie TOGETHER_API_KEY in der .env-Datei
```

**Lösung:**
1. Gehen Sie zu: https://api.together.xyz/settings/api-keys
2. Erstellen Sie einen neuen API-Key
3. Setzen Sie ihn in der `.env`-Datei:
   ```
   TOGETHER_API_KEY=your_actual_api_key_here
   ```

### Dependencies

```bash
❌ Fehler beim Installieren der Requirements
```

**Lösung:**
```bash
pip3 install together python-dotenv pydantic
```

### GUI Probleme

Wenn die GUI nicht startet:
```bash
# macOS
brew install python-tk

# Ubuntu/Debian
sudo apt-get install python3-tk

# Windows
# Meist bereits enthalten
```

## 📚 API-Referenz

### KimiClient Klasse

```python
class KimiClient:
    def __init__(self, model: str = "moonshotai/Kimi-K2-Instruct", 
                 temperature: float = 0.6, max_tokens: int = 4096)
    
    def simple_chat(self, message: str) -> str
    def chat_with_history(self, message: str, system_prompt: Optional[str] = None) -> str
    def chat_stream(self, message: str, system_prompt: Optional[str] = None) -> Iterator[str]
    def tool_call(self, message: str, tools: List[Dict[str, Any]]) -> Dict[str, Any]
    def clear_history(self)
    def get_models(self) -> List[str]
    def set_model(self, model: str)
    def get_model_info(self) -> Dict[str, Any]
```

## 🆚 Benchmark-Ergebnisse

Kimi K2 Instruct führt in vielen Benchmarks:

| Benchmark | Kimi K2 | DeepSeek-V3 | GPT-4.1 |
|-----------|---------|-------------|---------|
| **LiveCodeBench** | **53.7%** | 46.9% | 44.7% |
| **SWE-bench Verified** | **65.8%** | 38.8% | 54.6% |
| **MMLU** | **89.5%** | 89.4% | 90.4% |
| **AIME 2024** | **69.6%** | 59.4% | 46.5% |
| **ZebraLogic** | **89.0%** | 84.0% | 58.5% |


## 🛠️ Kimi K2 Agent

Neue Agent-Klasse `KimiK2Agent` mit direktem Zugriff auf das Execution Toolkit. Befehle aus einer Plan-Datei werden sequenziell ausgeführt.
## 📄 Lizenz

Modified MIT License - Siehe [Hugging Face Modell-Seite](https://huggingface.co/moonshotai/Kimi-K2-Instruct)

## 🤝 Support

- **Together AI Docs:** https://docs.together.ai/
- **Kimi K2 Model Card:** https://huggingface.co/moonshotai/Kimi-K2-Instruct
- **Issues:** Erstellen Sie ein Issue in diesem Repository

---

**Kimi K2 Instruct** - Agentic Intelligence für die Zukunft 🚀 
>>>>>>> cce06cf (first)
