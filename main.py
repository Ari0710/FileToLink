import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from bot import setup_bot, UPLOAD_DIR
import threading

app = FastAPI()

@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}, 404

# ✅ Fixed function
def start_bot():
    import asyncio
    app = setup_bot()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app.run_polling())

# Start bot in background
threading.Thread(target=start_bot).start()
