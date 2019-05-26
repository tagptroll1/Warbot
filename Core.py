import discord

from commands.CommandManager import CommandManager
from commands.GreetCommand import GreetCommand
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.DiscordDatabase import Server

Base = declarative_base()

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
        engine = create_engine('sqlite:///data/database/servers.db')

        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)

        session = DBSession()

        for guild in client.guilds:
            print(guild.name)
            # Insert a Server into the server table
            new_server = Server(id=guild.id, faction="NULL")
            session.add(new_server)
            session.commit()


client = MyClient()
client.run(open("token.txt", "r").read())
