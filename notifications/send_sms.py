from twilio.rest import Client
def SendSMSAPI(recepient, sender):
    # the following line needs your Twilio Account SID and Auth Token
    try:
        client = Client("AC6850bd762604a3d795a939c8666a1b26", "d93f7e859f399df844ffb4152aeaef6b")

        # change the "from_" number to your Twilio number and the "to" number
        # to the phone number you signed up for Twilio with, or upgrade your
        # account to send SMS to any phone number
        # client.messages.create(to=recepient, 
        #                     from_=sender, 
        #                     body="Hello from Python!")
        client.messages.create(to="+2347062277804", 
                            from_="+17403050449", 
                            body="Hello from Python!")
        return True
    except:
        return False
