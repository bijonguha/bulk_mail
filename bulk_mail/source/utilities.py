import smtplib, ssl, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(sender_email, password, contacts, subject,\
              salutation, body_plain, body_html, html, pause, domain):
    
    #Check for email id domain for connecting to right smtp_server
    if (domain == 'auto'):
        #If domain is auto, email id should have ending gmail.com or outlook.com
        if(sender_email.split('@')[1] == 'gmail.com'):
            smtp_server = "smtp.gmail.com"
        elif(sender_email.split('@')[1] == 'outlook.com'):
            smtp_server = "smtp-mail.outlook.com"
        else: 
            print('Email id domain unknown, please CHECK spelling or enter CORRECT email id')
            return -1
    
    elif (domain == 'gmail' or domain == 'outlook'):
        #if custom domain is used, email id should be from outlook/Microsoft and gmail/gsuite
        if(domain == 'gmail'):
            smtp_server = "smtp.gmail.com"
        else :
            smtp_server = "smtp-mail.outlook.com"
            
    else:
        print('Email id domain unknown, please CHECK spelling or enter CORRECT email id')
        return -1        
    
    
    port = 587 # For starttls
    context = ssl.create_default_context() # Create a secure SSL context
    
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() 
        server.starttls(context=context) # Secure the connection
        server.ehlo() 
        server.login(sender_email, password)    
        print('Authentication successful, Logged in')
        for i in range(len(contacts)):
            tic = time.time()
            
            receiver_email = contacts.loc[i,'email']# Enter receiver address
            receiver_name = contacts.loc[i,'name']
            print('Sending email to %s' %receiver_email)
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject #subject of email
            message["From"] = sender_email
            message["To"] = receiver_email

            # Create the plain-text and HTML version of your message
            text = salutation+' '+receiver_name+',\n\n'+body_plain
            part1 = MIMEText(text, "plain")
            message.attach(part1)
            
            if(html == True):
                html_doc = salutation+' '+receiver_name+',\n\n'+body_html
                part2 = MIMEText(html_doc, "html")
                message.attach(part2)
            
    
            server.sendmail(sender_email, receiver_email, message.as_string())
            time.sleep(pause)
            print('email sent !',time.time()-tic)
            
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 


    