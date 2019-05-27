from sqlalchemy.orm import sessionmaker
from database.DiscordDatabase import *
from discord.ext import commands
import discord
from sqlalchemy import exists

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
        new_server = Server(id=guild.id)
        session.merge(new_server)
        session.commit()


@client.event
async def on_member_join(ctx):
    server = session.query(Server).filter_by(id=ctx.guild.id).one()
    ret = session.query(exists().where(User.id == ctx.member.id)).scalar()

    if ret:
        print("A valid civible member has joined!")
        user = session.query(User).filter_by(id=ctx.member.id).one()

        if user.faction == "terran":
            server.terran += 1
        elif user.faction == "protoss":
            server.protoss += 1
        elif user.faction == "zerg":
            server.zerg += 1

    else:
        print("Joining member does not play civible!")


@client.event
async def on_member_leave(ctx):
    server = session.query(Server).filter_by(id=ctx.guild.id).one()
    ret = session.query(exists().where(User.id == ctx.member.id)).scalar()

    if ret:
        print("A valid civible member has left!")
        user = session.query(User).filter_by(id=ctx.member.id).one()

        if user.faction == "terran":
            server.terran -= 1
        elif user.faction == "protoss":
            server.protoss -= 1
        elif user.faction == "zerg":
            server.zerg -= 1

    else:
        print("Leaving member does not play civible!")


@client.command()
async def join(ctx):
    server = session.query(Server).filter_by(id=ctx.guild.id).one()
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
        # TODO: Ensure that the user has entered a valid faction name prior to doing work
        # Check ahead of time if the user is already in a faction.
        ret = session.query(exists().where(User.id == ctx.message.author.id)).scalar()

        if ret:
            user = session.query(User).filter_by(id=ctx.message.author.id).one()

            if user.faction == "terran":
                if server.terran > 0:
                    server.terran -= 1
            elif user.faction == "protoss":
                if server.protoss > 0:
                    server.protoss -= 1
            elif user.faction == "zerg":
                if server.zerg > 0:
                    server.zerg -= 1

        fac = ctx.message.content.split(" ")[1].lower()
        user = User(id=ctx.message.author.id, faction=fac)
        session.merge(user)
        session.commit()

        if fac == "terran":
            session.merge(Terran(id=ctx.message.author.id))
            server.terran += 1
            session.commit()
            await ctx.channel.send("You have successfully joined the Terran!")

        elif fac == "protoss":
            session.merge(Protoss(id=ctx.message.author.id))
            server.protoss += 1
            session.commit()
            await ctx.channel.send("You have successfully joined the Protoss!")

        elif fac == "zerg":
            session.merge(Zerg(id=ctx.message.author.id))
            server.zerg += 1
            session.commit()
            await ctx.channel.send("You have successfully joined the Zerg!")

    return


@client.command()
async def info(ctx):
    user = session.query(User).filter_by(id=ctx.message.author.id).one()

    user_faction = user.faction

    print(user_faction)
    if user_faction == "terran":
        terran = session.query(Terran).filter_by(id=ctx.message.author.id).one()

        emb = discord.Embed(
            title="Terran",
            color=discord.Color.blue()
        )

        emb.add_field(name="ID", value=str(ctx.message.author.id), inline=False)
        emb.add_field(name="Minerals", value=str(terran.minerals), inline=True)
        emb.add_field(name="Vespene", value=str(terran.vespene), inline=True)
        await ctx.send(embed=emb)

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

    if user_faction == "zerg":
        zerg = session.query(Zerg).filter_by(id=ctx.message.author.id).one()

        emb = discord.Embed(
            title="Zerg",
            color=discord.Color.purple()
        )

        emb.add_field(name="ID", value=str(ctx.message.author.id), inline=False)
        emb.add_field(name="Minerals", value=str(zerg.minerals), inline=True)
        emb.add_field(name="Vespene", value=str(zerg.vespene), inline=True)
        await ctx.send(embed=emb)
    return


@client.command()
async def scout(ctx):
    server = session.query(Server).filter_by(id=ctx.guild.id).one()

    controlling_faction = server.faction

    user = session.query(User).filter_by(id=ctx.message.author.id).one()

    user_faction = user.faction

    if controlling_faction.lower() == "null":
        await ctx.send("This server is not yet controlled by any known factions. Would you like to claim it? (yes/no)")

        def yes(m):
            return m.content == 'yes' and m.channel == ctx.channel

        await client.wait_for('message', check=yes)
        server.faction = user_faction
        server.claimer = ctx.message.author.id
        session.commit()
        await ctx.send("This server has now been claimed by the {}!".format(user_faction))

        # def no(m):
        #     return m.content == 'no' and m.channel == ctx.channel
        #
        # await client.wait_for('message', check=no)
        # await ctx.send("The {} have chosen to let this server be.".format(user_faction))

    else:
        await ctx.send("This server is currently controlled by the " + controlling_faction + "!")
    return


client.run(open("token.txt", "r").read())
