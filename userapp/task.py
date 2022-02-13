from celery import shared_task
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import *
import csv
import string
import random
from django.contrib.auth.hashers import make_password
import os
import pandas as pd

@shared_task()
def mail(mail):
    send_mail('message for you','You are allowed by admin and now you can login','javashrm@gmail.com',[mail],fail_silently=False)
    print('send mail successfully')
    return 'Send message successfully'

def generate_password():
      data=''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(6))
      return data

@shared_task()
def login_not_allowed_mail(mail):
    send_mail('message for you','You are not allowed by admin and now you can not login','javashrm@gmail.com',[mail],fail_silently=False)
    print('send mail successfully')
    return 'Send message successfully'


@shared_task()
def savedata(filepath):
    data = pd.read_csv(filepath)
    data.dropna(subset=['username'], inplace=True)
    data.dropna(subset=['name'], inplace=True)
    data.dropna(subset=['email'], inplace=True)
    data.dropna(subset=['phone'], inplace=True)
    for index,row in data.iterrows():
            if CustomUser.objects.filter(username=row['username']).exists():
                pass
            else:
                mypassword=generate_password()
                password=make_password(mypassword,hasher='default',salt=None)
                email=row['email']
                username=row['username']
                user=CustomUser(username=username,
                name=row['name'],email=email,
                phone=row['phone'],password=password)
                user.save()
                send_mail('message for you',f'your email is {email} and your username is {username} and password is {mypassword}',
                'javashrm@gmail.com',[email],fail_silently=False)            
    os.remove(filepath)  
    return "Data Store Successfully"


