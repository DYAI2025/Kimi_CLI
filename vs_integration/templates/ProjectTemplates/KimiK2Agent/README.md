# $projectname$ - Kimi K2 AI Agent

Autonomous AI agent powered by **Kimi K2 Instruct** - the state-of-the-art MoE model with 1 trillion parameters.

## 🚀 Features

- **🤖 Advanced AI Agent** - Powered by Kimi K2 Instruct
- **💻 Code Execution** - Safe shell command execution
- **📊 Code Analysis** - Automated bug detection and optimization
- **🧪 Test Generation** - Comprehensive unit test creation
- **💬 Interactive Chat** - Natural language programming interface
- **📋 Plan Execution** - Automated workflow execution
- **🔄 Conversation Management** - Save and load chat history

## 📦 Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Moonshot AI API key
   ```

3. **Run the Agent:**
   ```bash
   python main.py
   ```

## 🎯 Usage

### Interactive Mode

```bash
python main.py
```

Available commands:
- `/help` - Show help
- `/analyze <file>` - Analyze code file
- `/run <command>` - Execute shell command
- `/plan <file>` - Execute plan from file
- `/quit` - Exit

### Programmatic Usage

```python
from kimi_agent import KimiK2Agent

agent = KimiK2Agent()

# Chat with the agent
response = agent.chat("Write a Python function to calculate fibonacci numbers")

# Analyze code
analysis = agent.analyze_code(code, "fibonacci.py")

# Generate tests
tests = agent.generate_tests(code, "python")
```

## 📋 Plan Files

Create plan files in the `plans/` directory with shell commands:

```bash
# Example plan
echo "Starting build process"
python -m pytest tests/
python setup.py build
echo "Build complete"
```

## ⚙️ Configuration

Edit `config.py` or use environment variables:

- `MOONSHOT_API_KEY` - Your Moonshot AI API key
- `KIMI_MODEL` - Model name (default: moonshotai/Kimi-K2-Instruct)
- `TEMPERATURE` - Response creativity (0.0-1.0)
- `MAX_TOKENS` - Maximum response length

## 🔒 Security

- Shell execution is sandboxed with timeouts
- API keys are loaded from environment
- Commands are logged for audit

## 📚 Examples

See the `examples/` directory for:
- Code analysis workflows
- Test generation examples
- Automated development plans
- Integration patterns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Powered by Kimi K2 Instruct** 🚀