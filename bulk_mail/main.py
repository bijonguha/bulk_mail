# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 02:34:01 2019

@author: bijon
"""
from source.utilities import send_mail
import pandas as pd
import os

def main(sender_email, password, receiver_file, pause, domain):
    
    contacts = pd.read_excel(os.path.join('data', receiver_file))
    send_mail(sender_email, password, contacts, pause, domain)
        
if __name__ == "__main__":
    import argparse
    import getpass

    parser = argparse.ArgumentParser()
    parser.add_argument('sender',metavar='SENDER', help='Sender email address')
    parser.add_argument('-re','--receiver', default='contacts.xlsx', help='Receiver excel file')
    parser.add_argument('-p','--pause', default = 6, type= int, help = 'Pause timing between each email')
    parser.add_argument('-dom','--domain', default = 'auto', help = 'Specify domain of email')
    
    args = parser.parse_args()
    
    sender_email = args.sender
    password = getpass.getpass()
    receiver_file = args.receiver
    pause = args.pause
    domain = args.domain
    
    main(sender_email, password, receiver_file, pause, domain)   
    