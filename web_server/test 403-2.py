import requests

# Replace 'your_ip_address' with the actual IP address you want to send the request to
ip_address = '127.0.0.1'

url = f'http://{ip_address}/forbidden/forbidden.html'

try:
    response = requests.get(url) # 403 forbidden
    print(response.status_code)
except Exception as e:
    pass
    #print(f"Request failed with an exception: {e}")
