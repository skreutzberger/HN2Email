#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Please put here your credentials, etc.
# a comment starts with a # 

# email server settings
server = "localhost" # for Gmail use smtp.gmail.com
port = 587 # for Gmail use 587,  port 465 may not work
login = "" # for Gmail it is your full email address
password = ""
from_addr = "" # your sender email address

# add here your (personal) send-in email addresses from
# Readability, Evernote, Wunderlist where you want to send your
# Hacker News links to (you can also add your personal email here for testing)
# please make sure that your sender-email is correct (on Wunderlist & Evernote)
# remove the # to activate a link, you can also add links
send_to = [ 
                    "CHANGE_THIS@inbox.readability.com",
                    #"me@wunderlist.com",
                    #"CHANGE_THIS@m.evernote.com", 
]
