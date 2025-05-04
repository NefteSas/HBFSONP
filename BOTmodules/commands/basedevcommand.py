from typing import override

from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from BOTmodules.configuration import ConfigurationOvermind
from BOTmodules.commands.basebotcommand import BaseBotCommand

class BaseDevCommand(BaseBotCommand):
    def __init__(self, command, has_args=True) -> None:
        super().__init__(command, has_args)

    @override
    async def _callback(self, update: Update, callback: ContextTypes.DEFAULT_TYPE):
        print(f"CHECKING {update.effective_user.id}")
        if (str(update.effective_user.id) in ConfigurationOvermind().getBotDevs()):
            pass
        else:
            await update.message.reply_text("🛑 ВАМ НЕ ДОСТУПНА ДАННАЯ КОМАНДА. ОБРАТИТЕСЬ К СОЗДАТЕЛЮ.")
            raise PermissionError
        