#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
$projectname$ - Kimi K2 AI Agent
Autonomous AI agent powered by Kimi K2 Instruct
"""

import os
import sys
from dotenv import load_dotenv
from kimi_agent import KimiK2Agent
from config import Config

def main():
    """Main entry point for the Kimi K2 agent"""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize configuration
    config = Config()
    
    print(f"🤖 Starting {config.PROJECT_NAME}...")
    print(f"Model: {config.MODEL_NAME}")
    print(f"Temperature: {config.TEMPERATURE}")
    print("=" * 50)
    
    try:
        # Initialize the agent
        agent = KimiK2Agent(
            api_key=config.API_KEY,
            model=config.MODEL_NAME,
            temperature=config.TEMPERATURE
        )
        
        # Example: Interactive mode
        print("💬 Entering interactive mode. Type 'quit' to exit.")
        
        while True:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_input.startswith('/'):
                # Handle commands
                handle_command(agent, user_input[1:])
            else:
                # Regular chat
                response = agent.chat(user_input)
                print(f"\n🤖 {response}")
    
    except KeyboardInterrupt:
        print("\n\n👋 Agent stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

def handle_command(agent, command):
    """Handle special commands"""
    parts = command.split()
    cmd = parts[0].lower()
    
    if cmd == 'help':
        print("""
Available commands:
  /help           - Show this help
  /analyze <file> - Analyze code file
  /run <command>  - Execute shell command
  /plan <file>    - Execute plan from file
  /quit           - Exit the agent
        """)
    
    elif cmd == 'analyze':
        if len(parts) > 1:
            filename = parts[1]
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    code = f.read()
                result = agent.analyze_code(code, filename)
                print(f"\n📊 Analysis for {filename}:\n{result}")
            else:
                print(f"❌ File not found: {filename}")
        else:
            print("❌ Usage: /analyze <filename>")
    
    elif cmd == 'run':
        if len(parts) > 1:
            command = ' '.join(parts[1:])
            result = agent.execute_command(command)
            print(f"\n💻 Command result:\n{result}")
        else:
            print("❌ Usage: /run <command>")
    
    elif cmd == 'plan':
        if len(parts) > 1:
            plan_file = parts[1]
            if os.path.exists(plan_file):
                agent.execute_plan(plan_file)
            else:
                print(f"❌ Plan file not found: {plan_file}")
        else:
            print("❌ Usage: /plan <filename>")
    
    else:
        print(f"❌ Unknown command: {cmd}. Type /help for available commands.")

if __name__ == "__main__":
    main()