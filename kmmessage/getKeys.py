

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