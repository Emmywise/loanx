from twilio.rest import Client
#def SendSMSAPI(recepient, sender):

def SendSMSAPI(recepient, sender, body):
    # the following line needs your Twilio Account SID and Auth Token
    try:
        client = Client("AC6850bd762604a3d795a939c8666a1b26", "d93f7e859f399df844ffb4152aeaef6b")
        client.messages.create(to=recepient, 
                            from_=sender, 
                            body=body)
        return True
    except:
        return False
