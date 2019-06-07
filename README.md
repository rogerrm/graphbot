# GraphBot

This project contains the code for installing and running GraphBot, a Telegram bot that stores and shows information about geometrical graphs with Earth cities as nodes. You can find all the information about the project in the [statement](https://github.com/jordi-petit/lp-graphbot-2019).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

You need to have [python 3](https://www.python.org/downloads/) and [pip 9.0.1](https://pip.pypa.io/en/stable/installing/) installed on your local machine. You can install them by clicking on the previous links.

### Installing and running

To install the needed Python libraries required, open a new terminal and navigate to the directory folder. Then, install the requirements using 

```
pip3 install -r requirements.txt
```

Now, you need to create a new Telegram bot and get its token following the next instructions:

1. Visit the [@BotFather](https://telegram.me/botfather).
2. Use the `/newbot` command and provide the asked information.
3. Save in a file named `token.txt` the *access token*.
4. Write down your bot address, that has an aspect similar to [t.me/bot_name](https://t.me/bot_name).

Now, you can run the bot running

```
python bot.py
```

## Talking to the bot

Once the bot is running, you can talk to it using the commands expained in the [statement](https://github.com/jordi-petit/lp-graphbot-2019). But first, to stablish a conversation, open your bot address in a web browser, and click Send Message. Then, on Telegram, click Start and you will be able to start talking to the bot!

## Author

* **Roger Romero** [roger.romero.morral@est.fib.upc.edu](mailto:roger.romero.morral@est.fib.upc.edu)
