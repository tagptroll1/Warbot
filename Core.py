import discord

from commands import CommandManager, GreetCommand, JoinCommand
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.DiscordDatabase import Server

Base = declarative_base()

commandManager = CommandManager()

commandManager.addCommand(GreetCommand("greet"))
commandManager.addCommand(JoinCommand("join"))

commandManager.setPrefix("!")

engine = create_engine('sqlite:///data/database/warbot.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


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
            # Insert a Server into the server table
            new_server = Server(id=guild.id, faction="NULL")
            session.merge(new_server)
            session.commit()


client = MyClient()
client.run(open("token.txt", "r").read())
