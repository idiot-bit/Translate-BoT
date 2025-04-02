import openai
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI API Key and Telegram Token
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure to set this in your environment variables
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")  # Set this environment variable

# Command handler for /start command
async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hello! I am your translation bot. Send me a text, and I will translate it.")

# Function to translate text using OpenAI API
async def translate(update: Update, context: CallbackContext) -> None:
    """Translate text using OpenAI API."""
    user_input = update.message.text
    try:
        # Sending request to OpenAI API (You can modify the prompt as needed)
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # Or use "gpt-4" if available
            prompt=f"Translate the following text to English: {user_input}",
            max_tokens=100
        )

        # Send the translation result
        translated_text = response.choices[0].text.strip()
        await update.message.reply_text(f"Translated Text: {translated_text}")
    
    except openai.error.OpenAIError as e:
        await update.message.reply_text(f"Error occurred while translating: {str(e)}")

# Function to echo messages
async def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

def main():
    """Start the bot and set up handlers."""
    # Set up the application with the provided bot token
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Message handler to handle text messages (for translation)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

    # Add handler for echoing messages if no translation is needed
    application.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, echo))

    # Run the bot with polling
    application.run_polling()

if __name__ == "__main__":
    main()
