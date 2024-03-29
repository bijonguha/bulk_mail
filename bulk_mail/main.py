# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 02:34:01 2019

@author: bijon
"""
from source.utilities import send_mail
import pandas as pd
import os

def main(sender_email, password, receiver_file, subject_file, salutation,\
         body_plain, body_html, html_flag, pause):
    
    contacts = pd.read_excel(os.path.join('data',receiver_file))    
    subject = open(os.path.join('data',subject_file), "r").read()
    body_plain = open(os.path.join('data',body_plain), "r").read()
    html = False
    salutation = open(os.path.join('data',salutation), "r").read()
    
    if(html_flag == 'True'):
        body_html = open(os.path.join('data',body_html), "r").read()
        html = True

    send_mail(sender_email, password, contacts, subject,\
          salutation, body_plain, body_html, html, pause)
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('sender',metavar='SENDER', help='Sender email address')
    parser.add_argument('password',metavar='PASSWORD', help='Password of sender')
    parser.add_argument('-re','--receiver', default='contacts.xlsx', help='Receiver excel file')
    parser.add_argument('-su','--subject',default='subject.txt', help='Subject of Message')
    parser.add_argument('-sal','--salutation',default='salutation.txt', help='Salutation for beginning Message')
    parser.add_argument('-bod','--body', default='body_plain.txt', help='Plain body of Message')
    parser.add_argument('-bod_h','--body_html', default='body_html.txt', help='html body of Message')
    parser.add_argument('-html','--html', default = 'False', help = 'True if msg is html format')
    parser.add_argument('-p','--pause', default = 6, type= int, help = 'Pause timing between each email')
    
    args = parser.parse_args()
    
    sender_email = args.sender
    password = args.password
    receiver_file = args.receiver
    subject_file = args.subject
    body_plain = args.body
    body_html = args.body_html
    html_flag = args.html
    salutation = args.salutation
    pause = args.pause
    
    main(sender_email, password, receiver_file, subject_file, salutation,\
         body_plain, body_html, html_flag, pause)

    
    