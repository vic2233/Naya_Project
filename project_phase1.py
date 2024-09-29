import telebot
import http.client
import json
import os
from import_plot import generate_plot 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
#from api_stock import print_indexes  # Ensure this imports the function

# Get Token from bot Father
test1_token = 'mytoken'
bot = telebot.TeleBot(test1_token)

# Store user inputs in a dictionary
user_data = {}

# Handle the /start command
@bot.message_handler(commands=['start', 'help'])

def send_welcome(message):
    bot.reply_to(message, "Welcome! Please enter the stock symbol you want to analyze.")
    user_data[message.chat.id] = {}  # Initialize a dictionary for this user

# Step 2: Handle the stock symbol input
@bot.message_handler(func=lambda message: message.chat.id in user_data and 'symbol' not in user_data[message.chat.id])
def handle_symbol(message):
    symbol = message.text.upper()  # Convert the symbol to uppercase
    user_data[message.chat.id]['symbol'] = symbol

    keyboard = InlineKeyboardMarkup()
    periods = [30, 60, 90, 180]
    for period in periods:
        button = InlineKeyboardButton(text=f"{period} days", callback_data=f"period_{period}")
        keyboard.add(button)

    bot.send_message(message.chat.id, "Please choose a period for the data:", reply_markup=keyboard)

# Handle callback queries
@bot.callback_query_handler(func=lambda call: call.data.startswith('period_'))
def handle_query(call):
    period_days = int(call.data.split('_')[1])
    chat_id = call.message.chat.id
    symbol = user_data[chat_id]['symbol']

    try:
        # Generate the plot and save it
        plot_path = generate_plot(period_days,symbol)
        
        # Send the image to the user
        with open(plot_path, 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo)
        
        # Optional: Clean up by deleting the image file after sending it
        if os.path.exists(plot_path):
            os.remove(plot_path)
        
    except Exception as e:
        bot.send_message(call.message.chat.id, f"An error occurred: {e}")

# Start the bot
bot.polling()

# Handle the /start command
#@bot.message_handler(commands=['start'])
#def send_welcome(message):
    # Generate the plot and save it
 #   plot_path = generate_plot()

    # Send the image to the user
  #  with open(plot_path, 'rb') as photo:
   #     bot.send_photo(message.chat.id, photo)

    # Optional: Clean up by deleting the image file after sending it
    #if os.path.exists(plot_path):
     #   os.remove(plot_path)

# Start the bot
#bot.polling()
