# Dropcatching Filter

The script programmatically downloads the next day's expiring list from Namejet's website and parses it. It then filters the entire list in mere seconds based on the criteria you specify in the config.json file.

If running on a timer of some sort, please set the script to run AFTER 7:00 AM PST because the next day's list is not available until that time the day before.

## Installation
1. Download the Python 3.6.x+ installer from python.org/downloads
2. Run the installer, but please make sure to tick the box labeled "Add Python to environment variables". It is unchecked by default. **This is important!**
3. Open Terminal (Mac/Linux) or Command Prompt (Windows) and type the following command to let the terminal know where the script files are located. Replace [file path] with the full path to the directory containing the files: `cd [file path]`
4. Run the following command: `pip3 install -r requirements.txt`

## Usage
The above installation steps only need to be run once. Now every time you want to run this utility, you simply run the following command: `python main.py` (if that doesn't work, try replacing python in that command with python3)

If executed correctly, you will see domains being output according to your criteria and they will also be saved to a file in the results directory with the name formatted like so `results_MM-DD-YYYY.txt`


**Sample Configuration File** `config.json`
```js
{
  "maxDomainLength": 10,
  "keywords": [
    "minecraft",
    "coin",
    "craft",
    "tech",
    "pvp"
  ],
  "tlds": [
    "com",
    "net",
    "org",
    "io",
    "co"
  ]
}
```



Published a thread about this program on [NamePros](https://www.namepros.com/threads/1089218).

If this helped you, tips are greatly appreciated!

https://paypal.me/croc

https://cash.me/$croc

**BTC:** 36ZTw3CyFoKNZrFcxpx1pZfkPCLBkRGYBF
