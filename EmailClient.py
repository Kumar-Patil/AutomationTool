from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from Util import Util
class EmailClient():

    def __init__(self):
        #self.my_address = "santosh_patil2@bmc.com"
        print ""

    def send(self,bmcSubject, bmcfrom, bmcTo,bmcBody,bmcReply):

        msg = MIMEMultipart()
        msg['Subject'] = bmcSubject
        msg['From'] = bmcfrom
        msg['Reply-to'] = bmcReply
        msg['To'] = bmcTo
 
        # That is what u see if dont have an email reader:
        msg.preamble = 'Multipart massage.\n'
 
        # This is the textual part:
        part = MIMEText(bmcBody)
        msg.attach(part)
 
        # This is the binary part(The Attachment):
        part = MIMEApplication(open("report.html","rb").read())
        part.add_header('Content-Disposition', 'attachment', filename="report.html")
        msg.attach(part)
 
        # Create an instance in SMTP server
        #smtp = SMTP("mail.bmc.com")
        smtp = SMTP("172.24.32.31")
        # Send the email
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())