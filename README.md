My cheap personal library for messaging
==================================

Author(s): Keith Murray

Contact: kmurrayis@gmail.com



## Usage
Assuming the getKeys.py file has been properly filled out and the program has been installed correctly:

### Basic Usage

    # Import Module
    import kmmessage
    toPhoneSMS = "1234567890@messaging.sprintpcs.com"
    toPhoneMMS = "1234567890@@pm.sprint.com"
    toEmailAddr1 = "demo1@example.com"
    toEmailAddr2 = "demo2@example.com"

    # A simple SMS:
    msg = "A Simple Text Message.\nHello Phone!"
    kmmessage.sms_message_Send(toPhoneSMS, msg)

    # An MMS with an Image:
    msg = "Here's a pretty Picture"
    fl = 'BadParrot.jpg'
    kmmessage.mms_message_Send(recip=toPhoneMMS, msg=msg, media_FilePath=fl)
    # The MMS leaves an empty text string which I cant' easily hide

    # A standard email
    recips = [toEmailAddr1] # expects a list to have multiple recipients
    subj = "Hello, This is a simple email!"
    msg = "Not a whole lot of importance here"
    fls = ['BadParrot.jpg'] # As above, expects a list for multiple attached files
    kmmessage.message_Send_Full_Email(recip=recips, subject=subj, text=msg, files=fls)

    # Check for New Emails
    # I only care who it's from and what the body text says in my use cases
    fromAddrs, msgBodies = checkForMessage()



    

### Warning:
Phone carriers will ignore incoming messages randomly (especially MMS). Just because a message is successfully sent does not mean it will be recieved.


## Install

Because you need to connect the library with a gmail account, and setup default sms, mms, and email accounts the install is messy.

First clone the repo 

    git clone --recursive https://github.com/CrakeNotSnowman/Python_Message.git


inside the kmmessage folder (at the same level as the \_\_init\_\_.py file) you will need to edit the getKeys.py file with the following structure


    def GETEMAIL():
        # Your Messaging Gmail Username (From Addr)
        # Your Messaging Gmail Password (From Pass)
        # Full Gmail Address (From Email)
        # Default To Address for SMS: [10-digit phone number]@carrier.sms.portal
        # Default To Address for MMS: [10-digit phone number]@carrier.mms.portal
        # Default To Address for Standard Email: defaultTargetEmail@EmailHost.com
        username = 'gmailUserName'  
        password = 'gmailPass' 
        fromaddr = 'gmailUserName@gmail.com' 
        toaddrsSMS  = '1234567890@carrier.mms.portal' 
        toaddrsMMS  = '1234567890@carrier.mms.portal' 
        toaddrEmail = 'demo1@example.com' #
        return [username, password, fromaddr, toaddrsSMS, toaddrsMMS, toaddrEmail]

Fill out the varibles with your corrosponding information, and save the file. 

At the folder top level, run 

    pip install .

or 
    pip install -e .

to install allowing for changes to the code to be automatically reflected in future uses of the library.


#### More install information: 

https://python-packaging.readthedocs.io/en/latest/minimal.html


## A more complex, but very useful task
Often time there will be a program that needs user input but it is not reasonable to have the user wait by the computer. This is the perfect time to send a text asking what to do in a given sittuation. 

The key componets of this are get `get_UserInput()` and `getUserFeedbackViaText()`

`get_UserInput` a set of allowed replies to recieve via text, and assumes the use case is a yes or no sittuation. If the text the program recieves is not an expected affirmative, it assumes it's being told not to activate the conditional. 

`getUserFeedbackViaText` is much more complex. This is actually a sample of code I have in a larger program. 

User inputs are the outgoing message, recipient address, and the time delay between each resend of the message in case the message is not recieved by the user's phone. 

Initally, it defines the amount of time the program is willing to wait for a reply. If that time is exceeded, the function returns an empty string. There is also a risk that the text message is never recieved, so it has an allowed number of resends, as well as a user defined number of minutes in between retries. 

Next it flushes the unread emails from the POP libs perspective. This bounds the emails which the program checks to between the start time and max stop time of this function.

Finally the question is sent to the end user

Then the program enters a while loop, where it checks gmails for a new email about once every 30 seconds. If there is a new email, it checks to see if it's sent from the address of the end user (the same address it had just send the question to).

