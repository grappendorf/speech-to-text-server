#!/bin/bash

# Help text
show_help() {
    echo "Usage: $0 [PIN]"
    echo "Starts the Virtual Keyboard Server"
    echo ""
    echo "Arguments:"
    echo "  PIN    Optional: The PIN to use for authentication (default: 123456)"
    echo ""
    echo "Example:"
    echo "  $0 987654    # Start server with PIN 987654"
    echo "  $0           # Start server with default PIN"
}

# Check if help is requested
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    show_help
    exit 0
fi

# Set PIN if provided, otherwise use default
if [ -n "$1" ]; then
    export KEYBOARD_SERVER_PIN="$1"
fi

# Ensure we're in the script's directory
cd "$(dirname "$0")"

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the server
python keyboard_server.py 