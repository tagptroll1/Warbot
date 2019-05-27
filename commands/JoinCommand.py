from commands.Command import Command
from database.DiscordDatabase import User


class JoinCommand(Command):

    async def execute(self, message):
        if len(message.content.split(" ")) == 1:
            await message.channel.send(
                "Want to join a faction? Type ``!join FACTION_NAME`` to join a faction.\nCurrent "
                "factions are:\n\n"
                "- United Nations Space Command\n"
                "- Covenant\n"
                "- Flood\n"
                "- Marines\n"
                "- Yautja\n"
                "- Xenomorphs\n"
                "- Terran\n"
                "- Protoss\n"
                "- Zerg\n")
        elif len(message.content.split(" ")) == 2:
            user = User(id=message.author.id, faction=message.content.split(" ")[1])
            await message.channel.send(
                "You have successfully joined the " + message.content.split(" ")[1] + "!"
            )
            self.client.session.merge(user)
            self.client.session.commit()
        return
