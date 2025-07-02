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

def start_bot():
    import asyncio
    from bot import setup_bot

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = setup_bot()

    async def run_bot():
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        await asyncio.Event().wait()

    loop.run_until_complete(run_bot())

# ✅ Start bot in background
threading.Thread(target=start_bot).start()
