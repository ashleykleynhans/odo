#!/usr/local/bin/python3.7

import time
from datetime import datetime
import schedule
import requests
import re
from pyquery import PyQuery


def get_deals():

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    url = 'https://www.onedayonly.co.za/'

    try:
        r = requests.get(url, timeout=5.0, headers=headers)

        if r.status_code == 200:
            html = r.text
            return html

        else:
            print(f"ERROR: Something went wrong (Status code: {r.status_code}")

    except:
        print('ERROR: Could not get data')


def get_ids():
    try:
        file = open('ids.txt', 'r')
        data = file.read()
        ids = data.split()
        file.close()
    except:
        ids = []

    return ids


def get_products(html):
    if html == None:
        print('ERROR: HTML From OneDayOnly website is empty')
        return

    ids = get_ids()
    pq = PyQuery(html)
    products = pq('div.product_block')

    for item in products:
        id  = PyQuery(item)
        id = id('.new_product_block_anchor').attr('id')

        name = PyQuery(item)
        name = name('.name').text()
        name = name.strip()

        retail = PyQuery(item)
        retail = retail('.retail').text()
        retail = retail.strip()
        m = re.match(r"^Retail: (.+)", retail)

        if m is not None:
            retail = m.group(1)
        else:
            retail = '-'

        selling = PyQuery(item)
        selling = selling('.selling').text()
        selling = selling.strip()

        url = PyQuery(item)
        url = url('a.new_product_block').closest('a').attr('href')

        # Specify that we are only interested in values with a selling price of R0
        if selling == 'R0' and id not in ids:
            msg = f"ID: {id}\n"
            msg += f"Name: {name}\n"
            msg += f"Retail: {retail}\n"
            msg += f"Selling: {selling}\n"
            msg += f"URL: {url}\n"

            print(f"Found deal: {name}")
            print(f"Sending Telegram Notification for: {name}")

            telegram_bot_sendtext(msg)

            print(f"Adding ID {id} to the list of ids in ids.txt")
            out = open('ids.txt', 'a')
            out.write(id + "\n")
            out.close()


def telegram_bot_sendtext(bot_message):
    bot_token = 'INSERT_HERE'
    bot_chatID = 'INSERT_HERE'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def scrape():
    dt = datetime.now()
    ts = dt.strftime("%Y-%m-%d %H:%M:%S")

    print(f"{ts} : Scraping OneDayOnly.....")

    html = get_deals()
    get_products(html)


def run():
    schedule.every(15).seconds.do(scrape)
    scrape()

    while True:
        schedule.run_pending()
        time.sleep(1)


run()
