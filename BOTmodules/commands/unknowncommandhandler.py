from typing import override
from telegram import Update
from telegram.ext import ContextTypes, filters
from BOTmodules.commands import *
from BOTmodules.commands.basemessagehandler import BaseMessageHandler

class UnknownCommandHandler(BaseMessageHandler):
    def __init__(self):
        super().__init__(filters.COMMAND)
        
    async def _callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super()._callback(update, context)
        await update.message.reply_text(
        f"❌ Неизвестная команда: `{update.message.text}`\n"
        "Используйте меню (рядом с скрепочкой) для списка команд.",
        parse_mode="Markdown"
        )
    