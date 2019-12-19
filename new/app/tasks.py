from flask import current_app
from flask import request, render_template, flash, redirect, url_for, session
from flask_mail import Message

from app import celery, mail

#set celery's send email task
@celery.task
def send_async_email(email_data,**kwargvs):
    msg = Message(email_data['subject'],
                  recipients=[email_data['to']])
    #msg.body = email_data['body']
    msg.body=render_template(email_data['body']+'.txt',**kwargvs)
    msg.html=render_template(email_data['body']+'.html',**kwargvs)
    #print(email_data)
    with current_app.app_context():
        mail.send(msg)

