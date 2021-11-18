import asyncio
import quart.flask_patch
from quart import Quart

from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from mcrcon import MCRcon
from dotenv import load_dotenv

import os
from flask_discord_interactions import DiscordInteractions, Message

app = Quart(__name__)
discord = DiscordInteractions(app)

load_dotenv()

app.config["DISCORD_CLIENT_ID"] = os.getenv("DISCORD_CLIENT_ID")
app.config["DISCORD_PUBLIC_KEY"] = os.getenv("DISCORD_PUBLIC_KEY")
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
GROUP_NAME = os.getenv('GROUP_NAME')
VM_NAME = os.getenv('VM_NAME')
PORT = int(os.environ.get("PORT", 5000))


def get_credentials():
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    credentials = ClientSecretCredential(
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET'),
        tenant_id=os.getenv('AZURE_TENANT_ID')
    )
    return credentials, subscription_id


credentials, subscription_id = get_credentials()
compute_client = ComputeManagementClient(credentials, subscription_id)


@discord.command()
def wake(ctx):
    "Wake the bot up. Not necessary but very kind indeed."
    return "I'm awake"


@discord.command()
async def start(ctx):
    "Start server"

    async def do():
        await asyncio.sleep(0.1)
        await ctx.send("Starting Minecraft server")
        start_operation = compute_client.virtual_machines.begin_start(GROUP_NAME, VM_NAME)
        start_operation.wait()
        await asyncio.sleep(20)
        await ctx.send("Minecraft server is ready!")

    asyncio.create_task(do())
    return Message(deferred=True)


@discord.command()
async def stop(ctx):
    "Stop server"

    async def do():
        try:
            with MCRcon(os.getenv('SERVER_URL'), os.getenv('RCON_PASSWORD')) as mcr:
                mcr.command("stop")
        except:
            await ctx.send("Minecraft server seems to be stopped. Deallocating VM...")
        start_operation = compute_client.virtual_machines.begin_deallocate(GROUP_NAME, VM_NAME)
        start_operation.wait()
        await ctx.send("Minecraft server has stopped!")

    asyncio.create_task(do())
    return Message(deferred=True)


discord.set_route_async("/interactions")
discord.update_commands(guild_id=os.getenv("TEST_SERVER_ID"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
