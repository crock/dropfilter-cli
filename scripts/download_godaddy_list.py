#!python
import shutil
import urllib.request as request
from contextlib import closing
from urllib.error import URLError
import os
import arrow
import zipfile
import json

service_name = "godaddy"
list_url = "ftp://auctions@ftp.godaddy.com/all_listings_ending_tomorrow.json.zip"
filename = "all_listings_ending_tomorrow"
date_format = "M-DD-YYYY"
timezone = "America/New_York"
local = arrow.now(timezone)
script_path = os.path.dirname(os.path.abspath(__file__))

# download dates
tomorrow = local.shift(days=1).format(date_format)

def in_x_days(num_days):
	return local.shift(days=num_days).format(date_format)
	
all_download_times = [tomorrow]

def reformat(name):
	domains = []
	
	with open(f"lists/{service_name}/{name}.json", 'r') as fx:
		jsonData = json.load(fx)
		for domain in jsonData['data']:
			domains.append(domain['domainName'].lower())
	
	with open(f"lists/{service_name}/{name}.txt", 'w') as fx:
		fx.write("\n".join(domains))
	
	os.remove(f"lists/{service_name}/{name}.json")

for dl_time in all_download_times:
	url = list_url
	
	try:
		with closing(request.urlopen(url)) as r:
			if not os.path.exists(script_path, '..', f"lists/{service_name}"):
				os.makedirs(script_path, '..', f"lists/{service_name}")
			path = os.path.join(script_path, '..', f"lists/{service_name}", f"{dl_time}.zip")
			with open(path, 'wb') as f:
				shutil.copyfileobj(r, f)
			with zipfile.ZipFile(path, 'r') as zip_ref:
				zip_ref.extractall(f"lists/{service_name}")
			source_path = os.path.join(script_path, '..', f"lists/{service_name}", f"{filename}.json")
			dest_path = os.path.join(script_path, '..', f"lists/{service_name}", f"{dl_time}.json")
			os.rename(source_path, dest_path)
			os.remove(path)
			reformat(dl_time)
			print(f"Downloaded {service_name} list: {dl_time}.zip")
	except URLError as e:
		print(f"Could not download {service_name} list: {dl_time}.zip")
		if e.reason.find('No such file or directory') >= 0:
			raise Exception('FileNotFound')
		else:
			raise Exception(f'Something else happened. "{e.reason}"')