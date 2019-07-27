import smtplib, ssl, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(sender_email, password, contacts, subject,\
              salutation, body_plain, body_html, html, pause):

    if(sender_email.split('@')[1] == 'gmail.com'):
        smtp_server = "smtp.gmail.com"
    elif(sender_email.split('@')[1] == 'outlook.com' or 'live.com' or 'hotmail.com'):
        smtp_server = "smtp-mail.outlook.com"
    else: 
        print('Email id domain unknown')
        return -1
    
    port = 587
    context = ssl.create_default_context()
    
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)    
        print('Authentication successful')
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
                html = salutation+' '+receiver_name+',\n\n'+body_html
                part2 = MIMEText(html, "html")
                message.attach(part2)
            
    
            server.sendmail(sender_email, receiver_email, message.as_string())
            time.sleep(pause)
            print('email sent !',time.time()-tic)
            
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 


    