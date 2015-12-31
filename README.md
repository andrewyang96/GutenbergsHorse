# GutenbergsHorse
Tweets a sentence from the most popular books of Project Gutenberg every 15 minutes.

Twitter account: [@Gutenbergshorse](https://twitter.com/gutenbergshorse "@Gutenbergshorse")

Suspended as of 2015 Dec 31. If you want to host this yourself, follow these steps:

1. Run `python downloadtexts.py` and type in `y` when prompted.
2. Copy `exampletwitterconfig.py` to `twitterconfig.py` and insert the necessary API keys and tokens.
3. Type `crontab -e` in the terminal and copy the contents of `cronconfig.cron`, changing some absolute paths if necessary.
