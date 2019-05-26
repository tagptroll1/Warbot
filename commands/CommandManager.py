

class CommandManager:

    coms = []
    prefix = ""

    def addCommand(self, command):
        self.coms.append(command)

    def setPrefix(self, prefix):
        self.prefix = prefix
