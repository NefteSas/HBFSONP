from ast import Not
import dis
import math
import queue
import random
import re
from turtle import distance, update
from typing import override
from geopy import distance

from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import telegram
from telegram.ext import ContextTypes, CallbackQueryHandler, ConversationHandler, CommandHandler, MessageHandler, filters

from BOTmodules import database
from BOTmodules.commands.basebotcommand import BaseBotCommand
from BOTmodules.commands.basedevcommand import BaseDevCommand
from BOTmodules.commands.infocommand import InfoCommand

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

    IN_LIST = 5

    def __init__(self) -> None:
        super().__init__("monums")
        self.markuphandler = CallbackQueryHandler(self._queryCallback, pattern="^MONUMS:")

    async def _queryCallback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        context.user_data["listPage"] = context.user_data["listPage"] if "listPage" in context.user_data.keys() else 0
        if (query.data=="MONUMS:1"):
            if (context.user_data["listPage"] + 1 < math.ceil(len(db.GetIDS()) / MonumentListCommand.IN_LIST)):
                context.user_data["listPage"] += 1
            else:
                await query.answer("Конец списка")
                return
            
        elif (query.data == "MONUMS:-1"):
            if (context.user_data["listPage"]>0):
                context.user_data["listPage"]-=1
            else:
                await query.answer("Начало списка")
                return
        
        splitted = query.data.split(':')
        
        if (len(splitted)==3):
            newContext = context
            newContext.args = [splitted[2]] 
            await query.answer()
            await MonumentInfoCommand()._callback(update=update, context=newContext)
            return
        
        v = self.__renderList(context.user_data["listPage"])        
                
        keyboard = [
            [InlineKeyboardButton("⬅️", callback_data="MONUMS:-1"),
            InlineKeyboardButton("➡️", callback_data="MONUMS:1")],
            v[1]
        ]        
        await query.answer()
        await query.edit_message_text(v[0], reply_markup=InlineKeyboardMarkup(keyboard))
        
        
    def __renderList(self, iters: int) -> tuple[str, list]:
        ids = sorted(db.GetIDS())


        keyboard = []
        #print(math.ceil(len(db.GetIDS())/MonumentListCommand.IN_LIST))
        string = f"СТРАНИЦА {iters+1} / {math.ceil(len(db.GetIDS())/MonumentListCommand.IN_LIST)} \n\n"

        for i in ids[((MonumentListCommand.IN_LIST * iters)):]:
            if (i<=MonumentListCommand.IN_LIST + MonumentListCommand.IN_LIST * iters):
                pass
            else:
                break
            monument: database.Monument = db.ReadMonumentByID(i)
            
            k = (i - MonumentListCommand.IN_LIST * iters)-1
            
            string += f"{INT_TO_SMILICK[k]}: {monument.name} \n\n"
            keyboard.append(InlineKeyboardButton(f"{INT_TO_SMILICK[k]}", callback_data=f"MONUMS:ID:{i}"))
        
        
        if (string == ""):
            string = "Увы, никаких памятников пока не добавлено 😔"
        else:
            string+= "Нажми на кнопки ниже, чтобы подробнее узнать о памятниках 😉"
            
        

        return (string, keyboard)

    @override
    async def _callback(self, update: Update, callback: ContextTypes.DEFAULT_TYPE):
        callback.user_data.clear()
        try:
            callback.user_data["listPage"] = callback.user_data["listPage"] if callback.user_data["listPage"] is not None else 0
        except KeyError:
            callback.user_data["listPage"] = 0

        renderetTuple = self.__renderList(0)
        string = renderetTuple[0]

        keyboard = [
            [InlineKeyboardButton("⬅️", callback_data="MONUMS:-1"),
            InlineKeyboardButton("➡️", callback_data="MONUMS:1")],
            renderetTuple[1]
        ]
        await update.message.reply_text(
            string,
            reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    @override
    def GetHandler(self):
        return [self.handler, self.markuphandler]
        
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
        
        message = update.message if update.message is not None else update.callback_query.message
        
        await message.reply_text(
            f"""
            📇: {monument.name}\n\n🔎: {monument.position_stupid}\n\nℹ️: {monument.description},
            """,
            reply_markup=reply_markup)
        
        await message.reply_location(monument.getGPSPosition[0], monument.getGPSPosition[1])
        

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
    START, NAME, DESCRITPTION = range(3)

    def __init__(self, command="EM", has_args=True):
        self.conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(callback=self._startEditing, pattern=r"monument:\d:\d")
        ],
        states={
            EditMonumentInfo.NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self._get_name)],
            EditMonumentInfo.DESCRITPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self._get_desc)]
        },
        fallbacks=[CancelDialogCommand().GetHandler()]
    )
        self.comm_handler = CommandHandler("EM", self.__command_callback)
        super().__init__(command, has_args)

    async def __command_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await super()._callback(update, context)

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
            return

        # Создаем кнопку для запуска диалога
        keyboard = [
            [InlineKeyboardButton("Имя", callback_data=f"monument:{args[0]}:1")],
            [InlineKeyboardButton("Описание", callback_data=f"monument:{args[0]}:2")],
            [InlineKeyboardButton("Геолокацию", callback_data=f"monument:{args[0]}:3")],
            [InlineKeyboardButton("Адресс", callback_data=f"monument:{args[0]}:4")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Нажмите кнопку, чтобы начать изменение определенного параметра",
            reply_markup=reply_markup
        )

    # Обработчик нажатия кнопки
    async def _startEditing(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        query_data = query.data.split(':')
        print(query_data[2]=="1")
        context.user_data["ID"] = query_data[1]
        if (query_data[2]=="1"):
            await query.edit_message_text("Введите новое имя памятника:")
            return EditMonumentInfo.NAME
        elif (query_data[2]=="2"):
            await query.edit_message_text("Введите новое описание памятника:")
            return EditMonumentInfo.DESCRITPTION
        
    async def _get_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            database.MonumentsDatabase().UpdateMonumentSaveByID(context.user_data["ID"], name=update.message.text)
        except FileExistsError:
            await update.message.reply_text("❌ обновление не удалось")
        await update.message.reply_text("✅ данные обновлены")
        return await self._endConv(update, context)

    async def _get_desc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            database.MonumentsDatabase().UpdateMonumentSaveByID(context.user_data["ID"], desc=update.message.text)
        except FileExistsError:
            await update.message.reply_text("❌ обновление не удалось")
        await update.message.reply_text("✅ данные обновлены")
        return await self._endConv(update, context)
    
    @override
    def GetHandler(self):
        return [self.conv_handler, self.comm_handler]
    
class RandomMonument(BaseBotCommand):
    def __init__(self, command="rand", args=None):
        super().__init__(command, args)
        
    async def _callback(self, update, callback):
        ids = db.GetIDS()
        callbackG = callback
        callbackG.args = [random.randint(0, len(db.GetIDS()))]
        await MonumentInfoCommand()._callback(update, callbackG)
        
class MonumentsByLocation(BaseBotCommand):
    MAX_DEPTH_LEVEL = 5
    GET_LOCATION_STATE = 1
    
    def __init__(self, args=None):
        self.dialogHandler = ConversationHandler(
            entry_points=[CommandHandler('locate', self._callback)], states={
                MonumentsByLocation.GET_LOCATION_STATE: [MessageHandler(filters.TEXT | filters.LOCATION, self.__getMonument)]
            }, fallbacks=[
                CancelDialogCommand().GetHandler()
            ]
        )
        self.queryhandler = CallbackQueryHandler(self._callback_query,pattern="^LOCATE:")
        
    async def _callback_query(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        newContext = context
        newContext.args = [query.data.split(":")[1]] 
        await query.answer()
        await MonumentInfoCommand()._callback(update=update, context=newContext)      
        
    async def _callback(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        #await super()._callback(update, context)
        await update.message.reply_text("🗺 Привет, чтобы получить список ближайших памятников отправь свою геолокацию ☺️ (нажми на скрепочку)")
        return MonumentsByLocation.GET_LOCATION_STATE
    
        
    async def __getMonument(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if (update.message.location is None):
            await update.message.reply_text("⚠️ Ожидалась геолокация. Если хочешь отменить, пропиши /cancel")
            return MonumentsByLocation.GET_LOCATION_STATE
        else:
            #await update.message.reply_text("update.message.location")
            list_by_distance = self.__getNearestList(update.message.location)
                
            string = "🔎Список памятников по расстоянию \n\n"
            keyboard = [[]]
            k=0
            for i in list_by_distance.keys():
                k+=1
                if (k>5):
                    break
                monument = db.ReadMonumentByID(i)
                string += f"{INT_TO_SMILICK[k-1]} | {monument.name} | {math.floor(list_by_distance[i])}м \n\n"
                keyboard[0].append(InlineKeyboardButton(f"{INT_TO_SMILICK[k-1]}", callback_data=f"LOCATE:{i}"))             
            print(keyboard)
            await update.message.reply_text(string, reply_markup=InlineKeyboardMarkup(keyboard))
            context.user_data.clear()
            return ConversationHandler.END
    

         
    def __getNearestList(self, location: telegram.Location) -> dict[int: float]:
        ids = sorted(db.GetIDS())
        id_distance = {}
        for id in ids:
            id_distance[id] = self.__calculateDistance(location, db.ReadMonumentByID(id=id))
            
        
        id_distance = dict(sorted(id_distance.items(), key=lambda item: item[1]))
        return id_distance
    
    
    def __calculateDistance(self, location: telegram.Location, monument: database.Monument) -> float:
        return distance.distance((location.latitude, location.longitude), monument.getGPSPosition).m
        
    @override
    def GetHandler(self):
        return [self.dialogHandler, self.queryhandler]
        