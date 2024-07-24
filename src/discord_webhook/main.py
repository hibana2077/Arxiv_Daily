import os
import time
import datetime
import random
import requests
import logging

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8081')
WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL','https://discord.com/api/webhooks/963662949489197147/ZedW9QI5N8kt5G-RCmniOlv4qOaYCduCbEJXMGi9YBxR6e-G0uSLaAg6BZLZ_G1fps36')
DAILY_SEND_TIME = os.environ.get('DAILY_SEND_TIME', '12:00')

icon_url_list = [
    'https://i.pinimg.com/564x/ce/76/99/ce7699ba7397901965d4d87849556521.jpg',
    'https://i.pinimg.com/564x/32/09/d6/3209d6bc7f26e5fa87719c756f9a2ea5.jpg',
    'https://i.pinimg.com/564x/d9/a1/75/d9a1756b54a1cb91ed46c82ac7f63031.jpg',
    'https://i.pinimg.com/564x/5d/e6/82/5de682c0f20b169525714e8874be79bb.jpg'
]

# Configure logging
logging.basicConfig(level=logging.INFO)

def send_discord_webhook(payload):
    if WEBHOOK_URL:
        payload = payload
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            logging.info('Webhook sent successfully.')
        else:
            logging.error('Failed to send webhook: %s', response.text)
    else:
        logging.warning('DISCORD_WEBHOOK_URL environment variable not set.')

def gen_webhook_payload() -> dict:
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    hour = datetime.datetime.now().hour
    mine = datetime.datetime.now().minute

    response = requests.get(f'{BACKEND_URL}/daily-cs-papers?year={year}&month={month}&day={day-2}')
    if response.status_code == 200:
        papers = response.json().get('papers')
        if papers:
            fields = []
            for paper in papers:
                field = {
                    'name': f'{paper.get("title")}',
                    'value': f'Authors:{', '.join(paper.get("authors"))}\nLink:[Read]({paper.get("link")})\nInnovation:{paper.get("Innovation_or_Breakthrough")}\n\n',
                    'inline': False
                }
                fields.append(field)
            return {
                'content': 'Daily Arxiv Papers Digest',
                'embeds': [{
                    # 'title': '最新的 Arxiv 論文精選',
                    'title': 'Daily Arxiv Papers Digest',
                    # 'description': '以下是今日精選的幾篇論文及其創新點。',
                    'description': 'Here are some selected papers and their innovations today.',
                    'color': 0xb31b1b,  # Cornell Red
                    'thumbnail': {
                        'url': 'https://info.arxiv.org/brand/images/brand-logo-primary.jpg'
                    },
                    'fields': fields,
                    'footer': {
                        'text': 'Arxiv Digest Bot - Give you the latest papers every day',
                    },
                    'timestamp': f'{year}-{month}-{day-1}T{hour}:{mine}:00Z',
                    'author': {
                        'name': 'Arxiv Digest Bot',
                        'url': 'https://github.com/hibana2077/Arxiv_Daily',
                        'icon_url': random.choice(icon_url_list)
                    }
                }]
            }


# send_discord_webhook(payload_input)
if __name__ == '__main__':
    while True:
        try:
            # check is time to send
            now = datetime.datetime.now()
            if now.strftime('%H:%M') >= DAILY_SEND_TIME:
                # check if already send
                year, month, day = now.year, now.month, now.day
                response = requests.get(f'{BACKEND_URL}/daily_check?year={year}&month={month}&day={day}')
                if response.status_code == 200:
                    if response.json().get('fetched') == False:
                        # send webhook
                        payload_input = gen_webhook_payload()
                        send_discord_webhook(payload_input)
                        logging.info('Webhook sent successfully.')
                        # set daily check
                        data = {
                            'year': year,
                            'month': month,
                            'day': day
                        }
                        response = requests.post(f'{BACKEND_URL}/daily_check', json=data)
                        if response.status_code == 200:
                            logging.info('Daily check updated successfully.')
                        else:
                            logging.error('Failed to update daily check.')
                            time.sleep(5)
                    else:
                        logging.info('Webhook already sent today.')
                        time.sleep(5)
                else:
                    logging.error('Failed to check if webhook already sent today.')
                    time.sleep(5)
            else:
                logging.info('Not time to send webhook yet.')
                time.sleep(5)
        except Exception as e:
            logging.error('Error occurred: %s', e)
            time.sleep(5)