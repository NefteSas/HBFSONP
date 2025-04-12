from typing import override

from telegram import Update
from telegram.ext import ContextTypes

from BOTmodules.commands.basebotcommand import BaseBotCommand


class InfoCommand(BaseBotCommand):
    def __init__(self) -> None:
        super().__init__("hello")

    @staticmethod
    @override
    async def _callback(update: Update, callback: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Z")
