import os.path
import json

import requests
import arrow
import progressbar
from lib.Filters import Filters


local = arrow.now("America/New_York")
tomorrow = local.shift(days=1).format("M-DD-YYYY")

url = f"http://www.namejet.com/download/{tomorrow}.txt"
# csv = "https://snapnames.com/search_dl.sn?type=12"

filename = tomorrow + ".txt"

fp = open("config.json", "r")
config = json.load(fp)
fp.close()

def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code is 200:
        if not os.path.exists("tmp"):
            os.makedirs("tmp")
        fx = open(os.path.join('tmp', filename), 'wb')
        file_size = int(response.headers['Content-Length'])
        chunk = 1
        num_bars = file_size / chunk
        bar = progressbar.ProgressBar(maxval=num_bars).start()
        i = 0
        for chunk in response.iter_content():
            fx.write(chunk)
            bar.update(i)
            i += 1
        fx.close()
        print("Done.")
    else:
        print("Couldn\'t get file.")


def filter_domains(domains):
    for domain in domains:
        filter = Filters(config)
        a = filter.is_select_tld(domain)
        b = filter.is_proper_length(domain)
        c = filter.contains_keyword(domain)

        if not os.path.exists("results"):
            os.makedirs("results")
        fx = open(os.path.join('results', f'results_{filename}'), 'a')
        if a is True and b is True and c is True:
            print(domain)
            fx.write(domain + '\n')
        fx.close()


def main():
    if os.path.isfile(os.path.join('tmp', filename)):
        pass
    else:
        print("Downloading tomorrow\'s list of expiring domains...")
        download_file(url, filename)

    print("Filtering domains according to your specified conditions...")
    domains = [line.rstrip('\n') for line in open(os.path.join('tmp', filename))]
    filter_domains(domains)


if __name__ == '__main__':
    main()
