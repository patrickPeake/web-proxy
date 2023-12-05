import requests

# Replace 'your_ip_address' with the actual IP address you want to send the request to
ip_address = '127.0.0.1'
url = f'http://{ip_address}/test.html'  # Specify the path or endpoint as needed
urlBad = f'http://{ip_address}/test.htm'
urlForbidden = f'http://{ip_address}/forbidden/forbidden.html'

import subprocess

# Replace 'script_to_call.py' with the actual name of the script you want to call
script1 = 'test 200-304.py'
script2 = 'test 403-1.py'
script3 = 'test 403-2.py'
script4 = 'test 404.py'

# Use subprocess to call the script
try:
    subprocess.call(['python', script1])
except subprocess.CalledProcessError as e:
    print(f"Error calling {script1}: {e}")

try:
    subprocess.call(['python', script2])
except subprocess.CalledProcessError as e:
    print(f"Error calling {script1}: {e}")

try:
    subprocess.call(['python', script3])
except subprocess.CalledProcessError as e:
    print(f"Error calling {script1}: {e}")

try:
    subprocess.call(['python', script4])
except subprocess.CalledProcessError as e:
    print(f"Error calling {script1}: {e}")
    