In the while loop there are checks to see if another message should be sent, or if the max wait time has been exceeded. 

Outside of that the sample code is just a standard foo() function which waits to be told whether or not it should execute the conditional. At the end of the whole program it sends a text message letting the user know the program has completed. That message could easily be turned into an email with an attached pdf report about the programs output and results. 




    # Import Module
    import kmmessage
    toPhoneSMS = "1234567890@messaging.sprintpcs.com"
    toPhoneMMS = "1234567890@@pm.sprint.com"
    toEmailAddr1 = "demo1@example.com"
    toEmailAddr2 = "demo2@example.com"
    
    def get_UserInput():
        sms_msg = "Should I do the thing?"
        reply = getUserFeedbackViaText(outgoingMsg=sms_msg, recipAddr=toPhoneSMS).strip()
        print(reply)
        doTheThing=False
        if reply.lower() in ['y', 'yes']:
            print("Zhu Li DO THE THING!")
            doTheThing=True
        else:
            print("Aw. Nevermind Zhu Li.")
            doTheThing=False
        return doTheThing



    def getUserFeedbackViaText(outgoingMsg, recipAddr, tryAgainDelayMin=5):
        """
        Sends a text message to the recipient and waits for a reply
        Parameters
        ----------
        outgoingMsg : str
            The message going to the user
        recipAddr : str
            Email Address string the recipient is at
        tryAgainDelayMin : int
            Number of minutes between each repeated sent message. Networks don't often 
            prioritize these messages, and 'loose' them fairly frequently, or don't 
            pass them through until multiple hours have passed. If there's no reply
            in `tryAgainDelayMin` time, another message is sent, until `resendTotalCount`
            attempts have been made
        Returns
        -------
        msg : str
            The body of the email recieved IF it came in after the outgoing message was 
            sent and before the `hardStopLimitMin` timelimit has been reached and was 
            sent by the same address as `recipAddr`.  If `hardStopLimitMin` is reached,
            returns an empty string.
        Notes
        -----
        It's not the cleanest function, but it works
        Eventually I will build in a varible that mutes the messages between a defined 
        timespan (night or during work hours)
        """
        # Bodge it
        quietAtNight = False
        tryResending = True
        resendTotalCount = 3
        if tryAgainDelayMin == -1:
            tryResending = False
        hardStopLimitMin = 60
        
        # Flush pop queue
        msg_From, msg_Body = kmmessage.checkForMessage()
        
        # Message User
        kmmessage.sms_message_Send(msg=outgoingMsg, recip=recipAddr)
        
        # wait for reply
        startTime = time.time()
        shortWaitStart = startTime
        sentCount = 1
        while True:
            timeSince = time.time() - startTime
            # Hard break if there's been no reply for a long period
            if timeSince > hardStopLimitMin*60:
                # It's over, we've waited too long. Time to move on
                msg = ""
                break
            # Resend message in case it got lost (happens mildly often)
            # Happened, 3 messages, zero recieved 
            if tryResending:
                if sentCount < resendTotalCount:
                    if (time.time() - shortWaitStart) > (tryAgainDelayMin * 60):
                        kmmessage.sms_message_Send(msg=outgoingMsg, recip=recipAddr)
                        sentCount += 1
                        shortWaitStart = time.time()
            # Wait and check for new email
            time.sleep(30)
            msg_From, msg_Body = kmmessage.checkForMessage()
            msg = ""
            # Parse new emails to see if they're from recipAddr
            for i in range(len(msg_From)):
                trimmed = msg_From[i].strip('<').strip('>')
                print(recipAddr, trimmed)
                
                if recipAddr == trimmed:
                    msg = msg_Body[i]
                    break
            if msg != "":
                break
                
        return msg

    def theThing():
        print("Something Special")
        return 

    def bar():
        # this is no fun. 
        return
    
    def foo():
        # Large Complex function that takes a lot of time
        time.sleep(30)
        # Walk away from the computer at some point, and bam, a condtional 
        #  which requires user input pops up
        conditional = True
        if conditional:
            # Time to ask what to do
            doTheThing = get_UserInput()
            if doTheThing:
                theThing()
            else:
                bar()
        # Takes more time to run
        time.sleep(30)
        kmmessage.sms_message_Send(toPhoneSMS, msg="All Done!")
            
