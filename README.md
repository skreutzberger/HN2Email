# HN2Email

Ever wanted to have the top-ranked Hacker News articles automatically in your **Readability** account? 

Or in your **Wunderlist** inbox? Or maybe in **Evernote** or in \<ADD FANCY WEBSERVICE NAME HERE\>?

HN2Email fetches the article links and sends them by email to one of these services. Call it with a cronjob and you are ready to go! 

BTW: Did you know that Readability can push the full articles(!) automatically in a daily agenda to your Kindle? 

## Requirements

HN2Email is a Python application. Luckily, Python 2.7 is already pre-installed on most Mac OS X and Linux computers. The script does not require any extra dependencies.

You even do **not need** Readability API keys!

## Setup & Run

- put the files in folder
- copy or rename settings_default.py to settings.py
- enter your email credentials in settings.py
- enter your personal Readability, Evernote, etc. mail-in email address
- run `python emailer.py` to send the emails

## Further Infos
You can automate the fetching and sending by calling the script by a cronjob. I recommend not earlier as 6:00 UTC due the slow update of the top-rank list.

I also recommend to use a standard localhost SMTP server and not a Google Mail account, because Google often thinks that your account was hacked if it receives an email which was sent automatically with your credentials.

This project is based upon one of my other OS Github projects called HN2Readability. That still used the official way (Readability API), but the approach of HN2Email is far simpler and also more flexible. And that’s always better, isn’t it?

## Please Contribute
... and add more services. Hacker News is great, so let's mail the links to other services!





