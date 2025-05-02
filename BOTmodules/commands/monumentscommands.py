from typing import override

from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, CallbackQueryHandler, ConversationHandler, CommandHandler, MessageHandler, filters

from BOTmodules import database
from BOTmodules.commands.basebotcommand import BaseBotCommand
from BOTmodules.commands.basedevcommand import BaseDevCommand

INT_TO_SMILICK = ['1️⃣',
'2️⃣',
'3️⃣',
'4️⃣',
'5️⃣',
'6️⃣',
'7️⃣',
'8️⃣',
'9️⃣',
'🔟']
db = database.MonumentsDatabase()

class MonumentListCommand(BaseBotCommand):
    def __init__(self) -> None:
        super().__init__("monums")

    @override
    async def _callback(self, update: Update, callback: ContextTypes.DEFAULT_TYPE):

        string = ""

        
        ids = db.GetIDS()

        for i in ids:
            if (i<=10):
                pass
            else:
                break
            print(i)
            monument: database.Monument = db.ReadMonumentByID(i)
            string += f"{INT_TO_SMILICK[i-1]}: {monument.name} \n"
        
        if (string == ""):
            string = "Увы, никаких памятников пока не добавлено 😔"

        await update.message.reply_text(
            string)
        
class MonumentInfoCommand(BaseBotCommand):
    def __init__(self) -> None:
        super().__init__("monum")

    @override
    async def _callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = context.args 
        monument = None
        if (not context.args):
            await update.message.reply_text(
            "⚠️ Укажите идентефикатор памятника")
            return
        try:
            monument = db.ReadMonumentByID(args[0])
        except FileNotFoundError:
            await update.message.reply_text(
            "⚠️ Памятника с таким идентефикатором не существует")

        keyboard = [
        ]
        if (monument.getURL):
            keyboard.append([InlineKeyboardButton("Подробнее", url=monument.getURL)])
            
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"""
            📇: {monument.name}\n\n🔎: {monument.position_stupid}\n\nℹ️: {monument.description},
            """,
            reply_markup=reply_markup)
        
        await update.message.reply_location(monument.getGPSPosition[0], monument.getGPSPosition[1])

NAME = 1

class CancelDialogCommand(BaseBotCommand):
    def __init__(self, command='cancel', args=None):
        super().__init__(command, args)
    
    @override    
    async def _callback(self, update, callback):
        await update.message.reply_text("🚫 Диалог прерван.", reply_markup=ReplyKeyboardRemove())
        callback.user_data.clear()
        return ConversationHandler.END

class EditMonumentInfo(BaseDevCommand):
    def __init__(self, command="EM", has_args=True):
        super().__init__(command, has_args)
        self.callbackQueryHandler = CallbackQueryHandler(self.button)
        self.handler = CommandHandler(command=command,callback=self._callback)
        self.converstationHandler = ConversationHandler(entry_points=[self.callbackQueryHandler
            ],states={
                NAME: [CallbackQueryHandler(self.__getName)]
            },fallbacks=[CallbackQueryHandler(CancelDialogCommand()._callback)], per_message=True
        )
        
        
    async def __getName(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Z")
        
    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query
        
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        await query.answer("")
        
        if (query.data == "1"):
            print(query.data)
        return NAME
        

            
    async def _callback(self, update, callback):
        await super()._callback(update, callback)
        
        args = callback.args 
        monument = None
        if (not callback.args):
            await update.message.reply_text(
            "⚠️ Укажите идентефикатор памятника")
            return
        try:
            monument = db.ReadMonumentByID(args[0])
        except FileNotFoundError:
            await update.message.reply_text(
            "⚠️ Памятника с таким идентефикатором не существует")
            return
        
        keyboard = [
        [
            InlineKeyboardButton("Название", callback_data="1"),
            InlineKeyboardButton("Описание", callback_data="2"),
            InlineKeyboardButton("Адресс", callback_data="3"),
            InlineKeyboardButton("Геолокацию", callback_data="4")
        ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Че изменить?", reply_markup=reply_markup)
    
    @override
    def GetHandler(self):
        return [self.handler, self.converstationHandler, self.callbackQueryHandler]