from BOTmodules import *
from BOTmodules.commands.infocommand import InfoCommand
from BOTmodules.configuration import ConfigurationOvermind
from BOTmodules.telegram_interface import TelegramBotInterface

TGI = TelegramBotInterface(ConfigurationOvermind().getBotToken())
TGI.AddHandlerToList(InfoCommand().GetHandler)
TGI.Run()
