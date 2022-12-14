from django.conf import settings 
# html email required stuff

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from member.models import Withdraw



def youtube_reward_email_to_member(email , price):
    html_content = render_to_string("trxadmin/reward_email_to_member.html",{'title':'send mail','heading':'Youtube Content Earings','content':'Youtube Content Earnings','member':email,'price':price})
    text_content = strip_tags(html_content)
    subject = 'YOU GOT A NEW YOUTUBE CONTENT EARNINGS'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email_obj = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()

def youtube_reward_reject_email_to_member(email , reson , video):
    html_content = render_to_string("trxadmin/youtube_reward_reject_email.html",{'title':'send mail','heading':'Youtube Content','content':'Youtube Content Earnings','member':email,'video':video,'reson':reson})
    text_content = strip_tags(html_content)
    subject = 'YOUTUBE CONTENT'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email_obj = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()


def reffer_reward_email_to_member(email , price):
    html_content = render_to_string("trxadmin/reward_email_to_member.html",{'title':'send mail','heading':'Refferal Earings','content':'Refferal Earnings','member':email,'price':price})
    text_content = strip_tags(html_content)
    subject = 'YOU GOT A NEW REFFERAL EARNINGS'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email_obj = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()

def weekly_reward_email_to_member(email , price):
    html_content = render_to_string("trxadmin/reward_email_to_member.html",{'title':'send mail','heading':'Weekly Earnings','content':'Deposit','member':email,'price':price})
    text_content = strip_tags(html_content)
    subject = 'YOU GOT A NEW WEEKLY EARNINGS'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email_obj = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()

def withdraw_request_reject_email_to_member(id):
    withdraw_obj = Withdraw.objects.get(id=id)
    html_content = render_to_string("trxadmin/withdraw_reject_email.html",{'withdraw_rej_obj':withdraw_obj})
    text_content = strip_tags(html_content)
    subject = 'Your withdrawal request has been rejected'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [withdraw_obj.user]
    email_obj = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()