from telegram.ext import Application, ApplicationBuilder, BaseHandler


class TelegramBotInterface:
    def __init__(self, token: str) -> None:
        self.app: Application = ApplicationBuilder().token(token).build()

    def AddHandlerToList(self, handler: BaseHandler):
        self.app.add_handler(handler)

    def AddHandlers(self, handlers: list[BaseHandler]):
        self.app.add_handlers(handlers)

    def Run(self):
        self.app.run_polling()
