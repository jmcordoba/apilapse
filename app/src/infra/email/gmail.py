import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Sender:
    """
    Class responsible for sending emails using a Gmail account.
    """
    def __init__(self):
        """
        Initialize the GmailSender with the Gmail account credentials.
        
        :param gmail_user: The Gmail account email address.
        :param gmail_password: The Gmail account password.
        """
        self.gmail_user = 'apilapse@gmail.com'
        self.gmail_password = 'dqxmsbvmszutksmi' # Use an app password

    def send_email(self, to_email, subject, body):
        """
        Send an email using the Gmail account.
        
        :param to_email: The recipient's email address.
        :param subject: The subject of the email.
        :param body: The body of the email.
        :return: True if the email was sent successfully, False otherwise.
        """
        try:
            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Connect to the Gmail SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)

            # Send the email
            server.send_message(msg)
            server.quit()

            print("Email sent successfully")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False