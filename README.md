# Virtual Keyboard Server

> 🤖 This project was entirely developed by AI (Claude 3.5 Sonnet) in an interactive pair programming session.

A REST service that simulates keyboard input on Linux via X11, ideal for voice assistants and automation tasks.

Features:
- REST API for simulating keyboard input
- PIN-based authentication with configurable PIN
- Special command support (typing "make it so" simulates Return key)
- Runs as a systemd background service
- German keyboard layout support via setxkbmap
- Secure local network access
- Detailed request logging

## Prerequisites

- Python 3.8 or higher
- Linux with X11
- `xdotool` for keyboard simulation
- `setxkbmap` for keyboard layout configuration

## Installation

1. Install system dependencies (Arch Linux):
```bash
sudo pacman -S xdotool xorg-setxkbmap python-pip
```

For Ubuntu/Debian:
```bash
sudo apt-get install xdotool x11-xkb-utils python3-pip python3-dev
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the systemd service:
```bash
# Copy service file to systemd directory
sudo cp keyboard-simulator.service /etc/systemd/system/keyboard-simulator@${USER}.service

# Optional: Configure a custom PIN (default is 123456)
sudo sed -i 's/#Environment=KEYBOARD_SERVER_PIN=123456/Environment=KEYBOARD_SERVER_PIN=YOUR_PIN/' /etc/systemd/system/keyboard-simulator@${USER}.service

# Reload systemd
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable keyboard-simulator@${USER}
sudo systemctl start keyboard-simulator@${USER}
```

## Configuration

### PIN Authentication
The server requires a PIN for authentication. You can set it in three ways:

1. Environment variable:
```bash
export KEYBOARD_SERVER_PIN=your_pin
```

2. In the systemd service file:
```ini
Environment=KEYBOARD_SERVER_PIN=your_pin
```

3. If not set, it defaults to "123456"

## Usage

The server runs on `http://0.0.0.0:8000` and provides a single endpoint:

- `POST /type`: Accepts JSON with required fields:
  - `text`: The text to type
  - `pin`: Authentication PIN

### Examples

1. Simple text typing:
```bash
curl -X POST "http://localhost:8000/type" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello World", "pin": "123456"}'
```

2. Typing text with Return key:
```bash
curl -X POST "http://localhost:8000/type" \
     -H "Content-Type: application/json" \
     -d '{"text": "Search query make it so", "pin": "123456"}'
```
This will type "Search query" and press Return.

## Response Format

The server responds with JSON:

Success:
```json
{
    "status": "success",
    "message": "Successfully typed text: Hello World"
}
```

Error:
```json
{
    "status": "error",
    "message": "Invalid PIN"
}
```

## Logging

The server logs all requests and operations to the console, including:
- Received request bodies
- PIN validation results
- Keyboard layout configuration
- Any errors that occur

## Security Notes

- The server listens on all interfaces (0.0.0.0) but should be protected by firewall rules
- PIN authentication is required for all typing operations
- X11 display and authentication is handled automatically
- German keyboard layout is set on server startup 