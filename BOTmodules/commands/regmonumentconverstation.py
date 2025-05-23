from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from BOTmodules import database
from BOTmodules.commands import *
from BOTmodules.commands.basedevcommand import BaseDevCommand
from BOTmodules.commands.monumentscommands import CancelDialogCommand
from BOTmodules.telegram_interface import TelegramBotInterface

DESCRITPTION,GETSTUPIDPOIS,ASKPOS,GETGPSPOS,IMG,URL,CONFIRM = 1,2,3,4,5,6,7

class RegMonumentCommand(BaseDevCommand):
    def __init__(self, command, has_args=True):
        super().__init__("RM", None)
        
    async def _callback(self, update, callback):
        await super()._callback(update, callback)
        await update.message.reply_text("Название памятника пожалуйста")
        return DESCRITPTION
        

class RegMonumentConverstation():
    def __init__(self):
        self.conv_handler: ConversationHandler = ConversationHandler(
        entry_points=[RegMonumentCommand("RM", None).GetHandler()],  # Господь, прости меня за это
        states={
            DESCRITPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.__getMonumentDescription)],
            GETSTUPIDPOIS: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.__getMonumentLocation)],
            URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.__getURL)],
            ASKPOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.__AskMonumentGeoLocation)],
            GETGPSPOS: [MessageHandler(filters.LOCATION | filters.TEXT, self.__GetMonumentGeoLocation)],
            CONFIRM: [MessageHandler(filters.LOCATION | filters.TEXT & ~filters.COMMAND, self.__confrimData)],
            IMG: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.__getMonumentImg)]
        },
        fallbacks=[CancelDialogCommand().GetHandler()],  # Отмена
    ) 
    
    async def __getMonumentDescription(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["name"] = update.message.text
        await update.message.reply_text("Отлично, добавь описание")
        return GETSTUPIDPOIS

    async def __getMonumentLocation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["description"] = update.message.text
        await update.message.reply_text("Теперь URL адрес изображения. Если без него, пиши '-'")
        return IMG #IMG
    
    async def __getMonumentImg(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text != "-":
            if not TelegramBotInterface.is_url(update.message.text):
                await update.message.reply_text("⚠️ Ожидалась ссылка. Повторите. Если без него, пиши '-'")
                return IMG
            context.user_data["IMG"] = update.message.text
        else:
            context.user_data["IMG"] = None
            
        await update.message.reply_text("Теперь URL адрес. Если без него, пиши '-'")
        return URL
    
    async def __getURL(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text != "-":
            if not TelegramBotInterface.is_url(update.message.text):
                await update.message.reply_text("⚠️ Ожидалась ссылка. Повторите. Если без него, пиши '-'")
                return URL
            context.user_data["URL"] = update.message.text
        else:
            context.user_data["URL"] = None
        
        
        await update.message.reply_text("Теперь адрес")
        return ASKPOS
    
    async def __AskMonumentGeoLocation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["address"] = update.message.text
        await update.message.reply_text(
            "Теперь приложи геолокацию (нажми на скрепку → 'Геопозиция'). Или: широта долгота",
            reply_markup=ReplyKeyboardRemove()
        )
        return GETGPSPOS
    
    async def __GetMonumentGeoLocation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if (update.message.location is not None):
            location = update.message.location
            context.user_data["latitude"] = location.latitude
            context.user_data["longitude"] = location.longitude
        else:
            location = update.message.text.split(" ")
            if (len(location) != 2):
                await update.message.reply_text("⚠️ Ошибка форматирования геопозиции. Повторите попыку. Например: 5 5. __ЧЕРЕЗ ПРОБЕЛ__")
                return GETGPSPOS
            
            context.user_data["latitude"] = location[0]
            context.user_data["longitude"] = location[1]

        
        
        # Создаем клавиатуру для подтверждения
        reply_keyboard = [["Да", "Нет"]]
        
        await update.message.reply_text(
            "Подтверждаете данные?\n"
            f"Название: {context.user_data['name']}\n"
            f"Описание: {context.user_data['description']}\n"
            f"URL: {context.user_data['URL']}\n"
            f'IMG: {context.user_data['IMG']}\n'
            f"Адрес: {context.user_data['address']}\n"
            f"Координаты: Широта: {context.user_data["latitude"]}, Долгота: {context.user_data["longitude"]}",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, 
                one_time_keyboard=True,
                input_field_placeholder="Да/Нет"
            )
        )
        return CONFIRM
    
    async def __confrimData(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == "Да":
            DB = database.MonumentsDatabase()
            DB.CreateMonumentFile(
                database.Monument(DB.GetUniqueID(),
                                  _name=context.user_data['name'],
                                  _description=context.user_data['description'],
                                  _position_stupid=context.user_data['address'],
                                  _GPSPosition=(context.user_data["latitude"], context.user_data["longitude"]),
                                  _url = context.user_data["URL"],
                                  _img = context.user_data["IMG"])
                )

            await update.message.reply_text(
                "✅ Данные сохранены!",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await update.message.reply_text(
                "❌ Регистрация отменена",
                reply_markup=ReplyKeyboardRemove()
            )
        
        context.user_data.clear()
        return ConversationHandler.END

    async def __cancel_dialog(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🚫 Диалог прерван.", reply_markup=ReplyKeyboardRemove())
        context.user_data.clear()
        return ConversationHandler.END
    
    def getHandler(self) -> ConversationHandler:
        return self.conv_handler