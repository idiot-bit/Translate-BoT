import logging
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to start the bot and greet the user
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hi! Send me any Hindi text, and I'll translate it to English using ChatGPT.")

# Function to handle translation using ChatGPT
def translate_to_english(update: Update, context: CallbackContext) -> None:
    hindi_text = update.message.text

    # Use OpenAI's ChatGPT to translate the text
    try:
        response = openai.Completion.create(
            model="gpt-4",  # You can use GPT-3.5 or GPT-4 depending on your access
            prompt=f"Translate the following Hindi text to English:\n\n{hindi_text}",
            temperature=0.5,
            max_tokens=100
        )

        # Get the translation from the response
        translated_text = response.choices[0].text.strip()

        # Send the translated text back to the user
        update.message.reply_text(f"Translated text: {translated_text}")

    except Exception as e:
        update.message.reply_text("Sorry, something went wrong. Please try again later.")
        logger.error(f"Error while translating: {e}")

# Error handler
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Set up the Telegram bot with your token
    updater = Updater("7456531687:AAEq9pNuJgTkdUK3fmzP60vCacisBbU2xl4")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Command handler for the /start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Message handler for translating Hindi text to English
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_to_english))

    # Error handler
    dispatcher.add_error_handler(error)

    # Start polling for messages
    updater.start_polling()

    # Run the bot until you stop it manually
    updater.idle()

if __name__ == '__main__':
    main()
