import os
import requests
import logging

WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL','')

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

# Example usage

payload_input = {
    'content': 'Daily Arxiv Papers Digest',
    'embeds': [{
        'title': '最新的 Arxiv 論文精選',
        'description': '以下是今日精選的幾篇論文及其創新點。',
        'color': 0xb31b1b,  # Cornell Red
        'thumbnail': {
            'url': 'https://info.arxiv.org/brand/images/brand-logo-primary.jpg'
        },
        'fields': [
            {
                'name': '論文標題 1',
                'value': '作者：作者 A\n連結：[閱讀原文](https://arxiv.org/abs/1234.56789)\n創新點：這篇論文提出了一種新的機器學習模型，能夠顯著提高預測準確度。',
                'inline': False
            },
            {
                'name': '論文標題 2',
                'value': '作者：作者 B\n連結：[閱讀原文](https://arxiv.org/abs/9876.54321)\n創新點：該研究探討了量子計算在優化問題中的應用，提供了一種新穎的解決方案。',
                'inline': False
            }
        ],
        'footer': {
            'text': '每日日報 - 持續關注最新研究',
            'icon_url': 'https://example.com/icon.png'
        },
        'timestamp': '2024-07-23T12:00:00Z',
        'author': {
            'name': 'Arxiv Digest Bot',
            'url': 'https://arxiv.org',
            'icon_url': 'https://info.arxiv.org/brand/images/brand-logo-primary.jpg'
        }
    }]
}


send_discord_webhook(payload_input)
