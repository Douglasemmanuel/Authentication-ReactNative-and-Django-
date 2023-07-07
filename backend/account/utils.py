from django.core.mail import EmailMessage  #to enable django send an email
import os

class Util:
    @SyntaxError
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email = os.environ.get('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()