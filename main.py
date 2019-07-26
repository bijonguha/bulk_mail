# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 02:34:01 2019

@author: bijon
"""
from source.utilities import send_mail
import pandas as pd
import os
import time

def main(sender_email, password, receiver_file, subject_file, salutation,\
         body_plain, body_html, html_flag):
    
    contacts = pd.read_excel(os.path.join('data',receiver_file))    
    subject = open(os.path.join('data',subject_file), "r").read()
    body_plain = open(os.path.join('data',body_plain), "r").read()
    html = False
    salutation = open(os.path.join('data',salutation), "r").read()
    
    if(html_flag == 'True'):
        body_html = open(os.path.join('data',body_html), "r").read()
        html = True
    
    
    for i in range(len(contacts)):
        receiver_email = contacts.loc[i,'email']
        receiver_name = contacts.loc[i,'name']
        print('Sending email to %s' %receiver_email)
        send_mail(sender_email, password, receiver_email, receiver_name, subject,\
              salutation, body_plain, body_html, html)
        time.sleep(6)
        print('email sent !')
        
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
    parser.add_argument('--html', default = 'False', help = 'True if msg is html format')
    
    args = parser.parse_args()
    
    sender_email = args.sender
    password = args.password
    receiver_file = args.receiver
    subject_file = args.subject
    body_plain = args.body
    body_html = args.body_html
    html_flag = args.html
    salutation = args.salutation
    
    main(sender_email, password, receiver_file, subject_file, salutation,\
         body_plain, body_html, html_flag)

    
    