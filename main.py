import os

from flask import Flask
from flask_discord_interactions import DiscordInteractions


app = Flask(__name__)
discord = DiscordInteractions(app)


app.config["DISCORD_CLIENT_ID"] = "909869584394375309"
app.config["DISCORD_PUBLIC_KEY"] = "d264c84e405a6ec9f457def0b4ccf6c19646a460ce687591bfb5411f3ed1243e"
app.config["DISCORD_CLIENT_SECRET"] = "odGjnwUOgn7rgUQdPb28Tq-BfCa_4VfF"


@discord.command()
def ping(ctx):
    "Respond with a friendly 'pong'!"
    return "Pong!"


discord.set_route("/interactions")


discord.update_commands(guild_id="909870127686750270")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT'))
