import requests

ip_address = '127.0.0.1'

url = f'http://{ip_address}/forbidden/forbidden.html'

try:
    response = requests.get(url) # 403 forbidden
    print(response.status_code)
except Exception as e:
    pass
