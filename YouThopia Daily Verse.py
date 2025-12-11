import os
import threading
import time
import requests
import schedule
import telebot
import logging
from flask import Flask
from dotenv import load_dotenv

import json
GROUPS_FILE = "groups.json"

#function to load group ID  from the file
def load_groups():
    try:
        with open(GROUPS_FILE, "r")  as  f:
            return set(json.load(f)) # I used set here to avoid Duplicates
    except FileNotFoundError:
        return set()

#Function to save a new group ID
def save_group(group_id):
    groups = load_groups()
    groups.add(group_id)
    with open(GROUPS_FILE, "w") as f:
        json.dump(list(groups), f)
        logging.info(f"Saved new group ID: {group_id}")



# --- START OF KEEP-ALIVE SERVER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "I am alive"

def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_http_server)
    t.start()

# Start the server immediately so Render sees the open port
keep_alive()
# --- END OF KEEP-ALIVE SERVER ---
   
# Load variables from .env file
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to get a random Bible verse
def get_random_verse():
    try:
        response = requests.get("https://bible-api.com/?random=1", timeout=10)
        response.raise_for_status()
        data = response.json()
        return f"{data['reference']}\n\n{data['text']}"
    except Exception as e:
        logging.error(f"Error fetching verse: {e}")
        return "I couldn't fetch a verse right now. Try again later."

# Function to send an automatic Bible verse every morning
def send_morning_verse():
    logging.info("Sending Morning Verse to  all groups....")
    verse = get_random_verse()
    groups = load_groups()
    
    for chat_id in groups:
        try:
            bot.send_message(chat_id, f"Hey Good Morning! Here is your Bible Verse For The Day📖: \n\n{verse}")
            time.sleep(0.5) #Wait 0.5 seconds To avoid hittting telegram limit
        except  Exception as e:
            logging.error(f"Failed to send to group{chat_id}: {e}")
  
    
# --- SCHEDULER CONFIGURATION ---
# Note: Render servers are usually UTC.
# Nigeria (WAT) is UTC+1. So 05:00 UTC = 06:00 Nigeria time.
schedule.every().day.at("05:00").do(send_morning_verse)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start the scheduler in a separate thread
threading.Thread(target=run_scheduler, daemon=True).start()

# --- BOT COMMANDS ---
@bot.message_handler(commands=["verse"])
def send_verse(message):
    bot.reply_to(message, get_random_verse())

@bot.message_handler(commands=["ping"])
def ping(message):
    bot.reply_to(message, "I am Alive and Kicking ✔")
    
    
    
#-----When Bot is added to a group-----
@bot.message_handler(content_types=["new_chat_members"])
def on_join(message):
    for new_member in message.new_chat_members:
        if new_member.id == bot.get_me().id:
            save_group(message.chat.id)
            bot.send_message(message.chat.id, "Hello! Thanks for adding me to the group. You will receive daily verses starting tomorrow by 6am!📖")   
    
    
# --- WELCOME COMMAND ---
# Usage: /start or /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # 1. Get the name, but SPLIT it to take only the first word
    full_name = message.from_user.first_name
    if full_name:
        user_first_name = full_name.split()[0]  # "Cyril Ogban" -> "Cyril"
    else:
        user_first_name = "Friend"  # Fallback just in case
    
    # 2. Create the welcome text
    welcome_text = (
        f"👋 *Hi {user_first_name}, Welcome to YouThopia Daily Verse! \n\n I am a Christ-Centered community Bot ✝️* \n\n"
        "I am here to encourage you with God's word every day.\n\n"
        "✨ *Here is what I can do:*\n"
        "Daily Morning Verse (Automatic at 6:00 AM)\n"
        "/read [Verse] - Read a specific Bible verse (e.g., /read John 3:16)\n"
        "/verse - Get a random encouraging verse right now\n"
        "/find [topic] - Find verses for emotions (e.g., /find anxiety)\n"
        "/ping - Check if I am online\n\n"
        "📢 *Add me to your Group* to send verses to everyone!"
    )

    # 3. Send the message with Markdown enabled (for bold text)
    bot.reply_to(message, welcome_text, parse_mode="Markdown")  

# --- INFINITE RESTART LOOP ---
if __name__ == "__main__": 
    while True:
        try:
            bot.polling(non_stop=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            logging.error(f"Bot crashed: {e}")
            time.sleep(5)  # Wait 5 seconds before restarting
            continue