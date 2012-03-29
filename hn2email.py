#!/usr/bin/env python
# -*- coding: utf-8 -*-
# the script connects to daemonology and fetches the 
# top 10 links on Hacker News of a day
# the links can be sent by email afterwards, for example to
# Wunderlist, Evernote or Readability

#import os, sys, readability
#from modules import parser

import urllib
import time
from datetime import date, timedelta
import emailer
try:
    import settings
except:
    print ("Please rename settings_default.py to settings.py and try again. Thanks!")
    exit()

# check if somehow variables are missing in setup.py
required_settings = ["server", "port", "login", "password", "from_addr", "send_to"]
for var in required_settings:
    if not hasattr(settings, "from_addr"):
        print ("The variable "+var+" is somehow missing or invalid in settings.py. Please double-check. Thanks!")

if not settings.from_addr or not settings.send_to or not settings.server or not settings.port:
    print ("There are some email settings missing in settings.py. Please add them and try again.")

if len(settings.send_to) < 1:
    print ("Please activate (remove the #) from at least one email address in the send_to variable in settings.py")

# returns the html of a page or False
def get_html(source):
	try:
		sock = urllib.urlopen(source) 	
		html = sock.read()                            
		sock.close()   
		return html
	except:
		return False	

# checks if a string is in the format YYYY-MM-DD
# and valid, returns boolean
def is_daystring(day=""):
    struct_time = time.strptime("30 Nov 00", "%d %b %y")
    print "returned tuple: %s " % struct_time

# returns a list of links from Hacker News
# on error an empty list is returned
def hnlinks_top10(datestr="2012-01-23"):
    links = []
    # check if datestr is valid
    try:
        struct_time = time.strptime(datestr, "%Y-%m-%d")
    except:
        print ("ERROR: Invalid date "+datestr+", please use format YYYY-MM-DD")
        return links
    # fetch html
    url = "http://www.daemonology.net/hn-daily/"+datestr+".html"
    html = get_html(url)
    if html == False:
        print ("ERROR: Could not connect to "+url)
        return links	
    # parse html, take the first block
    blocks = html.split('<h2>')
    block = blocks[1]
    title = block.split("</h2>")[0]    
    # get the story links
    parts = block.split('<span class="storylink"><a href="')[1:]
    for part in parts:
    	url = part.split('">')[0]
    	if "http" in url and "//news.ycombinator.com" not in url:
    		links.append(url)
    # was everyhing successfully extracted?
    if len(title) < 5 or len(links) < 1:
    	print ("ERROR: Could not extract title and links from page")
    return links

# get yesterday’s links
yesterday = date.today() - timedelta(1)
yesterday_string =  yesterday.strftime('%Y-%m-%d')
links = hnlinks_top10(yesterday_string)

# stop if there are no links
if not links:
    exit(0)
else:
    print ("Successfully fetched "+str(len(links))+" links")

############## 
# send the email
subject = 'Top 10 HN Articles '+yesterday_string
body = "\n".join(links)
#print subject
#print body
debug = False # set to True if connection does not work

em = emailer.Emailer(server=settings.server, port=settings.port, 
                        login=settings.login, password=settings.password, debug=debug)
if em.connected:
    for to_addr in settings.send_to:
        sent = em.sendmail(from_addr=settings.from_addr, to_addr=to_addr, subject=subject, body=body)
        if sent:
            print ("Sent email to "+to_addr)
        else:
            print ("ERROR: could not send email to "+to_addr)
else:
    print ("Could not connect to email server, please check your settings in settings.py")