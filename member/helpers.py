from django.conf import settings 
# html email required stuff

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from member.models import Deposit, Withdraw


def send_deposit_mail_to_admin(test_id):
    deposit_details = Deposit.objects.filter(test_id=test_id).last()
    html_content = render_to_string("member/deposit_email_to_admin.html",{'title':'send mail','deposit_details':deposit_details})
    text_content = strip_tags(html_content)
    subject = 'YOU GOT A NEW DEPOSIT'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER]
    email_obj = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()


def send_withdraw_mail_to_admin(txn_id):
    withdraw_details = Withdraw.objects.filter(txn_id=txn_id).last()
    html_content = render_to_string("member/withdraw_email_to_admin.html",{'title':'send mail','withdraw_details':withdraw_details})
    text_content = strip_tags(html_content)
    subject = 'YOU GOT A NEW WITHDRAW REQUEST'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER]
    email_obj = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()
