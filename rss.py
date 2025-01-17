import os
import pickledb # You can use any other database too. Use SQL if you are using Heroku Postgres.
import feedparser
from time import sleep, time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from apscheduler.schedulers.background import BackgroundScheduler

session_name = "1BJWap1sBuxh59IVLjC-UqTwiPhcFgHlUesS_z-D_5cZv_4hqamv59QwVw_4UdEEA2sZ_bo3v6DzQepyfhzMBR37NaZMJLwUNevgxtaH6xLfqUjJ9QKkRGrpgCsUjI-5VZeyDy_wxWZ_RjR1bdtuyNVPrWgN0xoVhnPgfbfBFHMyZxlvIIrD9mCJ9iXhj9YVe-GIZ5-ERDdFdD1rd6kQtbcxwuwucK6yO4HzjJd26eQg1HSlQnsiupzVvNKC-fgIvyqjy7ZE1H9na2D9dm3bdeyvfosnyFIrqSVsN22KkbLlbXplZ4Aok_dNWiH3Hr7ym-KsiB5INfqRf4bexDs5NALw80MLb2mc="
api_id = "1799071"   # Get it from my.telegram.org
api_hash = "f011e39356047f59a9a31bc46300a602"   # Get it from my.telegram.org
feed_url = "https://torrentgalaxy.to/rss?magnet&user=29"   # RSS Feed URL of the site.
# Get it by creating a bot on https://t.me/botfather
log_channel = "-1001161510664"   # Telegram Channel ID where the bot is added and have write permission. You can use group ID too.
check_interval = 5   # Check Interval in seconds.  
max_instances = 5   # Max parallel instance to be used.
if os.environ.get("ENV"):   # Add a ENV in Environment Variables if you wanna configure the bot via env vars.
  api_id = os.environ.get("APP_ID")
  api_hash = os.environ.get("API_HASH")
  feed_url = os.environ.get("FEED_URL")
  session_name = os.environ.get("SESSION_NAME")
  log_channel = int(os.environ.get("LOG_CHANNEL", None))
  check_interval = int(os.environ.get("INTERVAL", 30))
  max_instances = int(os.environ.get("MAX_INSTANCES", 5))

db = pickledb.load('rss.db', True)
if db.get("feed_url") == None:
  db.set("feed_url", "*")
app = Client(session_name=session_name, api_id=api_id, api_hash=api_hash)

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
