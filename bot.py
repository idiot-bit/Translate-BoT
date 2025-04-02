import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Replace these with your own keys
TELEGRAM_API_KEY = 'YOUR_TELEGRAM_BOT_API_KEY'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

# Function to translate informal Hindi to English using OpenAI GPT model
def translate_text(input_text: str) -> str:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use GPT-4 if available
            prompt=f"Translate this text from informal Hindi to English: {input_text}",
            max_tokens=100,
            temperature=0.3,
        )
        translation = response.choices[0].text.strip()
        return translation
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, there was an error processing your request."

# Command to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me a message in informal Hindi, and I'll translate it to English.")

# Function to handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    if user_message:
        # Translate informal Hindi to English
        translated_text = translate_text(user_message)
        update.message.reply_text(translated_text)

# Main function to run the bot
def main():
    # Set up the Updater and Dispatcher
    updater = Updater(TELEGRAM_API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    # Command and message handler
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
