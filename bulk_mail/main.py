# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 02:34:01 2019

@author: bijon
"""
from source.utilities import send_mail
import pandas as pd
import os

def main(sender_email, password, receiver_file, salutation_plain, signature_plain,\
         body_plain, salutation_html, signature_html, body_html, html_flag, pause, domain):
    
    contacts = pd.read_excel(os.path.join('data', receiver_file))
    body_plain = open(os.path.join('data','plain',body_plain), "r").read()
    html = False
    salutation_plain = open(os.path.join('data','plain',salutation_plain), "r").read()
    signature_plain = open(os.path.join('data','plain',signature_plain), "r").read()
    
    if(html_flag == 'True'):
        body_html = open(os.path.join('data', 'html', body_html), "r").read()
        html = True
        salutation_html = open(os.path.join('data','html',salutation_html), "r").read()
        signature_html = open(os.path.join('data','html',signature_html), "r").read()
    
    send_mail(sender_email, password, contacts, salutation_plain, body_plain, signature_plain,\
                  salutation_html, body_html, signature_html, html, pause, domain)
        
if __name__ == "__main__":
    import argparse
    import getpass
    parser = argparse.ArgumentParser()
    parser.add_argument('sender',metavar='SENDER', help='Sender email address')
    #parser.add_argument('password',metavar='PASSWORD', help='Password of sender')
    parser.add_argument('-re','--receiver', default='contacts.xlsx', help='Receiver excel file')
    parser.add_argument('-salP','--salutationP',default='salutation_plain.txt', \
                        help='Plain Salutation for beginning Message')
    parser.add_argument('-salH','--salutationH',default='salutation_html.txt', \
                        help='Html Salutation for beginning Message')
    parser.add_argument('-bodP','--bodyP', default='body_plain.txt', help='Plain body of Message')
    parser.add_argument('-bodH','--bodyH', default='body_html.txt', help='html body of Message')
    parser.add_argument('-sigP','--signatureP',default='signature_plain.txt', \
                        help='Plain Signature for ending Message')
    parser.add_argument('-sigH','--signatureH',default='signature_html.txt', \
                        help='Html Signature for ending Message')
    parser.add_argument('-html','--html', default = 'False', help = 'True if msg is html format')
    parser.add_argument('-p','--pause', default = 6, type= int, help = 'Pause timing between each email')
    parser.add_argument('-dom','--domain', default = 'auto', help = 'Specify domain of email')
    
    args = parser.parse_args()
    
    sender_email = args.sender
    password = getpass.getpass()
    receiver_file = args.receiver
    body_plain = args.bodyP
    body_html = args.bodyH
    salutation_plain = args.salutationP
    salutation_html = args.salutationH
    signature_plain = args.signatureP
    signature_html = args.signatureH
    html_flag = args.html
    pause = args.pause
    domain = args.domain
    
    main(sender_email, password, receiver_file, salutation_plain, signature_plain,\
         body_plain, salutation_html, signature_html, body_html, html_flag, pause, domain)
    
    