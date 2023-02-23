# Discord Minecraft Stats Bot

This is a Discord bot that can get stats of players on a Minecraft server. The bot has several commands to retrieve stats for different categories such as time played, distance traveled, and items crafted.

## Installation

To use this bot, you'll need to do the following:

1. Install Python 3.6 or above
2. Clone the repo `git clone https://github.com/sailingteam4/MinecraftStats-to-DiscordBot`
4. Install the required dependencies: `discord`, `paramiko`, `requests`, `mojang` and `python-dotenv`. You can do that with `pip install -r requirements.txt`
4. Set up a Discord bot and obtain its token
5. Set up a `.env` file with the following environment variables:
    - `DISCORD_TOKEN` - the bot token
    - `HOST` - the Minecraft server host
    - `USER` - the SFTP user for the Minecraft server
    - `PASS` - the SFTP password for the Minecraft server
    - `PORT` - the SFTP port for the Minecraft server
6. Run the `bot.py` file

## Commands

The following commands are available:

- `/time <pseudo>` - get the time played by a player
- `/jump <pseudo>` - get the number of jumps made by a player
- `/bell <pseudo>` - get the number of bells rung by a player
- `/mined <pseudo>` - get the number of blocks mined by a player
- `/dead <pseudo>` - get the number of deaths of a player
- `/distance <pseudo>` - get the distance traveled by a player in kilometers
- `/broke <pseudo>` - get the number of tools broken by a player
- `/killed <pseudo>` - get the number of monsters killed by a player
- `/crafted <pseudo>` - get the number of items crafted by a player

Replace `<pseudo>` with the Minecraft username of the player you want to retrieve the stats for.
