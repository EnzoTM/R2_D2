import requests

import time

ip = "172.20.10.11"

def send_request(string):
    url = f'http://{ip}/{string}'
    
    response = requests.get(url)

    print(f"Mandar a acao {string}")

    print(response)

while True:
    send_request("frente")

    time.sleep(1)