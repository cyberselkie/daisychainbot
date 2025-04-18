import os

import arc
import hikari
from dotenv import load_dotenv

# Welcome to arc!

# Useful links:
# - Documentation: https://arc.hypergonial.com
# - GitHub repository: https://github.com/hypergonial/hikari-arc
# - Discord server to get help: https://discord.gg/hikari

# Load token from '.env' file
load_dotenv()

# Add your bot token to the .env file!
bot = hikari.GatewayBot(os.environ["TOKEN"])

# Initialize arc with the bot:
client = arc.GatewayClient(bot)

# Load the extension from 'src/extensions/example.py'
client.load_extension("src.extensions.roll")
client.load_extension("src.extensions.randgen")


# This must be on the last line, no code will run after this:
bot.run()
