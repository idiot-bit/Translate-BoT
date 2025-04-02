import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

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
async def start(update: Update, context) -> None:
    await update.message.reply_text("Hello! Send me a message in informal Hindi, and I'll translate it to English.")

# Function to handle messages
async def handle_message(update: Update, context) -> None:
    user_message = update.message.text

    if user_message:
        # Translate informal Hindi to English
        translated_text = translate_text(user_message)
        await update.message.reply_text(translated_text)

# Main function to run the bot
def main():
    # Set up the Application and Dispatcher (no 'use_context' argument)
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Command and message handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
