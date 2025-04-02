import logging
from google.cloud import translate_v2 as translate
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

# Enable logging for debugging purposes
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Google Translate API client
translate_client = translate.Client()

# Command handler to handle /start command
async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text('Hello! Send me any message in Hindi, and I will translate it to English.')

# Function to translate Hindi to English
async def translate_message(update: Update, context: CallbackContext) -> None:
    """Translate the message received in Hindi to English."""
    try:
        text_to_translate = update.message.text  # The message to be translated
        if text_to_translate.lower() == "/start":
            return  # Ignore the start command as it's handled already.

        # Translate the message from Hindi to English
        translation = translate_client.translate(text_to_translate, target_language='en', source_language='hi')
        translated_text = translation['translatedText']
        
        # Send the translated text back to the user
        await update.message.reply_text(f"Original (Hindi): {text_to_translate}\nTranslated (English): {translated_text}")
    
    except Exception as e:
        logger.error(f"Error while processing message: {str(e)}")
        await update.message.reply_text("Sorry, there was an error processing your request.")

def main() -> None:
    """Start the bot and set up the handlers."""
    TELEGRAM_API_KEY = 'YOUR_TELEGRAM_BOT_API_KEY'  # Replace with your actual token

    # Create the Application and set the bot token
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Add handlers for /start and text messages
    application.add_handler(CommandHandler("start", start))  # /start command handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))  # Text message handler

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
