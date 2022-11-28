import smtplib
import json
import os
class EmailSend():
    def __init__(self):
        file_path = os.path.abspath(__file__) # full path of your script
        dir_path = os.path.dirname(file_path) # full path of the directory of your script
        config_file_path = os.path.join(dir_path,'config.json') # absolute zip file path 
        with open(config_file_path, 'r') as c:
            self.mail_data = json.load(c)["mail_data"]
        # print("email sent")

    def send_email(self,SUBJECT, TEXT):
        print("blah blah")
        try:
            # create a smtp object
            toaddr = 'quick.cap.llc@gmail.com'
            cc = ['muhamdasim.business@gmail.com']
            bcc = ['harrissmanzoor22@gmail.com']
            fromaddr = self.mail_data['sender_mail']
            message_subject = SUBJECT
            message_text = TEXT
            message = "From: %s\r\n" % fromaddr+ "To: %s\r\n" % toaddr+ "CC: %s\r\n" % ",".join(cc)+ "Subject: %s\r\n" % message_subject+ "\r\n" + message_text
            toaddrs = [toaddr] + cc + bcc
            server = smtplib.SMTP('mail.codeaza-apps.com',587)
            server.starttls()
            server.login(self.mail_data['sender_mail'],self.mail_data['sender_password'])
            server.set_debuglevel(1)
            server.sendmail(fromaddr, toaddrs, message)
            server.quit()
        except smtplib.SMTPException as e:
            print(e)
            print ("Error: unable to send email")
        
# obj = EmailSend()
# name = 'hotels in tronto'
# message = "Task Completed Successfully for the query {}".format(name)
# obj.send_email(message)