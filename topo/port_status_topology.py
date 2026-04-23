import urllib.request
import time

print("Simple topology demo started.")
print("This file simulates Mininet actions for 3 switches.")

# s1-eth1 goes DOWN
print("1. Bringing s1-eth1 DOWN")
time.sleep(2)
urllib.request.urlopen(
    "http://127.0.0.1:8080/down?switch=s1&port=1"
).read()

# s2-eth2 goes DOWN
print("2. Bringing s2-eth2 DOWN")
time.sleep(2)
urllib.request.urlopen(
    "http://127.0.0.1:8080/down?switch=s2&port=2"
).read()

# s3-eth1 comes UP
print("3. Bringing s3-eth1 UP")
time.sleep(2)
urllib.request.urlopen(
    "http://127.0.0.1:8080/up?switch=s3&port=1"
).read()

# s1-eth1 comes UP again
print("4. Restoring s1-eth1")
time.sleep(2)
urllib.request.urlopen(
    "http://127.0.0.1:8080/up?switch=s1&port=1"
).read()

print("Done. Check controller terminal and dashboard.")
