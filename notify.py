import smtplib
from email.message import EmailMessage
import logging

class Notify:
    """class responsible for notification handling
    """
    def __init__(self, host, port, mail_from, mail_passwd, rcpt_to):
        self.host = host
        self.port = port
        self.mail_from = mail_from
        self.mail_passwd = mail_passwd
        self.rcpt_to = rcpt_to




    def send_email(self, msg):
        try:
            logging.info("sending email notification")
            logging.debug("connecting to mail server")
            logging.debug("connected")
            if self.port == 465:
                server = smtplib.SMTP_SSL(self.host, self.port)
            else:
                server = smtplib.SMTP(self.host, self.port)
                server.ehlo()
                server.starttls()
            server.login(self.mail_from, self.mail_passwd)
            logging.debug("logged in")
            server.send_message(
                msg,
                self.mail_from,
                self.rcpt_to
                )    
            server.quit()
            logging.info("notification sent")
        except Exception as e:
            logging.warning("Failed to send email: %s" %(e))


    def create_email(self,service, status):
        if status == 'healthy':
            status = "UP"
        if status == 'unhealthy':
            status = "DOWN"

        body = """
            Mail notification service status
            {service} service is {status}
        """.format(service=service, status=status)

        myemail = EmailMessage()
        myemail['Subject']="Tonto Notification: %s is %s" %(service, status)
        myemail['From']=self.mail_from
        myemail['To']=self.rcpt_to
        myemail.set_content(body)

        return myemail

