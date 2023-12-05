import requests

ip_address = '127.0.0.1'
url = f'http://{ip_address}/test.html'  # Specify the path or endpoint as needed

try:
    response = requests.get(url) # 304 or 200 depending on timing
    print(response.status_code)
except Exception as e:
    pass


