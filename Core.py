import discord

from commands.CommandManager import CommandManager
from commands.GreetCommand import GreetCommand
from commands.JoinCommand import JoinCommand
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.DiscordDatabase import Server


class MyClient(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.Base = declarative_base()

        self.commandManager = CommandManager()

        self.commandManager.addCommand(GreetCommand("greet", self))
        self.commandManager.addCommand(JoinCommand("join", self))

        self.commandManager.setPrefix("!")

        self.engine = create_engine('sqlite:///data/database/warbot.db')

        self.Base.metadata.bind = self.engine

        DBSession = sessionmaker(bind=self.engine)

        self.session = DBSession()


    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        for command in self.commandManager.coms:
            if message.content.startswith(self.commandManager.prefix + command.name):
                await command.execute(message)

    async def on_ready(self):

        for guild in client.guilds:
            print(guild.name)
            # Insert a Server into the server table
            new_server = Server(id=guild.id, faction="NULL")
            self.session.merge(new_server)
            self.session.commit()


client = MyClient()
client.run(open("token.txt", "r").read())
