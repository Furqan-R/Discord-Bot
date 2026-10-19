import feedparser

FEED_URL = "https://www.scmp.com/rss/514820/feed"

def get_entries():
    feed = feedparser.parse(FEED_URL)
    return feed.entries




