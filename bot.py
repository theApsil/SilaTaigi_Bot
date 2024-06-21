from config import ADMIN_ID, BOT_TOKEN, msg
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
from db import init_db, update_user_bonus, get_user_bonus, reset_user_bonus, add_user, get_all_users

CHAT_DATA = {}


# Генерация кода
def generate_code():
    return random.randint(1000, 9999)


# Стартовое сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    add_user(user_id)
    print(f"log: starting for USER [{user_id}]")
    keyboard = [
        [KeyboardButton("Сгенерировать код услуги")],
        [KeyboardButton("Проверить бонусы")],
        [KeyboardButton("Сгенерировать код подарка")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

    await update.message.reply_text(
        "Здравствуйте, дорогие гости! С помощью этого бота вы сможете копить баллы и получать подарки от вашей любимой «Силы Тайги»💚\n"
        "За помощью обращайтесь к администратору и получайте бонусы за каждое посещение!",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "/start - Начать взаимодействие с ботом\n"
        "/help - Показать список доступных команд\n"
        "Сгенерировать код услуги - Сгенерировать код для получения услуги\n"
        "Проверить бонусы - Проверить количество накопленных бонусов\n"
        "Сгенерировать код подарка - Сгенерировать код для получения подарка"
    )
    await update.message.reply_text(help_text)


# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "Сгенерировать код услуги":
        await generate_service_code(update, context)
    elif text == "Проверить бонусы":
        await check_bonuses(update, context)
    elif text == "Сгенерировать код подарка":
        await generate_gift_code(update, context)


# Обработка команды "сгенерировать код услуги"
async def generate_service_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    code = generate_code()
    CHAT_DATA[code] = {'user_id': user_id, 'action': 'service'}
    print(f"log: generate service code for USER [{CHAT_DATA[code]['user_id']}")
    await update.message.reply_text(f"Ваш код услуги: {code}")
    for item in ADMIN_ID:
        await context.bot.send_message(chat_id=item, text=f"Пользователь {user_id} запросил код услуги: {code}")


# Обработка команды подтверждения кода администратором
async def confirm_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat_id not in ADMIN_ID:
        await update.message.reply_text("Только администратор может подтверждать коды.")
        return

    try:
        code = int(update.message.text.split()[1])
    except (IndexError, ValueError):
        await update.message.reply_text("Используйте формат: /confirm <code>")
        return
    print(f"log: confirming from ADMIN [{update.message.chat_id}]\n"
          f"for USER [{CHAT_DATA[code]['user_id']}] CODE [{code}]")
    if code in CHAT_DATA and CHAT_DATA[code]['action'] == 'service':
        user_id = CHAT_DATA[code]['user_id']
        bonus_count = update_user_bonus(user_id)
        await context.bot.send_message(chat_id=user_id, text=f"Вам зачислен бонус {bonus_count} / 8")
        for admin_id in ADMIN_ID:
            await context.bot.send_message(chat_id=admin_id, text="Код успешно подтверждён")

        del CHAT_DATA[code]


# Проверка бонусов
async def check_bonuses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    bonus_count = get_user_bonus(user_id)
    print(f"log: check bonus USER [{user_id}]")

    await update.message.reply_text(f"Количество ваших бонусов: {bonus_count} / 8")


# Генерация кода подарка
async def generate_gift_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    bonus_count = get_user_bonus(user_id)

    if bonus_count < 8:
        await update.message.reply_text(
            f"К сожалению, у вас нет достаточного количества бонусов. \nВозвращайтесь как только накопите 8 бонусов. "
            f"\nКоличество ваших бонусов сейчас: {bonus_count}.")
    else:
        code = generate_code()
        CHAT_DATA[code] = {'user_id': user_id, 'action': 'gift'}

        await update.message.reply_text(f"Ваш код подарка: {code}")
        for item in ADMIN_ID:
            await context.bot.send_message(chat_id=item, text=f"Пользователь {user_id} запросил код подарка: {code}")


# Обработка подтверждения кода подарка администратором
async def confirm_gift_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat_id not in ADMIN_ID:
        await update.message.reply_text("Только администратор может подтверждать коды.")
        return

    try:
        code = int(update.message.text.split()[1])
    except (IndexError, ValueError):
        await update.message.reply_text("Используйте формат: /confirmgift <code>")
        return

    if code in CHAT_DATA and CHAT_DATA[code]['action'] == 'gift':
        user_id = CHAT_DATA[code]['user_id']
        reset_user_bonus(user_id)

        gifts = [
            "Спортивный массаж (30 мин)",
            "Антицеллюлитный (30 мин)",
            "Шоколадное обертывание",
            "Фруктово-ягодное обертывание",
            "Скидка на следующее посещение 20%",
            "Скидка на следующее посещение 30%",
            "Скидка на следующее посещение 40%",
            "Скидка на следующее посещение 50%",
        ]
        gift = random.choice(gifts)

        await context.bot.send_message(chat_id=user_id, text=f"🎁🎁🎁\nУ вас накопился 1 подарок! Ваш подарок: {gift}")
        for admin_id in ADMIN_ID:
            await context.bot.send_message(chat_id=admin_id, text="Код подарка успешно подтверждён")

        del context.chat_data[code]


# Команда для администраторов
async def admin_instructions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat_id not in ADMIN_ID:
        await update.message.reply_text("Эта команда доступна только администраторам.")
        return

    instructions = (
        "Инструкции для администратора:\n\n"
        "1. Когда пользователь запрашивает код услуги, администратор получает сообщение от бота с этим кодом.\n"
        "2. Для подтверждения кода услуги администратор вводит команду в чат с ботом: `/confirm <code>`, заменяя <code> на фактический код.\n"
        "3. Когда пользователь запрашивает код подарка, администратор также получает сообщение от бота с этим кодом.\n"
        "4. Для подтверждения кода подарка администратор вводит команду в чат с ботом: `/confirmgift <code>`, заменяя <code> на фактический код."
    )
    await update.message.reply_text(instructions)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Неизвестная команда. Используйте /help для получения списка доступных команд.")


async def broadcast_fixed_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    users = get_all_users()
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=msg)
        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю с ID {user_id}: {e}")


# Команда /broadcast
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat_id in ADMIN_ID:
        await broadcast_fixed_message(context)
        await update.message.reply_text("Сообщение успешно отправлено всем пользователям.")
    else:
        await update.message.reply_text("У вас нет прав для использования этой команды.")


def main() -> None:
    init_db()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("admin", admin_instructions))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("confirm", confirm_code))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("confirmgift", confirm_gift_code))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    application.run_polling()


if __name__ == '__main__':
    main()
