"""
Telegram Cock Size Bot

Simple bot for generating user cock size through inline queries.
"""

import configparser
import hashlib
import math
import logging
import os
from datetime import date
from typing import List, Optional

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, InlineQueryHandler, CallbackContext


class CockSizeBot:
    """Main bot class for generating cock size."""
    
    # Constants for size generation
    MIN_SIZE = 0
    MAX_SIZE = 50
    MODE = 0
    SPECIAL_USER = '@tech_alex'
    
    # Emojis for different sizes
    SIZE_EMOJIS = {
        (0, 6): '😭',
        (6, 11): '🙁',
        (11, 16): '😐',
        (16, 21): '😏',
        (21, 26): '🥳',
        (26, 31): '🥳',
        (31, 36): '😨',
        (36, float('inf')): '😱'
    }
    
    def __init__(self, config_path: str = 'config.ini'):
        """Initialize bot with configuration loading."""
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self._setup_logging()
        
    def _setup_logging(self) -> None:
        """Setup logging."""
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
        
    def _get_thumbnail_url(self) -> Optional[str]:
        """
        Get thumbnail URL from configuration.
        
        Returns:
            Thumbnail URL or None if not available
        """
        try:
            return self.config.get('DEFAULT', 'thumb')
        except (configparser.NoSectionError, configparser.NoOptionError):
            self.logger.warning("No thumbnail URL found in config")
            return None
        
    def _daily_hash_parser(self, prefix: str) -> float:
        """
        Generate deterministic number from 0 to 1 based on prefix and date.
        
        Args:
            prefix: Prefix for hash generation
            
        Returns:
            Number from 0 to 1
        """
        current_date = str(date.today())
        hash_input = f"{prefix}{current_date}"
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()
        return (int(hash_value, 16) % 100000) / 100000
        
    def _calculate_size(self, user_id: int) -> int:
        """
        Calculate cock size for user.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Size in centimeters
        """
        results = []
        
        for i in range(1, 4):  # 3 iterations for averaging
            hash_value = self._daily_hash_parser(f'cock{i}{user_id}')
            u = math.sin(hash_value)
            
            try:
                c = 0.5 if self.MODE is None else (self.MODE - self.MIN_SIZE) / (self.MAX_SIZE - self.MIN_SIZE)
            except ZeroDivisionError:
                return self.MIN_SIZE
                
            if u > c:
                u = 1.0 - u
                c = 1.0 - c
                low, high = self.MAX_SIZE, self.MIN_SIZE
            else:
                low, high = self.MIN_SIZE, self.MAX_SIZE
                
            result = low + (high - low) * math.sqrt(u * c)
            results.append(result)
            
        return int(sum(results) / len(results))
        
    def _get_emoji_for_size(self, size: int) -> str:
        """
        Return emoji for given size.
        
        Args:
            size: Size in centimeters
            
        Returns:
            Corresponding emoji
        """
        for (min_size, max_size), emoji in self.SIZE_EMOJIS.items():
            if min_size <= size < max_size:
                return emoji
        return self.SIZE_EMOJIS[(36, float('inf'))]  # Default for large sizes
        
    def _apply_special_logic(self, size: int, username: str) -> int:
        """
        Apply special logic for certain users.
        
        Args:
            size: Original size
            username: Username
            
        Returns:
            Modified size
        """
        if username == self.SPECIAL_USER:
            return math.floor(size / 3) + 1
        return size
        
    def _create_inline_result(self, user_id: int, size: int) -> List[InlineQueryResultArticle]:
        """
        Create result for inline query.
        
        Args:
            user_id: User ID
            size: Cock size
            
        Returns:
            List of results for inline query
        """
        emoji = self._get_emoji_for_size(size)
        message_text = f'My cock size is *{size}cm* {emoji}'
        thumb_url = self._get_thumbnail_url()
        
        # Create inline result with text message
        result = InlineQueryResultArticle(
            id=str(user_id),
            title=f"Cock size bot",
            description=f"Share your cock size",
            input_message_content=InputTextMessageContent(
                message_text=message_text,
                parse_mode='MARKDOWN'
            ),
            thumbnail_url=thumb_url
        )
        
        return [result]
        
    async def handle_inline_query(self, update: Update, context: CallbackContext) -> None:
        """
        Inline query handler.
        
        Args:
            update: Telegram update object
            context: Callback context
        """
        user = update.inline_query.from_user
        user_id = user.id
        username = user.username
        
        # Calculate size
        size = self._calculate_size(user_id)
        
        # Apply special logic if needed
        if username:
            size = self._apply_special_logic(size, f'@{username}')
            
        # Create result
        results = self._create_inline_result(user_id, size)
        
        # Log request
        self.logger.info(f"User {username} ({user_id}) requested size: {size}cm")
        
        # Send result
        await update.inline_query.answer(results, cache_time=0)
        
    def run(self) -> None:
        """Start the bot."""
        try:
            token = self.config.get('DEFAULT', 'token')
            if not token:
                raise ValueError("Bot token not found in config.ini")
                
            self.logger.info("Starting Telegram bot...")
            
            # Create application
            application = Application.builder().token(token).build()
            
            # Add inline query handler
            application.add_handler(InlineQueryHandler(self.handle_inline_query))
            
            # Start the bot
            self.logger.info("Bot has started successfully")
            application.run_polling()
            
        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
            raise


def main() -> None:
    """Main function to start the bot."""
    try:
        bot = CockSizeBot()
        bot.run()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
