import requests   // codigo em python utilizado para mandar HTTP requests e controlar o ESP32
ip = "" #ip gerado pelo ESP32
def send_request(string):
    url = f'http://{ip}/{string}'
    response = requests.get(url)
    print(response)
