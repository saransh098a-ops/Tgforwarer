import logging
import asyncio
from pyrogram import Client, filters

# Server logs setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = 23011335
API_HASH = "e6afd493eef834ef069e5fe84fec10f1"
SESSION_STRING = "BQFfIAcAIzQMuI4qulpULKlFQWR4JtViLEgMDnTXNK2-gwEa_JoOYBJ17pDDvXdsVQCXWAptkcNmQGufvqvsgN6mJSRM-veftIKbkfJRdta-eDdHNLCMMokNbQ2Ye2FiH4ItvjrS1DZlQOhEqhZ56K9ZE37FZXysa8Mr8nfQI_fVRzqdNbbEwO5TE_dTVU_TH3a6sN7xvlXIHGA25wpfFIz-Mq4Ljz-DR9C5WHx2122zVGKKvIC867SZjBVvZXk9pB-zH0Gx1ohZikOvLPk2Rev6arqfxBmwzCfHysid2R2CudIwdfyOMK6UTmo66Hq49frGqEpwhqotIm4iuNOHEAh7s3QyhwAAAAGkgG8eAA"

SOURCE_CHATS = [
    -1002361849910, -1002665293753, -1003148116572, 
    -1002471226575, -1002892320267, -1002105517884, 
    -1002066717511, -1002341140504, -1002625284153
]
TARGET_CHAT = -1003785009558

app = Client("forwarder_instance", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.on_message(filters.chat(SOURCE_CHATS))
async def handle_forward(client, message):
    try:
        await message.copy(chat_id=TARGET_CHAT)
        logger.info(f"Successfully forwarded message from: {message.chat.id}")
    except Exception as error:
        logger.error(f"Failed to forward message: {error}")

async def main():
    logger.info("Connecting to Telegram Server...")
    await app.start()
    
    # Peer Cache ko warm-up karne ke liye saare dialogs load kar rahe hain
    logger.info("Warming up database peer cache... Loading active chats...")
    try:
        async for dialog in app.get_dialogs():
            pass  # Yeh background mein cache database ko built kar dega
        logger.info("Database peer cache successfully loaded!")
    except Exception as cache_err:
        logger.warning(f"Cache warm-up encountered a minor issue: {cache_err}")

    logger.info("Railway 24/7 Forwarder Engine is now completely safe and ONLINE!")
    # Script ko hamesha active rakhne ke liye keep-alive lock
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
