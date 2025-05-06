from mailbox import FormatError
import re
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, BaseHandler, ContextTypes

class TelegramBotInterface:
    def __init__(self, token: str) -> None:
        self.app: Application = ApplicationBuilder().token(token).build()

    def AddHandlerToList(self, handler: BaseHandler):
        self.app.add_handler(handler)

    def getApplication(self) -> Application:
        return self.app

    def AddHandlers(self, handlers: list[BaseHandler]):
        self.app.add_handlers(handlers)

    def Run(self):
        print('BOT STARTING')
        self.app.run_polling()

    @staticmethod
    async def sendPhoto(url: str, update: Update, callback: ContextTypes.DEFAULT_TYPE):
        
        if not TelegramBotInterface.is_url(url):
            raise FormatError
        
        await callback.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=url
            )
        
    @staticmethod
    def is_url(text: str) -> bool:
        pattern = re.compile(
            r"^https?://"  # http:// или https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # Домен
            r"localhost|"  # Локальный хост
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # IPv4
            r"(?::\d+)?"  # Порт (опционально)
            r"(?:/?|[/?]\S+)$", 
            re.IGNORECASE
        )
        return re.match(pattern, text) is not None