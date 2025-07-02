import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

UPLOAD_DIR = "files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file_id = None

    if message.document:
        file_id = message.document.file_id
        filename = message.document.file_name
    elif message.video:
        file_id = message.video.file_id
        filename = message.video.file_name or "video.mp4"
    elif message.audio:
        file_id = message.audio.file_id
        filename = message.audio.file_name or "audio.mp3"
    elif message.photo:
        file_id = message.photo[-1].file_id
        filename = f"{file_id}.jpg"
    else:
        await update.message.reply_text("Please send a document, video, audio or photo.")
        return

    file = await context.bot.get_file(file_id)
    file_path = os.path.join(UPLOAD_DIR, filename)
    await file.download_to_drive(file_path)

    base_url = os.environ.get("BASE_URL", "http://localhost:8000")
    download_url = f"{base_url}/files/{filename}"
    await update.message.reply_text(f"✅ File saved!\n📥 Download link: {download_url}")

def setup_bot():
    bot_token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(MessageHandler(filters.ALL, handle_file))
    return app
