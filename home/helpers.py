


from django.core.mail import send_mail

from django.conf import settings 
# html email required stuff

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_forget_password_mail(email , token ):
    html_content = render_to_string("home/email_forget_password.html",{'title':'send mail','content':token})
    text_content = strip_tags(html_content)
    subject = 'We have received a request to reset your password.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email_obj = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()
