from typing import override

from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from BOTmodules.commands.basebotcommand import BaseBotCommand

## КОСТЫЛЬ
BOT_NAME = "Эхо Войны"
BOT_DATA = datetime.now()

class InfoCommand(BaseBotCommand):
    def __init__(self) -> None:
        super().__init__("start")

    @override
    async def _callback(self, update: Update, callback: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            f"""
            Привет! {BOT_NAME} - информационный бот, цель которого поддережание памяти о Великой Отечественной Войне через предоставление удобной информации о памятниках!
            \n Если хочешь увидеть список команд - смотри меню (рядом с скрепочкой)
            \nВремя сборки - {str(BOT_DATA)}
            """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("GitHub",url="https://github.com/NefteSas/HBFSONP")]])
            )