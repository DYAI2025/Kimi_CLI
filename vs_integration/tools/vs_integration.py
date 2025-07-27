#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Visual Studio Integration Tools for Kimi K2 CLI
Helper tools to integrate Kimi K2 functionality with Visual Studio
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, Optional


class VSIntegrationManager:
    """Manages Visual Studio integration for Kimi K2"""
    
    def __init__(self, vs_project_path: str = None):
        self.vs_project_path = vs_project_path
        self.kimi_config = self._load_kimi_config()
    
    def _load_kimi_config(self) -> Dict[str, Any]:
        """Load Kimi configuration from .env file"""
        config = {}
        env_file = Path(".env")
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        config[key] = value
        
        return config
    
    def install_extension(self) -> bool:
        """Install the Kimi K2 VS extension"""
        print("🔧 Installing Kimi K2 Visual Studio Extension...")
        
        # Check if VS is installed
        vs_paths = [
            "C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\Common7\\IDE\\devenv.exe",
            "C:\\Program Files\\Microsoft Visual Studio\\2022\\Professional\\Common7\\IDE\\devenv.exe",
            "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\IDE\\devenv.exe",
            "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Enterprise\\Common7\\IDE\\devenv.exe",
            "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Professional\\Common7\\IDE\\devenv.exe",
            "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\Common7\\IDE\\devenv.exe"
        ]
        
        vs_path = None
        for path in vs_paths:
            if os.path.exists(path):
                vs_path = path
                break
        
        if not vs_path:
            print("❌ Visual Studio not found. Please install Visual Studio 2019 or later.")
            return False
        
        print(f"✅ Found Visual Studio at: {vs_path}")
        
        # Build extension (simplified)
        extension_dir = Path(__file__).parent / "extension"
        if extension_dir.exists():
            print("✅ Extension files found")
            # In a real scenario, we would build and install the VSIX package
            print("📦 Extension ready for installation")
            print("💡 To install manually: Double-click the .vsix file when built")
            return True
        else:
            print("❌ Extension files not found")
            return False
    
    def create_project_template(self, output_dir: str) -> bool:
        """Create VS project template for Kimi K2 projects"""
        try:
            template_dir = Path(__file__).parent.parent / "templates" / "ProjectTemplates" / "KimiK2Agent"
            output_path = Path(output_dir)
            
            if not template_dir.exists():
                print(f"❌ Template directory not found: {template_dir}")
                return False
            
            # Copy template files
            import shutil
            shutil.copytree(template_dir, output_path / "KimiK2Agent", dirs_exist_ok=True)
            
            print(f"✅ Project template created at: {output_path / 'KimiK2Agent'}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating project template: {e}")
            return False
    
    def configure_intellisense(self) -> bool:
        """Configure IntelliSense for Kimi K2 development"""
        print("🧠 Configuring IntelliSense for Kimi K2...")
        
        # Create Python path configuration
        python_paths = [
            ".",
            "./tools",
            "./src",
        ]
        
        # Create .vscode/settings.json for VS Code compatibility
        vscode_dir = Path(".vscode")
        vscode_dir.mkdir(exist_ok=True)
        
        settings = {
            "python.defaultInterpreterPath": sys.executable,
            "python.autoComplete.addBrackets": True,
            "python.analysis.extraPaths": python_paths,
            "python.linting.enabled": True,
            "python.linting.flake8Enabled": True,
            "python.linting.mypyEnabled": True,
            "files.associations": {
                "*.txt": "plaintext"
            },
            "python.terminal.activateEnvironment": True
        }
        
        with open(vscode_dir / "settings.json", 'w') as f:
            json.dump(settings, f, indent=2)
        
        print("✅ IntelliSense configuration created")
        return True
    
    def setup_debugging(self) -> bool:
        """Setup debugging configuration"""
        print("🐛 Setting up debugging configuration...")
        
        # Create launch.json for debugging
        vscode_dir = Path(".vscode")
        vscode_dir.mkdir(exist_ok=True)
        
        launch_config = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python: Kimi Agent",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/main.py",
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}",
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}"
                    },
                    "args": []
                },
                {
                    "name": "Python: Run Plan",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/main.py",
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}",
                    "args": ["--plan", "${input:planFile}"]
                }
            ],
            "inputs": [
                {
                    "id": "planFile",
                    "description": "Plan file to execute",
                    "default": "plans/example_plan.txt",
                    "type": "promptString"
                }
            ]
        }
        
        with open(vscode_dir / "launch.json", 'w') as f:
            json.dump(launch_config, f, indent=2)
        
        print("✅ Debugging configuration created")
        return True
    
    def generate_snippets(self) -> bool:
        """Generate code snippets for Kimi K2 development"""
        print("✂️ Generating code snippets...")
        
        snippets = {
            "Kimi Agent Init": {
                "prefix": "kimi-init",
                "body": [
                    "from kimi_agent import KimiK2Agent",
                    "from config import Config",
                    "",
                    "# Initialize configuration",
                    "config = Config()",
                    "",
                    "# Create agent",
                    "agent = KimiK2Agent(",
                    "    api_key=config.API_KEY,",
                    "    model=config.MODEL_NAME,",
                    "    temperature=config.TEMPERATURE",
                    ")",
                    "",
                    "# $0"
                ],
                "description": "Initialize Kimi K2 Agent"
            },
            "Kimi Chat": {
                "prefix": "kimi-chat",
                "body": [
                    "response = agent.chat(\"${1:Your message here}\")",
                    "print(f\"🤖 {response}\")",
                    "$0"
                ],
                "description": "Chat with Kimi K2"
            },
            "Kimi Analyze Code": {
                "prefix": "kimi-analyze",
                "body": [
                    "with open(\"${1:filename.py}\", 'r') as f:",
                    "    code = f.read()",
                    "",
                    "analysis = agent.analyze_code(code, \"${1:filename.py}\")",
                    "print(f\"📊 Analysis: {analysis}\")",
                    "$0"
                ],
                "description": "Analyze code with Kimi K2"
            },
            "Kimi Execute Plan": {
                "prefix": "kimi-plan",
                "body": [
                    "agent.execute_plan(\"${1:plans/example_plan.txt}\")",
                    "$0"
                ],
                "description": "Execute a plan file"
            }
        }
        
        # Save snippets
        vscode_dir = Path(".vscode")
        vscode_dir.mkdir(exist_ok=True)
        
        with open(vscode_dir / "kimi.code-snippets", 'w') as f:
            json.dump(snippets, f, indent=2)
        
        print("✅ Code snippets generated")
        return True
    
    def validate_setup(self) -> bool:
        """Validate the VS integration setup"""
        print("✅ Validating Kimi K2 Visual Studio integration...")
        
        checks = [
            ("Configuration file", Path(".env").exists()),
            ("Project structure", Path("main.py").exists()),
            ("Tools directory", Path("tools").exists()),
            ("Plans directory", Path("plans").exists()),
            ("VS Code settings", Path(".vscode/settings.json").exists()),
            ("Debug configuration", Path(".vscode/launch.json").exists()),
            ("Code snippets", Path(".vscode/kimi.code-snippets").exists())
        ]
        
        all_passed = True
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n🎉 Visual Studio integration setup complete!")
            print("\n📋 Next steps:")
            print("1. Open the project in Visual Studio")
            print("2. Install Python support if not already installed")
            print("3. Configure your Moonshot AI API key in .env")
            print("4. Start coding with Kimi K2!")
        else:
            print("\n⚠️ Some setup items failed. Please check the configuration.")
        
        return all_passed


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Kimi K2 Visual Studio Integration Tools")
    parser.add_argument("command", choices=["install", "template", "configure", "validate"], 
                       help="Command to execute")
    parser.add_argument("--output", "-o", help="Output directory for templates")
    parser.add_argument("--project", "-p", help="VS project path")
    
    args = parser.parse_args()
    
    manager = VSIntegrationManager(args.project)
    
    if args.command == "install":
        manager.install_extension()
    elif args.command == "template":
        output_dir = args.output or "."
        manager.create_project_template(output_dir)
    elif args.command == "configure":
        manager.configure_intellisense()
        manager.setup_debugging()
        manager.generate_snippets()
    elif args.command == "validate":
        manager.validate_setup()


if __name__ == "__main__":
    main()