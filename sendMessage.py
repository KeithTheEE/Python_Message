#!/usr/bin/env python
"""
@author: Crake

The main goal of this function is alert the user when a large
program has finished running.

It has three time-based functions. This lets the user know
when the function began, and how long it took.

It has two messaging functions.

1. The first takes an error title, and sends a message to the user altering
   her/him of the error

2. The second takes a start and end time, and a name of the function that takes
   a large amount of time for my reference and convenience. This function is
   called when the large program is completed, and sends the message to the
   user.

The way I use this setup as follows:

- I traditionally have a main() function.
- The main() will execute all of the functions of my major program.
- At the top of the main() I call get_time() which, non-surprisingly returns
  the time.
- I store it in some variable start_time.
- I also usually call show_Full_Time() that way at the top of the output for
  whatever program I'm running, I have the start time.
- After the program completes, and I'm at the end of main() I call
  doneTextSend(start_Time, get_time(), process_Name) where process_Name is
  a string for my reference later on.


Carrier	Email to SMS Gateway
*****************************************************************


Alltel	                        [10-digit phone number]@message.alltel.com
                Example: 1234567890@message.alltel.com

AT&T (formerly Cingular)        [10-digit phone number]@txt.att.net
                                [10-digit phone number]@mms.att.net (MMS)
                                [10-digit phone number]@cingularme.com
                Example: 1234567890@txt.att.net

Boost Mobile	                [10-digit phone number]@myboostmobile.com
                Example: 1234567890@myboostmobile.com

Nextel (now Sprint Nextel)	[10-digit telephone number]@messaging.nextel.com
                Example: 1234567890@messaging.nextel.com

Sprint PCS (now Sprint Nextel)	[10-digit phone number]@messaging.sprintpcs.com
                                [10-digit phone number]@pm.sprint.com (MMS)
                Example: 1234567890@messaging.sprintpcs.com

T-Mobile	                [10-digit phone number]@tmomail.net
                Example: 1234567890@tmomail.net

US Cellular	                [10-digit phone number]email.uscc.net (SMS)
                                [10-digit phone number]@mms.uscc.net (MMS)
                Example: 1234567890@email.uscc.net

Verizon	                        [10-digit phone number]@vtext.com
                                [10-digit phone number]@vzwpix.com (MMS)
                Example: 1234567890@vtext.com

Virgin Mobile USA	        [10-digit phone number]@vmobl.com
                Example: 1234567890@vmobl.com

*****************************************************************

TROUBLE SHOOTING

I run this on Ubuntu 12.04 and this is written in Python 2.7.3

I have no real programming background, and have very little
experience with programming in general. I am writing this up
because this is one of my most helpful functions I've written,
and I want to help anyone who wants to use it as well. There
are some errors is this, but it works so I use it.

If your service provider is not covered in this list, Google
'how do I find out my phone number's email address'. That's how I
came up with this list, and it's not a hard feat to manage.

Verify that your
[10-digit phone number]@serviceProvider.something functions with
and actual email address before using this function to minimize
headaches further on down the line.

This uses Simple Mail Transfer Protocol
http://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol
and the setup this program uses is for Gmail.

I recommend that you make a Gmail account, but that's only because
it's what I use. If you want to use another email provider,
search for it. I also recommend that you create an email account
for the express purpose of this program, and that the email account
is not linked to anything else (ie not your Reddit account). In my
opinion this is for your personal security, but hey, do as you will.

I've also encountered some errors when the function will execute,
but a text message will not be received. After reviewing my email
accounts sent message list, I've noted that the emails are sent,
and the error PROBABLY lies with the service provider.

One last thing of note: I start each line in the messages I send
with \n because that's the way I get it to work. There's a reason
behind this fact, however I've never bothered to look.

"""

import smtplib
import time
from time import gmtime, strftime, localtime

# Credentials (if needed)
# I recomend you create a new email account just for this
username = 'emailUserName'
password = 'password'
fromaddr = 'yourEmailAddress'
toaddrs  = 'emailAddressOfTarge@somewhere'

def get_Time() :
    return time.time()

def show_Full_Time() :
    return strftime("%a, %d %b %Y %H:%M:%S", localtime())



def show_Time(start_Time, end_Time) :
    '''
    THERE IS AN ERROR in this formatting. If this section is important
    to you, correct it. It takes floating point numbers as its input.
    '''
    timeUsed = end_Time - start_Time
    hoursHold = int(timeUsed / 3600)
    minutesHold = int(timeUsed / 60 - int(hoursHold * 60))
    secondsHold = int(timeUsed - int(minutesHold*60))
    formatedTime = str(hoursHold) + ':' + str(minutesHold) + ':' + str(secondsHold)
    return formatedTime


def errorTextSend(errorName) :
    '''
    function takes in an error name (as a string), and sends
    a text message alerting the user of the error
    '''
    msg = ('\nERROR\nProcess: Errored Out\n' + str(errorName))

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


def doneTextSend(start_Time, end_Time, process) :
    '''
    function takes the start and end time (both are floating points) of whatever
    your function is, and the function title (string).
    '''
    timeUsed = end_Time - start_Time
    hoursHold = int(timeUsed / 3600)
    minutesHold = int(timeUsed / 60 - int(hoursHold * 60))
    secondsHold = int(timeUsed - int(minutesHold*60))
    formatedTime = str(hoursHold) + ':' + str(minutesHold) + ':' + str(secondsHold)


    msg = ('\nDONE\nProcess: ' + str(process) + '\nTime required: '  + str(formatedTime))


    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
