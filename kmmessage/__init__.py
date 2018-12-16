#!/usr/bin/env python
"""
Created on Sun May 10 2012

@author: Keith Murray
Updated Fri Dec 14 2018
    By Keith Murray


    The main goal of this function is alter the user when a large
    program has finished running.

    It has three time-based functions. This lets the user know
    when the function began, and how long it took.

    It has two messaging functions.
        The first takes an error title, and sends a message to the
        user altering her/him of the error

        The second takes a start and end time, and a name of the
        function that takes a large amount of time. This function
        is called when the large program is completed, and sends
        the message to the user. 


    The way I use this setup is as follows
        I traditionally have a main() function
        The main() will execute all of the functions of my major
        program. At the top of the main() I call get_time()
        which, non-surprisingly returns the time. I store it in
        some variable start_time. I also usually call
        show_Full_Time() that way at the top of the output for
        whatever program I'm running, I have the start time.
        After the program completes, and I'm at the end of main()
        I call doneTextSend(start_Time, get_time(), process_Name)
        where process_Name is a string for my reference. 


Carrier        Email to SMS Gateway
*****************************************************************
          

Alltel                                [10-digit phone number]@message.alltel.com
                Example: 1234567890@message.alltel.com
    
AT&T (formerly Cingular)        [10-digit phone number]@txt.att.net
                                [10-digit phone number]@mms.att.net (MMS)
                                [10-digit phone number]@cingularme.com
                Example: 1234567890@txt.att.net
    
Boost Mobile                        [10-digit phone number]@myboostmobile.com
                Example: 1234567890@myboostmobile.com
    
Nextel (now Sprint Nextel)        [10-digit telephone number]@messaging.nextel.com
                Example: 1234567890@messaging.nextel.com
    
Sprint PCS (now Sprint Nextel)        [10-digit phone number]@messaging.sprintpcs.com
                                [10-digit phone number]@pm.sprint.com (MMS)
                Example: 1234567890@messaging.sprintpcs.com
    
T-Mobile                        [10-digit phone number]@tmomail.net
                Example: 1234567890@tmomail.net
    
US Cellular                        [10-digit phone number]email.uscc.net (SMS)
                                [10-digit phone number]@mms.uscc.net (MMS)
                Example: 1234567890@email.uscc.net
    
Verizon                                [10-digit phone number]@vtext.com
                                [10-digit phone number]@vzwpix.com (MMS)
                Example: 1234567890@vtext.com
    
Virgin Mobile USA                [10-digit phone number]@vmobl.com
                Example: 1234567890@vmobl.com

*****************************************************************

TROUBLE SHOOTING
I run this on Ubuntu 12.04, raspberry pi, windows 10 and this is Python 2.7.3/2.7.9,
Ubuntu 18.04 and python 3.6.5


If your service provider is not covered in this list, Google
"how do I find out my phone number's email address". 

Verify that your
[10-digit phone number]@serviceProvider.something functions with
and actual email address to minimize headaches.

This uses Simple Mail Transfer Protocol
http://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol
and the setup this program uses is for Gmail.

I recommend that you make a Gmail account, but that's only because
it's what I use. If you want to use another email provider,
search for it.

I've also encountered some errors when the function will execute,
but a text message will not be received. After reviewing my email
accounts sent message list, I've noted that the emails are sent,
and the error PROBABLY lies with the service provider.

One last thing of note: I start each line in the messages I send
with \n because that's the way I get it to work. There's a reason
behind this fact, however I've never bothered to look. 
    
"""

import time
from time import gmtime, strftime, localtime
import poplib
from email import parser
import email, os

try:
    # Python 3.6
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE, formatdate
    from email import encoders as Encoders
except ImportError:
    # Python 2.7
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email.Utils import COMMASPACE, formatdate
    from email import Encoders


import imaplib
from . import getKeys
import smtplib


# Credentials (if needed)
# I recomend you create a new email account just for this
emKeys = getKeys.GETEMAIL()
username = emKeys[0] 
password = emKeys[1]
fromaddr = emKeys[2]
toaddrsSMS  = emKeys[3]
toaddrsMMS  = emKeys[4]
toaddrEmail = emKeys[5]

def message_Error(errorName):
    '''
    function takes in an error name (as a string), and sends
    a text message alerting the user of the error 
    '''
    msg = ('\nERROR\nProcess: Errored Out\n' + str(errorName))
  
    # The actual mail send  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  
    server.sendmail(fromaddr, toaddrEmail, msg)
    server.quit()
    

def checkForMessage():
    '''
    This function serves to check email for a specific command
    I suggest the use of cron instead of this function, but this 
    is acting as a proof of concept 
    '''
    from_Addr = ''
    message_Str = ''
    message_Body = []
    message_From = []
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user(username)
    pop_conn.pass_(password)
    #Get messages from server:
    messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
    # Concat message pieces:
    try:
        #python 2.7:
        messages = ["\n".join(mssg[1]) for mssg in messages]
    except TypeError:
        # python 3.6
        messages = [b"\n".join(mssg[1]).decode("utf-8")  for mssg in messages]

    #Parse message intom an email object:
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]
    for message in messages:
        from_Addr = str(message['Return-Path'])
        #print "\n\tSubject:   \t" + str(message['Subject'])
        #print "\tRtrn. Path:\t" + str(message['Return-Path'])
        #print "\tDate:      \t" + str(message['Date'])
        #print "\tFrom:      \t" + str(message['From'])
        #print '    ***MESSAGE***'
        #phoneEmail = 'xxxxxxxxxx@emailof.serviceprovider.com'
        #if ( str(message['From']) == phoneEmail) :
        #    print "\t" + str(message.get_payload())
        #    message_Send('\nMessage Below was Recieved:\n' + str(message.get_payload()) )
        #if ( str(message['From']) != phoneEmail) :
        #    print "\t" + str(message.get_payload(0, False))# len of 1: fails if a text message
        #    message_Body = str(message.get_payload())
        #print "\n"
        #print ()
        message_From.append(from_Addr)
        message_Body.append(str(message.get_payload()))

    pop_conn.quit()
    return message_From, message_Body


def message_Send_Full_Email(recip, subject, text, files=[]):
    assert type(recip)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = COMMASPACE.join(recip) 
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    if text != "":
        msg.attach( MIMEText(text) )
    

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    # The actual mail send  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  
    server.sendmail(fromaddr, recip, msg.as_string())  
    server.quit()


def message_Send(recip, msg):
    '''
    function verifies that a message was recieved, echos the message
    '''
    
    # The actual mail send  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  
    server.sendmail(fromaddr, recip, msg)  
    server.quit()

def sms_message_Send(recip, msg):
    '''
    function verifies that a message was recieved, echos the message


    Notes
    =====
    https://stackoverflow.com/questions/13299954/python-smtplib-adds-newline-to-message#
    There will be a new line at the end of this. 
    '''
    if recip == "":
        recip = toaddrsSMS
    msg = "\n" + str(msg).strip()
    
    # The actual mail send  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  
    server.sendmail(fromaddr, str(recip), msg)  
    server.quit()



def mms_message_Send(recip, msg, media_FilePath):
    '''
    function verifies that a message was recieved, echos the message


    Notes
    =====
    https://stackoverflow.com/questions/13299954/python-smtplib-adds-newline-to-message#
    There will be a new line at the end of this. 
    '''
    if recip == "":
        recip = toaddrsSMS
    message_Send_Full_Email([recip], subject="", text=msg, files=[media_FilePath])



