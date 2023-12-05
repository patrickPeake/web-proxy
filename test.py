import requests

# Replace 'your_ip_address' with the actual IP address you want to send the request to
ip_address = '127.0.0.1'
url = f'http://{ip_address}/test.html'  # Specify the path or endpoint as needed

try:
    response = requests.post(url)
    print(response.status_code)
    # Check the response status code
    if response.status_code == 200:
        print(f"Success! Response content:\n{response.text}")
    else:
        print(f"Request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Request failed with an exception: {e}")