import telebot
import http.client
import json
import os
from  project.import_plot import generate_plot 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
#from api_stock import print_indexes  # Ensure this imports the function

# Get Token from bot Father
test1_token = '7339144610:AAGwRBE3Jn8kSwChILtp9SEAMUlhSROvvy0'
bot = telebot.TeleBot(test1_token)

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
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
    
    try:
        # Generate the plot and save it
        plot_path = generate_plot(period_days)
        
        # Send the image to the user
        with open(plot_path, 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo)
        
        # Optional: Clean up by deleting the image file after sending it
        if os.path.exists(plot_path):
            os.remove(plot_path)
        
    except Exception as e:
        bot.send_message(call.message.chat.id, f"An error occurred: {e}")

# Start the bot
#bot.polling()

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