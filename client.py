import os
from pyrogram import Client
from subprocess import Popen
import asyncio

# Load environment variables securely
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION = os.getenv("SESSION")

User = Client(name="user", session_string=SESSION)
DlBot = Client(name="auto-delete", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"}
        )

    async def start(self):
        await super().start()
        try:
            await User.start()
            print("⚡ Bot Started ⚡")
        except Exception as e:
            print(f"Error starting User client: {e}")

        # Run the `delete` script asynchronously
        self.delete_process = Popen("python3 -m utils.delete", shell=True)

    async def stop(self, *args):
        # Stop both Bot and User clients
        await User.stop()
        await super().stop()
        print("Bot stopped.")
        # Optionally terminate the delete process
        self.delete_process.terminate()

# Instantiate and run the bot
if __name__ == "__main__":
    bot = Bot()
    bot.run()
