import json
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from queue import Queue
from dotenv import load_dotenv
from os import getenv

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hello = '''Hello! This is a bot to help practice the PAO system, a technique for memorizing numbers.

/quiz will return a two-digit number. Then, you have to answer with the three items (Person, Action, Object) relative to the given number.

/learn <number> will return the three items for the provided number.

/mix will give you three two-digit numbers concatenated. You have to answer by providing the Person for the first two-digit number, the Action for the second two-digit number and the Object for the third two-digit number.

Finally, the answers must be given separated by commas: person,action,object
'''
    await update.message.reply_text(hello)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    number = str(random.randint(0, 99)).zfill(2)
    context.user_data["quiz_number"] = number
    await update.message.reply_text(f"Please provide the three items for the number {number}. Separate them with commas.")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    quiz_number = context.user_data.get("quiz_number")
    quiz_numbers = context.user_data.get("mixed_quiz_numbers")

    if not quiz_number and not quiz_numbers:
        await update.message.reply_text("Please use /quiz, /learn or /mix.")
        return

    user_response = update.message.text.split(",")
    if len(user_response) != 3:
        await update.message.reply_text("Please provide exactly three items separated by commas.")
        return

    if quiz_number:
        correct_answers = data.get(quiz_number)
        if list(map(str.lower, user_response)) == list(map(str.lower, correct_answers)):
            await update.message.reply_text("Correct!")
        else:
            await update.message.reply_text(f"Incorrect. The correct answers are: \n\n{'\n'.join(correct_answers)}")
        context.user_data.pop("quiz_number", None)

    if quiz_numbers:
        correct_answers = [data[quiz_numbers[0]][0], data[quiz_numbers[1]][1], data[quiz_numbers[2]][2]]
        if list(map(str.lower, user_response)) == list(map(str.lower, correct_answers)):
            await update.message.reply_text("Correct!")
        else:
            await update.message.reply_text(f"Incorrect. The correct answers are: \n\n{correct_answers[0]}\n{correct_answers[1]}\n{correct_answers[2]}")
        context.user_data.pop("mixed_quiz_numbers", None)

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    number = context.args[0].zfill(2)
    items = data.get(number)
    if items:
        await update.message.reply_text(f"The items for the number {number} are: \n\n{'\n'.join(items)}")
    else:
        await update.message.reply_text(f"No items found for the number {number}.")

async def mixed_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    quiz_numbers = random.sample(list(data.keys()), 3)
    mixed_string = '-'.join(quiz_numbers)
    context.user_data["mixed_quiz_numbers"] = quiz_numbers
    await update.message.reply_text(f"Please provide the items in order for the mixed number {mixed_string}.")

def main() -> None:
    token = getenv('telegram')  # Replace with your Telegram bot token

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # Get the dispatcher to register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("learn", learn))
    application.add_handler(CommandHandler("mix", mixed_quiz))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mixed_answer))


    # Start the Bot
    application.run_polling()

if __name__ == "__main__":
    with open('./pao-100.json', "r") as file:
        data = json.load(file)

    main()
