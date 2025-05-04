import datetime

from BOTmodules import *
from BOTmodules.commands.infocommand import InfoCommand
from BOTmodules.commands.monumentscommands import *
from BOTmodules.configuration import ConfigurationOvermind
from BOTmodules.telegram_interface import TelegramBotInterface

from BOTmodules.commands.regmonumentconverstation import *
TGI = TelegramBotInterface(ConfigurationOvermind().getBotToken())
TGI.AddHandlerToList(InfoCommand().GetHandler())
TGI.AddHandlers(MonumentListCommand().GetHandler())
TGI.AddHandlerToList(RegMonumentConverstation().getHandler())
TGI.AddHandlerToList(MonumentInfoCommand().GetHandler())
TGI.AddHandlers(EditMonumentInfo().GetHandler())
TGI.AddHandlerToList(RandomMonument().GetHandler())
TGI.Run()
