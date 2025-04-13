from typing import Any, Awaitable, Callable
from abc import ABC, abstractmethod


from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ContextTypes


class BaseBotCommand(ABC):
    def __init__(self, command: str) -> None:
        self.handler = CommandHandler(command, self._callback)

    @staticmethod
    async def _callback(update: Update, callback: ContextTypes.DEFAULT_TYPE):
        pass

    @property
    def GetHandler(self):
        return self.handler
