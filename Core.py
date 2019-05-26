import discord

from commands.CommandManager import CommandManager
from commands.GreetCommand import GreetCommand

commandManager = CommandManager()

commandManager.addCommand(GreetCommand("greet"))

commandManager.setPrefix("!")


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        for command in commandManager.coms:
            if message.content.startswith(commandManager.prefix + command.name):
                await command.execute(message)

    async def on_ready(self):
        for guild in client.guilds:
            print(guild.name)


client = MyClient()
client.run(open("token.txt", "r").read())
