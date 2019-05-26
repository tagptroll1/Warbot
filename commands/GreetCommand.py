from commands.Command import Command


class GreetCommand(Command):

    async def execute(self, message):
        await message.channel.send("Hello!")
        return
