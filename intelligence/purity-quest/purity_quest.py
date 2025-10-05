#!/usr/bin/env python3
"""
Purity Quest - A journey towards digital purity
"""

import sys
import time
import random

def display_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                        PURITY QUEST                          ║
    ║                                                              ║
    ║           "The path to digital enlightenment begins"        ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def purification_process():
    steps = [
        "Initializing purification protocol...",
        "Scanning for digital impurities...",
        "Removing traces of chaos...",
        "Cleansing the data streams...",
        "Aligning quantum frequencies...",
        "Harmonizing system energies...",
        "Achieving digital zen...",
        "Purification complete!"
    ]
    
    for step in steps:
        print(f"[*] {step}")
        time.sleep(random.uniform(0.5, 1.5))
    
    print("\n✨ You have achieved digital purity! ✨")
    print("Your system is now in a state of perfect harmony.")

def main():
    display_banner()
    print("Welcome to the Purity Quest!")
    print("This sacred ritual will cleanse your digital soul.\n")
    
    response = input("Are you ready to begin your purification journey? (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        print("\nCommencing purification ritual...\n")
        purification_process()
    else:
        print("Perhaps another time. The path to purity awaits when you are ready.")
        sys.exit(0)

if __name__ == "__main__":
    main()