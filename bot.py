"""
This is a Wikipedia bot.
It provides Wikipedia summaries for any incoming text messages.
"""

# https://api.telegram.org/bot7510753947:AAHRnA9nPYj_-u73rLKDLIeLlvb6wH5KXZg/getMe

import logging
from aiogram import Bot, Dispatcher, executor, types
import wikipedia

API_TOKEN = "7510753947:AAHRnA9nPYj_-u73rLKDLIeLlvb6wH5KXZg"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Set the default Wikipedia language
DEFAULT_LANG = "uz"
wikipedia.set_lang(DEFAULT_LANG)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Assalom Alaykum, Wikibotga xush kelibsiz!")


async def fetch_wiki_summary(query: str, lang: str) -> str:
    """Fetch Wikipedia summary for a given query and language."""
    wikipedia.set_lang(lang)
    try:
        return wikipedia.summary(query)
    except wikipedia.exceptions.PageError:
        return None
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Ko'proq aniqlik kiriting: {', '.join(e.options)}"
    except Exception:
        return "Xato yuz berdi yoki mavzuga doir ma'lumot topilmadi."


@dp.message_handler()
async def send_wiki(message: types.Message):
    # Try fetching in the default language (Uzbek)
    result = await fetch_wiki_summary(message.text, DEFAULT_LANG)

    # If no result, try in English
    if not result:
        result = await fetch_wiki_summary(message.text, "en")
        if not result:
            result = "Bu mavzuga doir ma'lumot topilmadi"

    await message.reply(result)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
