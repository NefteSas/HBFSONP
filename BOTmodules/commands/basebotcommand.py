from typing import Any, Awaitable, Callable
from abc import ABC, abstractmethod


from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ContextTypes, ConversationHandler


class BaseBotCommand(ABC):
    def __init__(self, command: str, args=None) -> None:
        self.textCommand = command
        self.handler = CommandHandler(command, self._callback, has_args=args)

    async def _callback(self, update: Update, callback: ContextTypes.DEFAULT_TYPE):
        pass

    async def _endConv(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.clear()
        return ConversationHandler.END

    @property
    def commandID(self) -> str:
        return self.textCommand

    def GetHandler(self):
        return self.handler
