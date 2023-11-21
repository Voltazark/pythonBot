import os
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Замените 'YOUR_TOKEN' на токен вашего бота
TOKEN = '6975544850:AAGlxGp9FNOo2134OxV3Q_mKUlMujedAuvs'

# Списки с именами
names_list_1 = ["Ace", "Amaru", "Ash", "Blackbeard", "Blitz", "Buck",
                "Capitão", "Dokkaebi", "Finka", "Flores", "Fuze", "Glaz",
                "Gridlock", "Hibana", "Iana", "IQ", "Jackal", "Kali",
                "Lion", "Maverick", "Montagne", "Nomad", "Nøkk", "Osa",
                "Sledge", "Thatcher", "Thermite", "Twitch", "Ying", "Zero",
                "Zofia", "Thorn", "RAM"]
names_list_2 = ["Smoke", "Mute", "Castle", "Pulse", "Doc", "Rook",
                "Seva buy SSD", "Kapkan", "Tachanka", "Jäger", "Bandit", "Frost",
                "Valkyrie", "Caveira", "Echo", "Lesion", "Ela", "Vigil",
                "Maestro", "Alibi", "Clash", "Kaid", "Mozzie", "Warden",
                "Goyo", "Wamai", "Oryx", "Melusi", "Aruni", "Thunderbird",
                "Thorn", "Azami", "Sens", "Grim", "Solis", "Brava", "Fenrir"]

# Папка с изображениями
images_folder = "images"

# Словарь для отслеживания выбранного имени по пользователю
selected_names = {}

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("Атака", callback_data='random_name_1'),
            InlineKeyboardButton("Защита", callback_data='random_name_2')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.message.reply_html(
        fr"Привет {user.mention_html()}!",
        reply_markup=reply_markup,
    )
    context.user_data['message_id'] = message.message_id

# Функция для обработки нажатия на кнопку
def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    selected_name = ""

    if query.data == 'random_name_1':
        selected_name = random.choice(names_list_1)
    elif query.data == 'random_name_2':
        selected_name = random.choice(names_list_2)

    # Сохраняем выбранное имя для пользователя
    user_id = query.from_user.id
    selected_names[user_id] = selected_name

    # Отправляем новый список кнопок, заменяя старый
    new_keyboard = [
        [
            InlineKeyboardButton("Атака", callback_data='random_name_1'),
            InlineKeyboardButton("Защита", callback_data='random_name_2')
        ]
    ]
    new_reply_markup = InlineKeyboardMarkup(new_keyboard)

    # Отправляем фотографию вместе с именем, если она существует
    image_path = os.path.join(images_folder, f"{selected_name}.jpg")
    if os.path.exists(image_path):
        with open(image_path, 'rb') as photo:
            update.callback_query.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=photo,
                caption=f"Выбран оперативник: {selected_name}\nПродолжайте выбирать:",
                reply_markup=new_reply_markup
            )
    else:
        # Если изображение отсутствует, отправляем только текст
        query.edit_message_text(
            text=f"Выбран оперативник: {selected_name}\nПродолжайте выбирать:",
            reply_markup=new_reply_markup
        )

# Функция для обработки команды /exit
def exit_bot(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Бот завершает работу.")
    context.bot.stop()

# Основная функция
def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("exit", exit_bot))
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

















