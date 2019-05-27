

class CommandManager:

    coms = []
    prefix = ""

    def add_command(self, command):
        self.coms.append(command)

    def set_prefix(self, prefix):
        self.prefix = prefix
