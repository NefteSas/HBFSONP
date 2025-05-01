from typing import override

from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from BOTmodules import database
from BOTmodules.commands.basebotcommand import BaseBotCommand

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