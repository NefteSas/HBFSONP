from BOTmodules.commands.basebotcommand import BaseBotCommand


class BaseCommandAssociation:
    def __init__(self, commands: list[BaseBotCommand] = []) -> None:
        self.commands = commands

    @property
    def GetCommandsToLoad(self) -> list[BaseBotCommand]:
        return self.commands
    