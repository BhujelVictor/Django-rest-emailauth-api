import environ
from django.core.mail import EmailMessage


env = environ.Env()
environ.Env.read_env()

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject= data['subject'],
            body= data['body'],
            from_email=env('EMAIL_HOST_USER'),
            to=[data['to_email']],
        )
        email.send()