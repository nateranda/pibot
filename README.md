#  Pibot
A command-line Python tool that uses rpilocator and Discord webhooks to notify when Raspberry Pis are back in stock.

### Disclaimer
The creator of rpilocator doesn't want anyone pinging the RSS feed more than once a minute, so don't change the wait time unless you want to get IP banned.

## Requirements
Pibot uses 3 pip libraries:
* Requests
* Feedparser
* Click

Setuptools can install these dependencies automatically and add the script to the PATH—just paste these commands to make a virtual environment and run the script in there:

```shell
python3 -m venv venv
. venv/bin/activate
pip install --editable .
pibot [OPTIONS] URL
```

If you don't want to use setuptools, ignore the setup.py file. The Python script can run on its own if the required packages are installed.

## Usage
Just run the Python script with your installed Python interpreter. Include any options you want to use and paste your Discord webhook URL at the end:

```
python3 pibot.py [OPTIONS] URL

Options:
  -f, --filter TEXT  Query to filter RSS feed.
  -t, --test         Quick feed & webhook test.
  --help             Show this message and exit.
```

The bot will then send a message indicating it started successfully. After a new stock update, it will send a message with a link to buy the Raspberry Pi.

Funny enough, I usually run this script on my Raspberry Pi. I just SSH into the machine, run the script with nohup in the background, and eventually kill the process using pkill:

```shell
nohup -u python3 pibot.py [OPTIONS] URL &
pkill -f pibot.py
```

It saves any output in the `nohup.out` file in case you need to troubleshoot.

All executable builds were built with pyinstaller on their respective platforms.

### Filters
You can filter your query by region/vendor and model. A widget to customize the filter is available at the bottom of [rpilocator's about page](https://rpilocator.com/about.cfm). Just use the `--filter` or `-f` flag and include everything after the last slash and you're good to go.