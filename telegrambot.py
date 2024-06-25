import requests
import datetime
import time

PROMETHEUS_URL = "http://localhost:9090"
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
CPU_THRESHOLD = 80
RAM_THRESHOLD = 80
CHECK_INTERNAL = 60

def query_promethus(query):
    url = f'{PROMETHEUS_URL}/api/v1/query'
    params = {
        'query': query
    }
    response = requests.get(url, params = params)
    result = response.json()['data']['result']
    if result:
        return float(result[0]['value'][1])
    return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.get(url, params=params)
    return response.json()

while True:
    try:
        cpu_usage = query_promethus('avg(server_cpu_usage)')
        ram_usage = query_promethus('avg(server_memory_usage)')
        # cpu_usage = 90
        if cpu_usage is not None and cpu_usage > CPU_THRESHOLD:
            message = f"Warning: High CPU usage detected! Current usage: {cpu_usage:.2f}%"
            send_telegram_message(message)

        if ram_usage is not None and ram_usage > RAM_THRESHOLD:
            message = f"Warning: High RAM usage detected! Current usage: {ram_usage:.2f}%"
            send_telegram_message(message)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(CHECK_INTERNAL)
