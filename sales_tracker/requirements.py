from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from .models import MiningData

import pytz #used to set our required time zone
import datetime
import smtplib

MINIMUM_MINING_COUNT = 0


def send_mail( time, username):
    my_mail_id = "gururajhr0305l@gmail.com"
    my_password = "vhax huoc shhq qjmh"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_mail_id, my_password)
        connection.sendmail(
            from_addr = my_mail_id,
            to_addrs = "gururajhr0305@gmail.com",
            msg = f"Subject:Employee Early Logout.\n\n {username} has been logged out earlier than actual time. \n Emp name : {username} \n Total logined Time : {time[0]}:{time[1]}:{time[2]}"
        )




def timer(utc_login_time):
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_login_time = utc_login_time.astimezone(ist_timezone)
    current_time = datetime.datetime.now(ist_timezone)
    elapsed_time = current_time - ist_login_time
    elapsed_time = str(elapsed_time).split(".")[0].split(":")
    return elapsed_time


def min_mining_required(a):
    
    def inner(template_name):
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        
        today_mining = MiningData.objects.filter(date = now_date)
        today_mining_count = today_mining.count()
        if today_mining_count >= MINIMUM_MINING_COUNT:
            a(template_name)
            print('this is working')
            return redirect("login")
        else:
            print('this is working')
            return HttpResponse("You need to complete 40 minings to logout")

    return inner


        
    