# Pip packages
import click
import feedparser
import requests

# Built-in packages
import time

# Save a timestamp to check if update is new
timestamp = ''


# Click stuff & main loop
@click.command()
@click.option('--filter', '-f', help='Query to filter RSS feed.')
@click.option('--test', '-t', is_flag=True, help='Quick feed & webhook test.')
@click.argument('url', required=True)
def main(filter, url, test):
    """Sends a notification to a discord webhook URL when a Raspberry Pi is in stock."""
    if test:
        test_script(filter, url)
        quit()

    start_feed(filter, url)
    while True:
        check_feed(filter, url)
        time.sleep(60)


# Checks for new updates
def check_feed(filter, url):
    global timestamp
    print('Checking for updates...', end =" " )
    feed = feedparser.parse(f'https://rpilocator.com/feed/{filter}')
    
    if feed.status == 200: # healthy response
        if not feed.entries: 
            print('No results.')
        elif not feed.entries[0].published == timestamp: # check if result has a newer timestamp
            timestamp = feed.entries[0].published
            print('Update found!')
            notify(feed.entries[0], url)
        else:
            print('No updates.')
    else:
        print('Error checking RSS feed. The link could be down or your query could be incorect.')


# Sets an initial timestamp
def start_feed(filter, url):
    global timestamp
    print('Initializing feed...')
    feed = feedparser.parse(f'https://rpilocator.com/feed/{filter}')
    
    if feed.status == 200:
        r = requests.post(url, data={"content": "Pibot Started!"})
        if feed.entries:
            timestamp = feed.entries[0].published
        else:
            print('No results.')
    else:
        print('Error checking RSS feed. The link could be down or your query could be incorect.')


# Sends discord webhook
def notify(entry, url):
    data = {
        "content": f"@everyone **Stock Update!**\n[{entry.title}]({entry.link})"
    }
    r = requests.post(url, data=data)


# Quick feed & webhook test
def test_script(filter, url):
    click.echo("Test Mode")
    click.echo('Initializing feed...')
    
    feed = feedparser.parse(f'https://rpilocator.com/feed/{filter}')
    
    if feed.status == 200:
        click.echo('Feed successful!')
        if feed.entries:
            click.echo("Sending latest result to Discord...")
            notify(feed.entries[0], url)
        else:
            click.echo('No results.')
    else:
        click.echo('Error checking RSS feed. The link could be down or your query could be incorect.')


if __name__ == '__main__':
    main()