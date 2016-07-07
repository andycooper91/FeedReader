# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 14:18:42 2016

@author: andy.cooper
"""

import feedparser
from threading import *
import copy

class Future:

    def __init__(self,func,*param):
        # Constructor
        self.__done=0
        self.__result=None
        self.__status='working'

        self.__C=Condition()   # Notify on this Condition when result is ready

        # Run the actual function in a separate thread
        self.__T=Thread(target=self.Wrapper,args=(func,param))
        self.__T.setName("FutureThread")
        self.__T.start()

    def __repr__(self):
        return '<Future at '+hex(id(self))+':'+self.__status+'>'

    def __call__(self):
        self.__C.acquire()
        while self.__done==0:
            self.__C.wait()
        self.__C.release()
        # We deepcopy __result to prevent accidental tampering with it.
        a=copy.deepcopy(self.__result)
        return a

    def Wrapper(self, func, param):
        # Run the actual function, and let us housekeep around it
        self.__C.acquire()
        try:
            self.__result=func(*param)
        except:
            self.__result="Exception raised within Future"
        self.__done=1
        self.__status=`self.__result`
        self.__C.notify()
        self.__C.release()



yahoo_EEUU = "https://es.noticias.yahoo.com/rss/estados-unidos"
yahoo_deportes = "https://es.noticias.yahoo.com/rss/deportes"
yahoo_americaLatina = "https://es.noticias.yahoo.com/rss/america-latina"
yahoo_economia = "https://es.noticias.yahoo.com/rss/economia"

bbc_recent = "http://www.bbc.co.uk/mundo/ultimas_noticias/index.xml"
bbc_tech = "http://www.bbc.co.uk/mundo/temas/tecnologia/index.xml"
bbc_cultura = "http://www.bbc.co.uk/mundo/temas/cultura/index.xml"
bbc_economia = "http://www.bbc.co.uk/mundo/temas/economia/index.xml"

cnn_espanol = "http://cnnespanol.cnn.com/feed/"

                     
#feed = feedparser.parse( python_wiki_rss_url )
feed1 = Future(feedparser.parse,cnn_espanol)
feed2 = Future(feedparser.parse,yahoo_economia)
feed3 = Future(feedparser.parse,yahoo_deportes)

   
links = []

count = 0
for item in feed1()["entries"]:
    links.append((item["published"],item["link"]))
    count += 1
    if count >2:
        break
    
count = 0
for item in feed2()["entries"]:
    links.append((item["published"],item["link"]))
    count += 1
    if count >2:
        break
    
count = 0
for item in feed3()["entries"]:
    links.append((item["published"],item["link"]))
    count += 1
    if count >2:
        break
    


newline = """
"""

body = ""
for l in links:
    body += l[0] + " - " + l[1]
    body += newline
    body += newline 




def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"





newline = """
"""

body = ""
for l in links:
    body += l[0] + " - " + l[1]
    body += newline
    body += newline 


user = "andycooper91@gmail.com"
pwd = ""
recipient = "andycooper91@gmail.com"
subject = "Daily Spanish Articles!"

send_email(user,pwd,recipient,subject,body)