#!python
import requests
import os
import arrow
import zipfile

service_name = "snapnames"
list_url = "https://snapnames.com/file_dl.sn?file=%s.zip"
date_format = "M-DD-YYYY"
timezone = "America/New_York"
local = arrow.now(timezone)
script_path = os.path.dirname(os.path.abspath(__file__))

# download dates
tomorrow = local.shift(days=1).format(date_format)

def in_x_days(num_days):
	return local.shift(days=num_days).format(date_format)
	
all_download_times = [
	(tomorrow, "snpexpingexclusive1list"), 
	(in_x_days(2), "snpexpingexclusive2list"), 
	(in_x_days(3), "snpexpingexclusive3list"), 
	(in_x_days(4), "snpexpingexclusive4list"), 
	(in_x_days(5), "snpexpingexclusive5list")
]

def reformat(name):
	domains = []
	
	with open(script_path, '..', f"lists/{service_name}/{name}.txt", 'r') as fx:
		lines = fx.readlines()
		del lines[0]
		for line in lines:
			parts = line.split('\t')
			domains.append(parts[0])
	
	with open(script_path, '..', f"lists/{service_name}/{name}.txt", 'w') as fx:
		fx.write("\n".join(domains))

for item in all_download_times:
	dl_time = item[0]
	name = item[1]
	url = list_url % name
	try:
		response = requests.get(url)
	
		if response:
			if not os.path.exists(script_path, '..', f"lists/{service_name}"):
				os.makedirs(script_path, '..', f"lists/{service_name}")
			path = os.path.join(script_path, '..', f"lists/{service_name}", f"{dl_time}.zip")
			with open(path, 'wb') as fx:
				fx.write(response.content)
			with zipfile.ZipFile(path, 'r') as zip_ref:
				zip_ref.extractall(script_path, '..', f"lists/{service_name}")
			source_path = os.path.join(script_path, '..', f"lists/{service_name}", f"{name}.txt")
			dest_path = os.path.join(script_path, '..', f"lists/{service_name}", f"{dl_time}.txt")
			os.rename(source_path, dest_path)
			os.remove(path)
			reformat(dl_time)
			print(f"Downloaded {service_name} list: {dl_time}.zip")
	except:
		print(f"Could not download {service_name} list: {dl_time}.zip")