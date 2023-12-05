import requests

ip_address = '127.0.0.1'
url = f'http://{ip_address}/test.htm'

try:
    response = requests.get(url) # 404 not found
    print(response.status_code)
except Exception as e:
    pass
