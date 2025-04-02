import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai

# Get API keys from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
telegram_token = os.getenv('TELEGRAM_API_TOKEN')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Send me a message in Hindi and I will translate it to English.')

# Function to handle messages
async def translate(update: Update, context: CallbackContext) -> None:
    hindi_text = update.message.text
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Translate the following Hindi text to English: {hindi_text}",
        temperature=0.5,
        max_tokens=100
    )
    english_translation = response.choices[0].text.strip()
    await update.message.reply_text(f"Translation: {english_translation}")

# Main function to set up the bot
def main():
    application = Application.builder().token(telegram_token).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Register message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()