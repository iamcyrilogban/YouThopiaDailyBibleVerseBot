
 YouThopia Daily Bible Verse Bot

A simple Telegram bot that sends daily Bible verses to your group or channel and allows users to request random verses on command. Built with Python, `pyTelegramBotAPI`, and scheduled tasks.


Features

* Sends a daily Bible verse every morning at 6:00 AM.
* Responds to `/verse` command with a random Bible verse.
* Responds to `/ping` command to confirm the bot is active.
* Easy to configure with a `.env` file for your bot token.


Setup

1. **Clone the repository**

```bash
git clone https://github.com/iamcyrilogban/YouThopiaDailyBibleVerseBot.git
cd YouThopiaDailyBibleVerseBot
```

2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set your Telegram bot token in a `.env` file:

```
BOT_TOKEN=your_bot_token_here
```



Usage

* Run locally:

```bash
python YouThopiaDailyVerse.py
```

Deploy on platforms like **Render**: set the start command to:

```bash
python YouThopiaDailyVerse.py
```



Commands

* `/verse` – Get a random Bible verse immediately.
* `/ping` – Check if the bot is alive.



Tech Stack

* Python 3.13+
* [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* [requests](https://pypi.org/project/requests/)
* [schedule](https://pypi.org/project/schedule/)


## Contribution

Feel free to fork, modify, and submit pull requests. Please respect the coding style and update `requirements.txt` for any new dependencies.

