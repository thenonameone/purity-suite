#!/usr/bin/env python3
"""
🔒 Purity Privacy Integrator
Quick access to anonymity commands within the Purity ecosystem
"""

import subprocess
import sys
import os
from pathlib import Path

class PurityPrivacy:
    def __init__(self):
        self.commands = {
            'anonymous': 'make-me-anonymous',
            'visible': 'make-me-visible', 
            'help': 'anonymity-help',
            'status': 'make-me-anonymous status',
            'emergency': 'make-me-anonymous emergency',
            'identity': 'make-me-anonymous identity'
        }
    
    def execute(self, action='help'):
        """Execute anonymity command"""
        if action in self.commands:
            command = self.commands[action]
            try:
                if ' ' in command:
                    # Command with arguments
                    cmd_parts = command.split()
                    subprocess.run(cmd_parts, check=True)
                else:
                    # Single command
                    subprocess.run([command], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Error executing {action}: {e}")
                return False
            except FileNotFoundError:
                print(f"❌ Command not found: {command}")
                print("Make sure the anonymity suite is installed.")
                return False
        else:
            print(f"❌ Unknown action: {action}")
            print(f"Available actions: {', '.join(self.commands.keys())}")
            return False

def main():
    """Main entry point for purity privacy commands"""
    privacy = PurityPrivacy()
    
    if len(sys.argv) < 2:
        # Default to help if no argument
        privacy.execute('help')
    else:
        action = sys.argv[1].lower()
        privacy.execute(action)

if __name__ == "__main__":
    main()