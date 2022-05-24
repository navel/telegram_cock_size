from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CallbackContext
import configparser
import hashlib
import math
from datetime import date

config = configparser.ConfigParser()
config.read('config.ini')


def calculate_cock_size(user_id: int) -> int:
    low = 0
    high = 50
    mode = 0
    results = []
    for i in [1, 2, 3]:
        u = math.sin(daily_int_hash_parser('cock' + str(i) + str(user_id)))
        try:
            c = 0.5 if mode is None else (mode - low) / (high - low)
        except ZeroDivisionError:
            return low
        if u > c:
            u = 1.0 - u
            c = 1.0 - c
            low, high = high, low
        results.append((low + (high - low) * math.sqrt(u * c)))
    return int((results[0] + results[1] + results[2]) / 3)

# generate 0-1 number
def daily_int_hash_parser(prefix: str) -> float:
    cur_date = str(date.today())
    return (int(hashlib.md5((prefix + cur_date).encode()).hexdigest(), 16) % 100000) / 100000


def get_smile(size: int) -> str:
    if size < 6:
        return '😭'
    elif size < 11:
        return '🙁'
    elif size < 16:
        return '😐'
    elif size < 21:
        return '😏'
    elif size < 26:
        return '🥳'
    elif size < 31:
        return '🥳'
    elif size < 36:
        return '😨'
    else:
        return '😱'


def get_size(update: Update, context: CallbackContext) -> None:
    size = calculate_cock_size(update.inline_query.from_user.id)
    msg_txt = 'My cock size is *' + str(size) + 'cm* ' + get_smile(size)

    thumb = config.get('DEFAULT', 'thumb')
    result = [
        InlineQueryResultArticle(
            id=str(update.inline_query.from_user.id),
            title="Share your cock size",
            input_message_content=InputTextMessageContent(message_text=msg_txt, parse_mode='MARKDOWN'),
            thumb_url=thumb
        )]
    print(update.inline_query.from_user.username, size)
    update.inline_query.answer(result, cache_time=0)


def main() -> None:
    print("Start python app")
    token = config.get('DEFAULT', 'token')
    updater = Updater(token)
    updater.stop()
    dispatcher = updater.dispatcher

    dispatcher.add_handler(InlineQueryHandler(get_size))

    updater.start_polling()
    print("Bot has started")
    updater.idle()


if __name__ == '__main__':
    main()
