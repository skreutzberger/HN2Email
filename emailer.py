#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# A class which sends emails 
# works also for Google Mail, aka Gmail

import smtplib
from email.mime.text import MIMEText

class Emailer:
    
    # public vars
    connected = False
    debug = False # set to true for debug 

    # private vars
    _server = "localhost"
    _port = 22
    _login =""
    _password =""
    _connection = None # becomes smtplib.SMTP instance
    
    def __init__(self, server="localhost", port=22, login="", password="", debug=False):
        self._server = server
        self._port = int(port)
        self._login = login
        self._password = password
        self._debug = bool(debug)
        self._connect = self._connect()
    
    # destructor, quits connection if it exists
    def __del__(self): 
        if self._connection:
            self._connection.quit()
    
    # returns boolean about success
    def sendmail(self, from_addr="", to_addr="", subject="", body=""):
        # very basic from and to validation
        if not from_addr or "@" not in from_addr or "." not in from_addr:
            return False
        if not to_addr or "@" not in to_addr or "." not in to_addr:
            return False
        # assemble message
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addr
        # try to connect and then send
        try:
            if self.connected:
                send_ret = self._connection.sendmail(from_addr, to_addr, msg.as_string())
                self._log("return value of connection.sendmail is "+str(send_ret))
                return True
            else:
                self._log("did not send email due to an connection error")
        except:
            self._log("could not send email due to an error while sending")
            pass
        return False
            
    # tries to establish a connection and sets 
    # self._connection to be an instance of smtplib.SMTP
    # returns boolean about success
    def _connect(self):
        ret = False
        s = None # becomes the smtp instance on success
        try:
            self._log("try to connect to "+self._server+":"+str(self._port))
            s = smtplib.SMTP(self._server, self._port)    
            if self._port == 465 or self._port == 587:
                self._log("using SSL")
                success = s.starttls() 
            if self._login and self._password:
                self._log("try to log-in")
                login_ret = s.login(self._login, self._password)
                self._log("return value of login() is "+str(login_ret))
                if login_ret != False: # becomes a list like (235, '2.7.0 Accepted') on success
                    ret = True
            else:
                ret = True
        except: # an error did occur
            self._log("could not connect to "+self._server+":"+str(self._port))
            pass
        self._connection = s
        self.connected = ret
        self._log("return value of _connect() is "+str(ret))
        return ret
        
    # for debug output
    def _log(self, text):
        if self._debug:
            print (text)

###########
# UNIT TESTS
###########


# call the test with Pytest
# py.test emailer.py
def test_connect():
    # enter valid credentials here
    import settings
    server = settings.server
    port = settings.port
    login = settings.login
    password = settings.password
    from_addr = settings.from_addr
    to_addr = from_addr # send email to myself
    
    em = Emailer(server=server, port=port, login=login, password=password, debug=True)
    assert True == em.connected
    
    # test for invalid credentials
    server_faulty = "foo"+server
    em_faulty = Emailer(server=server_faulty, port=port, login=login, password=password, debug=True)
    assert False == em_faulty.connected
    
    # try to send an email
    subject = "Test E-Mail"
    body = "Dear You,\n\nthis is a test."
    sent = em.sendmail(from_addr=from_addr, to_addr=to_addr, subject=subject, body=body)
    assert True == sent
    # invalid from or to
    sent = em.sendmail(from_addr="bar.", to_addr=to_addr, subject=subject, body=body)
    assert False == sent
    sent = em.sendmail(from_addr=from_addr, to_addr="foo", subject=subject, body=body)
    assert False == sent
    # invalid connection
    sent = em_faulty.sendmail(from_addr=from_addr, to_addr=to_addr, subject=subject, body=body)
    assert False == sent
    
    
#test_connect()







