#!/usr/bin/env python3
"""
 BONZAI DEPENDENCY FIXER
Install missing dependencies and fix configuration issues
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and return success status"""
    print(f" {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f" {description}: SUCCESS")
            return True
        else:
            print(f" {description}: FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f" {description}: ERROR - {e}")
        return False

def main():
    print(" FIXING BONZAI DEPENDENCIES")
    print("=" * 50)
    
    fixes = [
        ("pip install e2b-code-interpreter", "Installing E2B Code Interpreter"),
        ("pip install playwright", "Installing Playwright"),
        ("pip install crewai[all]", "Installing CrewAI"),
        ("pip install --upgrade openai", "Upgrading OpenAI"),
        ("pip install google-generativeai", "Installing Google Generative AI"),
        ("pip install --upgrade mem0ai", "Upgrading Mem0")
    ]
    
    success_count = 0
    
    for command, description in fixes:
        if run_command(command, description):
            success_count += 1
        print()
    
    print(f" SUMMARY: {success_count}/{len(fixes)} fixes successful")
    
    if success_count == len(fixes):
        print(" ALL DEPENDENCIES FIXED!")
    else:
        print(" Some dependencies still need attention")

if __name__ == "__main__":
    main()