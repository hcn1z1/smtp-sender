# smtp-sender
A library to send emails with smtps.

smtps syntax:  smtp|port|username|password
# usage
```
from SE.sender import SE
'''
    Adding data to the Sender
'''
SUBJECT = ["Subjects","List"]
SENDER = ["SENDERs","List"]
EMAIL = "/SE/emails.txt"
IMAGE = "/SE/IMAGE.png"
SMTP = "/SE/SMTP.txt"
HTML = "HTML Mail Letter"
SENDER = SE()
SENDER.emailExtracting(EMAIL)
SENDER.smtpExtracting(SMTP)
SENDER.LetterIntoObj(HTML)
SENDER.DATA(subject= SUBJECT, sender= SENDER, image= IMAGE)
'''
    Running the Sender
'''
SENDER.run()
```

# Features
- Multithreading with Random choice.
- Embedded Images added.
- Some variable method to use will give advantage to sender.
