import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from bot import setup_bot, UPLOAD_DIR
import threading

app = FastAPI()

# Serve files via /files/<filename>
@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}, 404

# Start Telegram bot in a separate thread
def start_bot():
    import asyncio
    app = setup_bot()
    asyncio.run(app.run_polling())

threading.Thread(target=start_bot).start()
