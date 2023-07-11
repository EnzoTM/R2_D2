import requests
ip = "" #ip gerado pelo ESP32
def send_request(string):
    url = f'http://{ip}/{string}'
    response = requests.get(url)
    print(response)
