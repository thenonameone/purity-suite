#!/bin/bash

# Android Recovery & Debugging Suite Launcher
# Quick launcher for the comprehensive Android toolkit

echo "🚀 Launching Android Recovery & Debugging Suite..."
echo ""

# Check if tools exist
if [[ ! -f "$HOME/data-recovery/tools/android-master-menu.sh" ]]; then
    echo "❌ Android suite not found. Please ensure the toolkit is properly installed."
    exit 1
fi

# Launch the master menu
exec "$HOME/data-recovery/tools/android-master-menu.sh"