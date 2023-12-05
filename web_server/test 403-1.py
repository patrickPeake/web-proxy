import requests

# Replace 'your_ip_address' with the actual IP address you want to send the request to
ip_address = '127.0.0.1'
url = f'http://{ip_address}/test.html'  # Specify the path or endpoint as needed



try:
    response = requests.delete(url)   # 403 forbidden 
    print(response.status_code)
except Exception as e:
    pass
    #print(f"Request failed with an exception: {e}")

