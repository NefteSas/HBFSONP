from abc import ABC
from telegram import Update
from BOTmodules.commands import *
from BOTmodules.commands.basebotcommand import BaseBotCommand

from telegram.ext import MessageHandler, ContextTypes, filters

class BaseMessageHandler(ABC):
    def __init__(self, filters: filters.BaseFilter):
        self.handler = MessageHandler(filters=filters, callback=self._callback)
        
    async def _callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass
    
    def GetHandler(self) -> MessageHandler:
        return self.handler