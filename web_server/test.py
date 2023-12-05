#this test driver spawns various processes to send one http request each and print the http response
import subprocess

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
    