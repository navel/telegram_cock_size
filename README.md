# Telegram Cock Size Bot

Simple Telegram bot for generating user cock size through inline queries.

## Description

This bot allows users to get a random cock size through inline queries in Telegram. The size is generated based on the user ID and current date, ensuring result stability throughout the day.

## Features

- **Inline queries**: Users can use the bot via `@username_bot` in any chat
- **Deterministic generation**: Size remains the same throughout the day for one user
- **Emoji reactions**: Different emojis depending on size
- **Special logic**: Special formula is applied for user @tech_alex

## Installation

### Quick installation

```bash
make install
```

### Manual installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure settings:
```bash
cp config.ini.example config.ini
# Edit config.ini with your bot token and thumbnail URL
```

## Running

### Via Makefile

```bash
make run-venv
```

### Manual run

```bash
# With virtual environment
source venv/bin/activate
python main.py

# Or directly
python main.py
```

## Configuration

Create a `config.ini` file:

```ini
[DEFAULT]
token=YOUR_BOT_TOKEN_HERE
thumb=http://example.com/thumb.jpg
```

### Thumbnail Configuration

The bot uses thumbnail URLs for inline queries:
- **Recommended size**: 320x320 pixels (square format)
- **Supported formats**: JPG, PNG, GIF, WebP
- **Maximum file size**: 200 KB
- **Must be accessible via HTTP/HTTPS**

### Getting bot token

1. Find [@BotFather](https://t.me/botfather) in Telegram
2. Send `/newbot` command
3. Follow the instructions to create a bot
4. Copy the received token to `config.ini`

## Usage

1. Start the bot
2. In any chat, start typing `@your_bot_username`
3. Select the suggested result
4. Send the message with the size

## Project Structure

```
telegram_cock_size/
├── main.py              # Main bot code
├── config.ini           # Configuration (create yourself)
├── config.ini.example   # Configuration template
├── requirements.txt     # Python dependencies
├── Makefile            # Project management commands
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## Available Makefile Commands

### Basic Commands
- `make help` - Show help
- `make install` - Install dependencies
- `make run` - Start the bot
- `make run-venv` - Start the bot with virtual environment
- `make clean` - Clean virtual environment
- `make dev-setup` - Full development setup

### Process Management
- `make start` - Start bot in background
- `make stop` - Stop running bot
- `make restart` - Restart bot
- `make status` - Check bot status
- `make logs` - Show bot logs
- `make follow` - Follow logs in real-time

### Production Deployment
- `make deploy` - Deploy for production
- `make install-service` - Install systemd service (Linux)
- `make service-start` - Start systemd service
- `make service-stop` - Stop systemd service
- `make service-status` - Check service status
- `make service-logs` - Show service logs

## Production Deployment

### Option 1: Simple Background Process

```bash
# Deploy and start
make deploy
make start

# Check status
make status

# View logs
make logs
```

### Option 2: Startup Script

```bash
# Make script executable
chmod +x start.sh

# Start bot
./start.sh start

# Check status
./start.sh status

# View logs
./start.sh logs
```

### Option 3: Systemd Service (Linux)

```bash
# Install as system service
make install-service
make service-start

# Check service status
make service-status

# View service logs
make service-logs
```


## Generation Algorithm

Size is generated based on:
- Telegram user ID
- Current date
- Deterministic hash function

This ensures:
- Result stability throughout the day
- Uniqueness for each user
- Daily value updates

## Requirements

- Python 3.7+
- python-telegram-bot
- configparser (built-in module)

## License

This project is created for educational purposes.
