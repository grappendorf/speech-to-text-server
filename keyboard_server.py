#!/usr/bin/env python3

import subprocess
import time
from flask import Flask, request, jsonify
import logging
import os
import pwd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Security configuration
DEFAULT_PIN = "123456"
VALID_PIN = os.environ.get('KEYBOARD_SERVER_PIN', DEFAULT_PIN)
logger.info(f"Using {'custom' if 'KEYBOARD_SERVER_PIN' in os.environ else 'default'} PIN configuration")

def set_keyboard_layout():
    """Set the keyboard layout to German."""
    try:
        env = os.environ.copy()
        env['DISPLAY'] = get_display()
        subprocess.run(['setxkbmap', 'de'], env=env, check=True)
        logger.info("Keyboard layout set to German")
        return True
    except Exception as e:
        logger.error(f"Error setting keyboard layout: {e}")
        return False

def get_display():
    """Get the current display for the user."""
    try:
        # Get DISPLAY from environment
        display = os.environ.get('DISPLAY')
        if display:
            return display
        
        # If not found, try to get it from the active session
        cmd = ["who", "-u"]
        output = subprocess.check_output(cmd).decode()
        for line in output.split('\n'):
            if '(:' in line:
                display = ':' + line.split('(:')[1].split(')')[0]
                return display
    except Exception as e:
        logger.error(f"Error getting display: {e}")
    return ":0"  # Default to :0 if nothing else works

def simulate_return():
    """Simulate pressing the Return key using xdotool."""
    try:
        display = get_display()
        env = os.environ.copy()
        env['DISPLAY'] = display
        cmd = ['xdotool', 'key', 'Return']
        subprocess.run(cmd, env=env, check=True)
        return True
    except Exception as e:
        logger.error(f"Error simulating Return key: {e}")
        return False

def type_text_part(text: str):
    """Type a part of text using xdotool."""
    try:
        display = get_display()
        env = os.environ.copy()
        env['DISPLAY'] = display
        cmd = ['xdotool', 'type', '--delay', '50', text]
        subprocess.run(cmd, env=env, check=True)
        return True
    except Exception as e:
        logger.error(f"Error while typing text part: {e}")
        return False

def type_string(text: str):
    """Simulate typing of a string using xdotool.
    Returns: tuple of (success: bool, was_command: bool)"""
    try:
        # Captain Picard's signature command to execute the last order
        command_text = "make it so"
        if text.endswith(command_text):
            # Type everything before the command
            prefix = text[:-len(command_text)].rstrip()
            if prefix:
                if not type_text_part(prefix):
                    return False, False
                time.sleep(0.1)  # Small delay between typing and Return
            return simulate_return(), True
            
        # If no command found, type the entire text
        return type_text_part(text), False
    except Exception as e:
        logger.error(f"Error while typing: {e}")
        return False, False

@app.route("/type", methods=["POST"])
def type_text():
    """Endpoint to receive text and simulate keyboard input."""
    try:
        data = request.get_json()
        logger.info(f"Received request body: {data}")
        
        if not data or "text" not in data or "pin" not in data:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
        # Verify PIN
        if data["pin"] != VALID_PIN:
            logger.warning("Invalid PIN received")
            return jsonify({"status": "error", "message": "Invalid PIN"}), 403
            
        text = data["text"]
        success, was_command = type_string(text)
        if success:
            action = "typed text and pressed Return" if was_command else f"typed text: {text}"
            return jsonify({"status": "success", "message": f"Successfully {action}"})
        else:
            return jsonify({"status": "error", "message": "Failed to type text"}), 500
            
    except Exception as e:
        logger.error(f"Error in type_text endpoint: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Set keyboard layout before starting the server
    if not set_keyboard_layout():
        logger.warning("Failed to set keyboard layout, keyboard input might be incorrect")
    app.run(host="0.0.0.0", port=8000) 
