from typing import override

from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from BOTmodules.commands.basebotcommand import BaseBotCommand

## КОСТЫЛЬ
BOT_NAME = "131417"
BOT_DATA = datetime.now()

class InfoCommand(BaseBotCommand):
    def __init__(self) -> None:
        super().__init__("info")

    @override
    async def _callback(self, update: Update, callback: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            f"""
            Привет! {BOT_NAME} - информационный бот, цель которого поддережание памяти о Великой Отечественной Войне через предоставление удобной информации о памятниках!
            \nВремя сборки - {str(BOT_DATA)}
            """)