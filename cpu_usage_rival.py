import psutil
import time
import subprocess


while True:
	cpu_usage = psutil.cpu_percent()
	print(cpu_usage)
	message = "cpu " + str(cpu_usage)
	subprocess.call(["python3", "rttoled.py", message])
	time.sleep(2)
