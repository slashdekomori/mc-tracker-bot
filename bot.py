import discord
import asyncio
from mcstatus import JavaServer
import os
from dotenv import load_dotenv
load_dotenv()

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
MC_HOST   = os.getenv("MC_HOST")
MC_PORT   = int(os.getenv("MC_PORT", 25565))  # fallback to 25565 if not set
INTERVAL  = 30  # seconds between polls
# --------------

intents = discord.Intents.default()
client  = discord.Client(intents=intents)

async def update_presence():
    await client.wait_until_ready()
    server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")

    while not client.is_closed():
        try:
            status = server.status()
            online  = status.players.online
            maximum = status.players.max
            motd    = status.description.strip()

            # Rich presence text shown under the bot's name
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{online}/{maximum} players online",
            )
            await client.change_presence(status=discord.Status.online, activity=activity)
            print(f"[OK] {online}/{maximum} — {motd}")

        except Exception as e:
            # Server is offline or unreachable
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name="Server is offline",
            )
            await client.change_presence(status=discord.Status.do_not_disturb, activity=activity)
            print(f"[WARN] Could not reach server: {e}")

        await asyncio.sleep(INTERVAL)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} — tracking {MC_HOST}:{MC_PORT}")
    client.loop.create_task(update_presence())


client.run(BOT_TOKEN)
