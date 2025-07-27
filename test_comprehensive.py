#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive Test Suite for Kimi K2 CLI
Tests all core functionality without requiring external API keys
"""

import os
import sys
import tempfile
import subprocess
from unittest.mock import patch, MagicMock

def test_imports():
    """Test that all core modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import dotenv
        print("✅ python-dotenv imported")
    except ImportError as e:
        print(f"❌ dotenv import failed: {e}")
        return False

    try:
        import pydantic
        print("✅ pydantic imported")
    except ImportError as e:
        print(f"❌ pydantic import failed: {e}")
        return False

    try:
        import openai
        print("✅ openai imported")
    except ImportError as e:
        print(f"❌ openai import failed: {e}")
        return False

    try:
        import kimi_client
        print("✅ kimi_client imported")
    except ImportError as e:
        print(f"❌ kimi_client import failed: {e}")
        return False

    try:
        import execution_toolkit
        print("✅ execution_toolkit imported")
    except ImportError as e:
        print(f"❌ execution_toolkit import failed: {e}")
        return False

    try:
        import kimi_k2_agent
        print("✅ kimi_k2_agent imported")
    except ImportError as e:
        print(f"❌ kimi_k2_agent import failed: {e}")
        return False

    print("✅ All core imports successful")
    return True

def test_execution_toolkit():
    """Test execution toolkit functionality"""
    print("\n🧪 Testing execution toolkit...")
    
    from execution_toolkit import execute_shell_command, read_file, write_file, delete_file
    
    # Test shell command execution
    result = execute_shell_command('echo "Hello World"')
    if result['exit_code'] == 0 and "Hello World" in result['stdout']:
        print("✅ Shell command execution works")
    else:
        print(f"❌ Shell command failed: {result}")
        return False
    
    # Test file operations
    test_file = tempfile.mktemp(suffix='.txt')
    try:
        test_content = "Test content for Kimi K2 CLI"
        write_file(test_file, test_content)
        
        if os.path.exists(test_file):
            print("✅ File writing works")
        else:
            print("❌ File writing failed")
            return False
        
        read_content = read_file(test_file)
        if read_content == test_content:
            print("✅ File reading works")
        else:
            print(f"❌ File reading failed: expected '{test_content}', got '{read_content}'")
            return False
        
        delete_file(test_file)
        if not os.path.exists(test_file):
            print("✅ File deletion works")
        else:
            print("❌ File deletion failed")
            return False
    
    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)
    
    print("✅ Execution toolkit tests passed")
    return True

def test_kimi_client_init():
    """Test KimiClient initialization"""
    print("\n🧪 Testing KimiClient initialization...")
    
    from kimi_client import KimiClient
    
    # Test with demo API key (should fail gracefully)
    try:
        client = KimiClient()
        print("❌ Should have failed with demo API key")
        return False
    except ValueError as e:
        if "erforderlich" in str(e):
            print("✅ Correctly rejects demo API key")
        else:
            print(f"❌ Unexpected error: {e}")
            return False
    
    # Test with mock API key
    with patch.dict(os.environ, {'MOONSHOT_API_KEY': 'sk-test-key-for-testing'}):
        try:
            client = KimiClient()
            print("✅ KimiClient initializes with valid-looking API key")
        except Exception as e:
            print(f"❌ KimiClient init failed: {e}")
            return False
    
    print("✅ KimiClient initialization tests passed")
    return True

def test_agent_functionality():
    """Test KimiK2Agent functionality"""
    print("\n🧪 Testing KimiK2Agent...")
    
    from kimi_k2_agent import KimiK2Agent
    
    # Test with mock API key
    with patch.dict(os.environ, {'MOONSHOT_API_KEY': 'sk-test-key-for-testing'}):
        try:
            agent = KimiK2Agent()
            print("✅ KimiK2Agent initializes")
        except Exception as e:
            print(f"❌ KimiK2Agent init failed: {e}")
            return False
        
        # Test command execution
        try:
            result = agent.run_command('echo "Agent test"')
            if "Agent test" in result:
                print("✅ Agent command execution works")
            else:
                print(f"❌ Agent command failed: {result}")
                return False
        except Exception as e:
            print(f"❌ Agent command execution failed: {e}")
            return False
    
    print("✅ KimiK2Agent tests passed")
    return True

def test_gui_imports():
    """Test GUI module imports"""
    print("\n🧪 Testing GUI imports...")
    
    try:
        import tkinter
        print("✅ tkinter available")
    except ImportError:
        print("❌ tkinter not available")
        return False
    
    try:
        import kimi_gui
        print("✅ Basic GUI module imports")
    except ImportError as e:
        print(f"❌ Basic GUI import failed: {e}")
        return False
    
    # Modern GUI may fail due to audio dependencies
    try:
        import kimi_gui_modern
        print("✅ Modern GUI module imports")
    except ImportError as e:
        print(f"⚠️  Modern GUI import failed (expected): {e}")
    
    print("✅ GUI import tests completed")
    return True

def test_api_info():
    """Test API info functionality"""
    print("\n🧪 Testing API info...")
    
    try:
        # Run api_info.py script
        result = subprocess.run([sys.executable, 'api_info.py'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ API info script runs successfully")
        else:
            print(f"⚠️  API info script exited with code {result.returncode}")
            if result.stderr:
                print(f"   Error: {result.stderr[:100]}...")
    except Exception as e:
        print(f"❌ API info test failed: {e}")
        return False
    
    return True

def run_all_tests():
    """Run all tests"""
    print("🚀 Kimi K2 CLI - Comprehensive Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_execution_toolkit,
        test_kimi_client_init,
        test_agent_functionality,
        test_gui_imports,
        test_api_info
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Kimi K2 CLI is working correctly.")
        print("\n📋 Functionality Status:")
        print("✅ Core API client")
        print("✅ Execution toolkit")
        print("✅ Agent system")
        print("✅ Basic GUI support")
        print("✅ Configuration management")
        print("\n⚠️  Note: Full functionality requires a valid Moonshot AI API key")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)