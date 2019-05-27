from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from database.DiscordDatabase import *
from discord.ext import commands
import discord

Base = declarative_base()
engine = create_engine('sqlite:///data/database/warbot.db')
conn = engine.connect()
Base.metadata.bind = engine
db_session = sessionmaker(bind=engine)
session = db_session()

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    for guild in client.guilds:
        print(guild.name)
        # Insert a Server into the server table
        new_server = Server(id=guild.id, faction="NULL")
        session.merge(new_server)
        session.commit()


@client.command()
async def join(ctx):
    if len(ctx.message.content.split(" ")) == 1:
        await ctx.channel.send(
            "Want to join a faction? Type ``!join FACTION_NAME`` to join a faction.\nCurrent "
            "factions are:\n\n"
            "- UNSC\n"
            "- Covenant\n"
            "- Flood\n"
            "- Marines\n"
            "- Yautja\n"
            "- Xenomorphs\n"
            "- Terran\n"
            "- Protoss\n"
            "- Zerg\n")

    elif len(ctx.message.content.split(" ")) == 2:
        fac = ctx.message.content.split(" ")[1].lower()
        user = User(id=ctx.message.author.id, faction=fac)
        session.merge(user)
        session.commit()

        if fac == "protoss":
            session.merge(Protoss(id=ctx.message.author.id))
            session.commit()
            await ctx.channel.send("You have successfully joined the Protoss!")

    return


@client.command()
async def info(ctx):
    user = session.query(User).filter_by(id=ctx.message.author.id).one()

    user_faction = user.faction

    print(user_faction)
    if user_faction == "protoss":
        protoss = session.query(Protoss).filter_by(id=ctx.message.author.id).one()

        emb = discord.Embed(
            title="Protoss",
            color=discord.Color.gold()
        )

        emb.add_field(name="ID", value=str(ctx.message.author.id), inline=False)
        emb.add_field(name="Minerals", value=str(protoss.minerals), inline=True)
        emb.add_field(name="Vespene", value=str(protoss.vespene), inline=True)
        await ctx.send(embed=emb)
    return

@client.command()
async def scout(ctx):
    server = session.query(Server).filter_by(id=ctx.guild.id).one()

    controlling_faction = server.faction

    user = session.query(User).filter_by(id=ctx.message.author.id).one()

    user_faction = user.faction

    if controlling_faction == "null":
        await ctx.send("This server is not yet controlled by any known factions. Would you like to claim it? (yes/no)")

        def yes(m):
            return m.content == 'yes' and m.channel == ctx.channel

        await client.wait_for('message', check=yes)
        server.faction = user_faction
        session.commit()
        await ctx.send("This server has now been claimed by the {}!".format(user_faction))

        def no(m):
            return m.content == 'no' and m.channel == ctx.channel

        await client.wait_for('message', check=no)
        await ctx.send("The {} have chosen to let this server be.".format(user_faction))

    else:
        await ctx.send("This server is currently controlled by the " + controlling_faction + "!")
    return

client.run(open("token.txt", "r").read())
