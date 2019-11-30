# OneDayOnly Website Scraper to return all 100% off (FREE) deals

## Requirements

Python 3.7

## Installing

```
pip install -r requirements.txt
chmod a+rx odo.py
```

## Running

```
./odo.py
```

The first time the script is run, it will generate a file called **ids.txt** which contains a list of product IDs.

Every subsequent time it is run, it will only show the newest deals.

## Telegram Notifications

1. Create a Telegram Bot (chat to BotFather on Telegram - /newbot)
2. Create a Public Telegram Channel
3. Make your Bot an Admin of the Telegram Channel
4. Get your Access Token from Bot Father and use the Channel Name to replace the INSERT_HERE in odo.py



