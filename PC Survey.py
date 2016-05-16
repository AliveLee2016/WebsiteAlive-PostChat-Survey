#Post Chat Survey report
from __future__ import unicode_literals
import json
import requests
import urllib2
import time
from datetime import datetime
from pytz import UTC
import pytest
from datetime import timedelta
from datetime import date
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import re

def dStrip(jSon):
  #This will strip extra characters from the end date segment.
    sIndx = jSon.index('Date": "') + 8
    sjSon = jSon[:sIndx]
    eIndx = jSon.index('"', sIndx + 1)
    mjSon = jSon[sIndx:eIndx]
    ejSon = jSon[eIndx:]
    mIndx = mjSon.index("T")+1
    mStart = mjSon[:mIndx-1] + " "
    mEnd = mjSon[mIndx:len(mjSon)-5]
    mYear = mStart[:4]
    mMonth = mStart[5:7]
    mDay = mStart[8:]
    mHour = mEnd[:2]
    mMinute = mEnd[3:5]
    mSecond = mEnd[6:8]
    dTime = datetime(int(mYear), int(mMonth), int(mDay), int(mHour), int(mMinute), int(mSecond))
    #Use this timedelta to convert the time zone
    mjSon = dTime - timedelta(hours = 1)
    return sjSon + str(mjSon) + ejSon
    
def eMailCSV(fName):
#This allows the uset to automatically send an e-mail containing the CSV file via e-mail
    send_from = "From_Email"
    send_to = "To_Email"
    subject = "Email_Subject"
    header = "To: To_Email\n From: From_Email\n Subject: Email_Subject\n\n\n"
    text = "Email_Text"
    eServer = "email.server.ext"
    ePort = portNumber
    
    msg = MIMEMultipart()
    msg['From']=send_from
    msg['To'] = send_to
    msg['Date'] =formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    
    with open(fName, "rb") as fil:
        msg.attach(MIMEApplication(
            fil.read(),
            Content_Disposition='attachment; filename="%s"' % basename(fName),
            Name=basename(fName)
        ))

    smtp = smtplib.SMTP(eServer,ePort)
    smtp.ehlo()
    #smtp.start_ssl()
    smtp.starttls()
    smtp.ehlo
    smtp.login('Login_Name', 'Login_Password')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

runs = 1
running = 1
while runs == 1:
    #This if checks to see that the day is Monday before running
    if date.weekday(date.today()) == 0:
        #This if makes sure the script has not already run today
        if running == 1:
            today = date.today()
            eDate = today - timedelta(days=1)
            sDate = today - timedelta(days=7)
            url = "https://apis.websitealive.com/prod/v2/reporting/post-chat-survey?objectref=*SERVER*&groupid=*GROUPID*&surveyid=*SURVEYID*&tz=US/Central&start=" + str(sDate) + "%2000:00:00&end=" + str(eDate) + "%2023:59:59"
            http = urllib2.urlopen(url)
            html = http.read()
            jSonSurveys = json.loads(html)
            
            mDict = []
            for i in jSonSurveys:
                if len(i) > len(mDict):
                    mDict = i
            Keys = []
            for key, item in mDict.iteritems():
                Keys.append(key)
            #print Keys
            jSonk = json.dumps(Keys)
            jSonk = json.loads(jSonk)
            #This area will allow you to re-order your jSon keys.
            jSonk = [jSonk[0], jSonk[1], jSonk[2], jSonk[3], jSonk[4], jSonk[5], jSonk[6], jSonk[7], jSonk[8], jSonk[9], jSonk[10], jSonk[11], jSonk[12]]
            #Set the name for the report here
            csvName = "Post Chat Survey for " + str(sDate) + " to " + str(eDate) + ".csv"
            with open(csvName, 'wb') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = jSonk)
                writer.writeheader()
                for i in jSonSurveys:
                    #print i
                    jSon1 = json.dumps(i)
                    jSon1 = dStrip(jSon1)
                    jSon1 = json.loads(jSon1)
                    #print jSon1
                    try:
                        writer.writerow(jSon1)
                    except Exception as e:
                        print e
                        pass
                csvfile.close()
            #Set the run check to 0 so the system knows not to run again.
            running = 0
            print "ready"
            eMailCSV(csvName)
    #If the day is Tuesday then set the run check back to 1 so that the report can run the following monday
    if date.weekday(date.today()) == 1:
        running = 1
    #Sleep time is the duration between checks
    time.sleep(3600)
    print "Done"
    
