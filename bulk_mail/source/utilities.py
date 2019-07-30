import smtplib, ssl, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

def send_mail(sender_email, password, contacts, salutation_html, body_html, \
                                          signature_html, pause, domain):
    
    res_logs = []
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

            res = [] #collecting results

            tic = time.time()
            
            receiver_email = contacts.loc[i,'email']# Enter receiver address
            receiver_name = contacts.loc[i,'name']
            print('Sending email to %s' %receiver_email)
            res.append(receiver_email)
            res.append(receiver_name)

            message = MIMEMultipart("alternative")
            message["Subject"] = contacts.loc[i,'subject'] #subject of email
            message["From"] = sender_email
            message["To"] = receiver_email
            
            # HTML version of your message
            html_doc = salutation_html.format(name=receiver_name)+'\n\n'+body_html+\
                                                     '\n\n'+ signature_html      
            part2 = MIMEText(html_doc, "html")
            message.attach(part2)
            
            try:
                server.sendmail(sender_email, receiver_email, message.as_string())
            except:
                print('Unable to send mail or Bad email id encountered at %d, Please check' %i)
                continue
            
            res.append('success')
            res_logs.append(res)

            time.sleep(pause)
            print('email sent !',time.time()-tic)

        server.quit()
        df_logs = pd.DataFrame(res_logs)
        df_logs.columns = ['email', 'name', 'status']
        return df_logs,1
           
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        print('Unable to Connect with Server Or Authentication issue -> Please try again with correct username password')
        return 0,0



    