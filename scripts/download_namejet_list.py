#!python
import requests
import os
import arrow

service_name = "namejet"
list_url = "http://www.namejet.com/download/%s.txt"
date_format = "M-DD-YYYY"
timezone = "America/New_York"
local = arrow.now(timezone)
scripts_dir = os.path.dirname(os.path.abspath(__file__))
lists_dir = os.path.join(scripts_dir, '..', 'lists')

# download dates
today = local.format(date_format)
yesterday = local.shift(days=-1).format(date_format)
tomorrow = local.shift(days=1).format(date_format)

def in_x_days(num_days):
	return local.shift(days=num_days).format(date_format)
	
all_download_times = [today, yesterday, tomorrow, in_x_days(2), in_x_days(3)]

if not os.path.exists(f"{lists_dir}/{service_name}"):
	os.makedirs(f"{lists_dir}/{service_name}")
for dl_time in all_download_times:
	url = list_url % dl_time
	path = os.path.join(f"{lists_dir}/{service_name}", f"{dl_time}.txt")
	if not os.path.exists(path):
		try:
			response = requests.get(url)
			if response:
				with open(path, 'w') as fx:
					fx.write(response.text)
				print(f"Downloaded {service_name} list: {dl_time}")
		except:
			print(f"Could not download {service_name} list: {dl_time}")