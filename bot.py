from aiogram import Bot, Dispatcher, executor, types
from telegraph import Telegraph
import uuid
import os 

API_TOKEN = os.getenv("API_TOKEN")
CHANNEL_ID = -1002523154982  # ID твоего канала
BOT_USERNAME = "@FluxPromptBot"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

telegraph = Telegraph()
telegraph.create_account(short_name="FluxPrompts")


def get_text_and_entities(message: types.Message):
    if message.text:
        return message.text, message.entities
    if message.caption:
        return message.caption, message.caption_entities
    return None, None


@dp.channel_post_handler()
async def catch_mention(message: types.Message):
    # только нужный канал
    if message.chat.id != CHANNEL_ID:
        return

    # игнор репостов
    if message.forward_from or message.forward_from_chat:
        return

    # берём текст ИЛИ подпись
    text = message.text or message.caption
    if not text:
        return

    # 🔑 САМЫЙ НАДЁЖНЫЙ ТРИГГЕР
    if BOT_USERNAME not in text:
        return

    prompt_text = text.replace(BOT_USERNAME, "").strip()
    if not prompt_text:
        return

    page = telegraph.create_page(
        title="Flux Prompt",
        html_content=f"<pre>{prompt_text}</pre>"
    )

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="📋 Копировать промпт",
            url=page["url"]
        )
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text="Готово ✨",
        reply_to_message_id=message.message_id,
        reply_markup=keyboard
    )




if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True)
