# Makefile for Telegram Cock Size Bot

.PHONY: help install run clean venv deps

## venv: Create virtual environment
venv:
	python3 -m venv venv
	@echo "Virtual environment created. Activate it with: source venv/bin/activate"

## install: Install dependencies
install: venv
	@echo "Installing dependencies..."
	venv/bin/pip install -r requirements.txt
	@echo "Dependencies installed successfully"

## deps: Install dependencies (alternative)
deps:
	pip install -r requirements.txt

## run: Run with virtual environment
run:
	@echo "Starting Telegram bot with virtual environment..."
	venv/bin/python main.py

## clean: Cleaning virtual environment
clean:
	@echo "Cleaning virtual environment..."
	rm -rf venv/
	@echo "Virtual environment cleaned"

## start: Start bot in background
start:
	@echo "Starting bot in background..."
	@nohup venv/bin/python main.py > bot.log 2>&1 &
	@echo "Bot started! PID: $$(pgrep -f 'python.*main.py')"
	@echo "Logs: tail -f bot.log"

## stop: Stop running bot
stop:
	@echo "Stopping bot..."
	@pkill -f "python.*main.py" || echo "No bot process found"
	@echo "Bot stopped"

## restart: Restart bot
restart: stop start

## status: Check bot status
status:
	@if pgrep -f "python.*main.py" > /dev/null; then \
		echo "✅ Bot is running (PID: $$(pgrep -f 'python.*main.py'))"; \
		echo "📊 Memory usage: $$(ps -o pid,ppid,cmd,%mem,%cpu --no-headers -p $$(pgrep -f 'python.*main.py'))"; \
	else \
		echo "❌ Bot is not running"; \
	fi

## logs: Show bot logs
logs:
	@echo "📋 Bot logs (last 50 lines):"
	@tail -50 bot.log 2>/dev/null || echo "No log file found"

## follow: Follow bot logs in real-time
follow:
	@echo "📋 Following bot logs (Ctrl+C to stop):"
	@tail -f bot.log 2>/dev/null || echo "No log file found"

## Production deployment

## deploy: Deploy bot for production
deploy: install
	@echo "🚀 Deploying bot for production..."
	@mkdir -p logs
	@echo "✅ Bot ready for production deployment"
	@echo "💡 Use 'make start' to run in background"
	@echo "💡 Use 'make status' to check if running"
	@echo "💡 Use 'make logs' to view logs"

## help: Show available Makefile commands
help:
	@echo "Available commands:"
	@awk -F ': ' '/^## [a-zA-Z0-9_-]+:/ { \
		sub(/^## /, "", $$1); \
		target = $$1; \
		help = $$2; \
		while (match(help, /<<[^>]+>>/)) { \
			help = substr(help, 1, RSTART-1) "\033[33m" substr(help, RSTART+2, RLENGTH-4) "\033[0m" substr(help, RSTART+RLENGTH); \
		} \
		printf "  \033[32m%-26s\033[0m %s\n", target, help; \
	}' $(MAKEFILE_LIST)