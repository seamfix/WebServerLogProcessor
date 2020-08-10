#!/usr/bin/env python3

from datetime import datetime

print(datetime.today().strftime('%Y-%m-%d'))
print(datetime.today())



import subprocess
subprocess.call(["mv", "logs/ssl_request.2020.01.11.log", "logs/backup/ssl_request.2020.01.11.log"])
print("file move completed")