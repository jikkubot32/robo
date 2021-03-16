import os
import pickledb # You can use any other database too. Use SQL if you are using Heroku Postgres.
import feedparser
from time import sleep, time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from apscheduler.schedulers.background import BackgroundScheduler


session_name="1BVtsOHoBu7vG8mDwraw0kC774M_SClICGAwEJiSZOtYAxd2L-iKxRLLgAdJCorlVQ7cS-JpWq7Qt7Sb7vHJUhjx5xGe-dkD7OrjJIUYy60Ro8EHfdlxBUIpNwV4hxqqkwzNqgdtV91rU_L1theVIWZIc6ql7o-tRFvEkcsz39nXbkia1H5CiA9Sdo8EQ6vQ71U3BDcybCg7pD35OQJwtD_ZQfWZcF4hY-A85kM3BwyLI5Donl-FeqVWbfiQkEsWTGHlbajTpZVmf9hbf0wsRfT28RCnA0-Sl5-kMx5w7X1ei0vBUku3C8A8H1qAak29AKwHLOh04LrxYSNzxQU3J-9MDa5Jtgfw="
api_id = 1086018  # Get it from my.telegram.org
api_hash = "3c2f1a043c1a22d5b0af74b8268993d5"   # Get it from my.telegram.org
feed_url = ["https://torrentgalaxy.to/rss?magnet"]  # RSS Feed URL of the site.
#bot_token = "1668902665:AAH5Nip5RlqEEZU5PdRK37UTizMtqJYM9SQ"   # Get it by creating a bot on https://t.me/botfather
log_channel = "-1001453174349"   # Telegram Channel ID where the bot is added and have write permission. You can use group ID too.
check_interval = 5   # Check Interval in seconds.    
max_instances = 1   # Max parallel instance to be used.
if os.environ.get("ENV"):   # Add a ENV in Environment Variables if you wanna configure the bot via env vars.
  api_id = os.environ.get("APP_ID")
  api_hash = os.environ.get("API_HASH")
  feed_url = os.environ.get("FEED_URL")
  session_name = os.environ.get("SESSION_NAME")
  log_channel = int(os.environ.get("LOG_CHANNEL", None))
  check_interval = int(os.environ.get("INTERVAL", 5))
  max_instances = int(os.environ.get("MAX_INSTANCES", 5))

db = pickledb.load('rss.db', True)
if db.get("feed_url") == None:
  db.set("feed_url", "*")
app = Client("rss-bot", session_name=session_name, api_id=api_id, api_hash=api_hash)

def check_feed():
    FEED = feedparser.parse(feed_url)
    entry = FEED.entries[0]
    if entry.id != db.get("feed_url"):
      
                   # ↓ Edit this message as your needs.
      message = f"{entry.link}"
      
      try:
        app.send_message(log_channel, message)
        db.set("feed_url", entry.id)
      except FloodWait as e:
        print(f"FloodWait: {e.x} seconds")
        sleep(e.x)
      except Exception as e:
        print(e)
    else:
      print(f"Checked RSS FEED: {entry.id}")



scheduler = BackgroundScheduler()
scheduler.add_job(check_feed, "interval", seconds=check_interval, max_instances=max_instances)
scheduler.start()
app.run()
