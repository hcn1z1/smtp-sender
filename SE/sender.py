'''
    Email sender through Simple Mail Transform Protocol
'''
from threading import Thread
from queue import Queue
from base64 import b64encode
from email.message import EmailMessage
from smtplib import SMTP
from random import choice
from email.utils import make_msgid

class Inboxing:
    def __init__(self,emails:list,smtps:list,letter:str,subject:list,sender:list,image:list):
        self.emails = emails
        self.smtps = smtps
        self.letter = letter
        self.subject = subject
        self.sender = sender
        self.img_list = image
    def send(self, lead :str):
        '''
        :param lead: a string input. sending one email per thread
        :return: None
        this is going to look complicated
        '''
        SMTPs = choice(self.smtps).split("|") #choosing a random smtp ['0','565',fdsfdsf]
        #Some SMTP informations
        sender_email = SMTPs[2]
        sender_password = SMTPs[3]
        if len(SMTPs)>4 : sender = SMTPs[4]
        else : sender = sender_email
        sender_id = choice(self.sender) #choosing a random sender id
        email_content = self.letter
        subject = choice(self.subject) #choosing a randome subject

        '''
        Preparing for sending 
        Setting HTML variables
        '''
        email_content = email_content.replace("THISISAKEYFORSPAGHETTIRUNNNERLOL", lead)
        email_content = email_content.replace("[email]", lead)
        email_content = email_content.replace("[username]", lead.split("@")[0])
        email_content = email_content.replace("[randomname]", str(choice(self.names)) + " " + str(choice(self.names)))
        email_content = email_content.replace("[randombr]", str(choice(self.random_browser)))
        email_content = email_content.replace("[os]", str(choice(self.OSs)))
        email_content = email_content.replace("[location]", str(choice(self.LOCs)))
        email_content = email_content.replace("[emailbase64]",b64encode(bytes(lead, "utf-8")).decode("UTF-8"))
        
        '''
        Setting subject and senderid variables
        '''
        subject = subject.replace("[link]", str(choice(self.Links)))
        subject = subject.replace("[os]", str(choice(self.OSs)))
        subject = subject.replace("[location]", str(choice(self.LOCs)))
        subject = subject.replace("[email]", lead)
        subject = subject.replace("[username]", lead.split("@")[0])
        subject = subject.replace("[randomname]", str(choice(self.names)) + " " + str(choice(self.names)))
        subject = subject.replace("[randombr]", str(choice(self.random_browser)))
        sender_id = sender_id.replace("[randomname]", str(choice(self.names)) + " " + str(choice(self.names)))
        sender_id = sender_id.replace("[randombr]", str(choice(self.random_browser)))
        sender_id = sender_id.replace("[link]", str(choice(self.Links)))
        sender_id = sender_id.replace("[os]", str(choice(self.OSs)))
        sender_id = sender_id.replace("[location]", str(choice(self.LOCs)))

        '''
        Setting MIME
        '''
        msg = EmailMessage()
        msg["To"] = lead
        msg["From"] = f"{sender_id} <{sender}>"
        msg['Subject'] = subject

        '''
        Setting embedded image to content
        '''
        name_section,cid = self.imageembedded(lead)
        for x in name_section:email_content = email_content.replace(x, str(cid[x])[1:-1])
        msg.add_alternative(email_content, "html")
        msg = self.payloadImg(msg,cid)
        '''
        Setting Server
        '''
        try:server = SMTP(SMTPs[0] + ":" + str(SMTPs[1]), timeout=10);server.starttls()
        except:server = SMTP(SMTPs[0] + ":" + str(SMTPs[1]), timeout=10)
        server.ehlo()
        server.login(sender_email,sender_password)
        server.sendmail(msg['From'], [lead], msg.as_string())
        print(f" Message sent to ! {lead}")
    def imageembedded(self,lead):
        cid = {}
        name_section = []
        try:
            for x, d in zip(self.img_list, range(len(self.img_list))):
                image_cid = make_msgid(domain=lead.split("@")[1])
                name = "#IMAGE" + str(d + 1)
                cid[name] = image_cid
                name_section.append(name)
        except:
            pass
        return name_section,cid
    def payloadImg(self,msg,cid={}):
        for x in range(len(self.img_list)):
            mp = "#IMAGE" + str(x + 1)
            msg.get_payload()[0].add_related(self.img_list[x],
                                             maintype="image",
                                             subtype="png",
                                             cid=cid[mp])
        return msg
    def openingfiles(self):
        '''
        Opening files that contain some random informations
        such as random operating system, random lacatuins and random links
        :return: bunch of lists inherited in class
        '''
        names = open("env/names.txt","r")
        self.names = list(names.read().splitlines())
        names.close()
        randoms = open("env/random.txt","r")
        self.random_browser= randoms.read().splitlines()
        randoms.close()
        os = open("env/os.txt","r")
        self.OSs= os.read().splitlines()
        os.close()
        os = open("env/locations.txt","r")
        self.LOCs= os.read().splitlines()
        os.close()
        os = open("env/link.txt","r")
        self.Links= os.read().splitlines()
        os.close()
    def queue_th_config(self,q):
        while not q.empty():
            i=q.get()
            try:self.send(i)
            except Exception as e:
                print(e)
                print("Dead SMTP or Internet")
            q.task_done()
class SE:
    def __init__(self):
        self.img_list = []
    def emailExtracting(self, emails :str):
        '''
            extractiong all emails from a file
            input : file path
            return : an array of emails
        '''
        self.emailsList = open(emails,'r').read().splitlines()

    def smtpExtracting(self, smtps :str):
        '''
            extractiong all smtps from a file
            input : file path
            return : an array of smtps
        '''
        self.smtpsList = open(smtps,'r').read().splitlines()

    def LetterIntoObj(self, letter :str):
        self.HTML = letter

    def DATA(self, subject = None, sender = None, image = None):
            if subject is not None:
                self.subject = subject
            elif sender is not None:
                self.sender = sender
            elif image is not None:
                self.img_list.append(open(image,"rb").read())

    def run(self):
        if bool(self.smtpsList) is True and bool(self.HTML) is True and bool(self.emailsList) is True:
            SEND = Inboxing(emails = self.emailsList , smtps= self.smtpsList,letter = self.HTML,
                            subject = self.subject,sender=self.sender,image=self.img_list)
            SEND.openingfiles()
            job = Queue()
            for jobs in self.emailsList:
                job.put(jobs)
            for i in range(5):
                th=Thread(target=SEND.queue_th_config,args=(job,))
                th.daemon=True
                th.start()
            return "Job is Done"
        else:
            return "Lack of requirements"
        
