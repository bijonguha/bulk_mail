import smtplib, ssl, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import os as ps

def send_mail(sender_email, password, contacts, pause, domain):
    
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
            
            body_html = open(ps.path.join('data', 'html', contacts.loc[i,'body_html']), "r").read()
            salutation_html = open(ps.path.join('data','html',contacts.loc[i,'salutation_html']), "r").read()
            signature_html = open(ps.path.join('data','html',contacts.loc[i,'signature_html']), "r").read()          
            
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
        
        l = len(df_logs)
        
        df_logs.loc[l,'email'] = ' '
        df_logs.loc[l,'name'] = ' '
        
        df_logs.loc[l+1,'email'] = 'Sender'
        df_logs.loc[l+1,'name'] = sender_email
    
        from datetime import datetime
        import os
        
        date_time = datetime.now().strftime("%m%d%Y%H%M%S")
        filename = date_time+'.csv'
        df_logs.to_csv(os.path.join('results',filename), index = False)
            
        return 1
           
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        print('Unable to Connect with Server Or Authentication issue -> Please try again with correct username password')
        return 0



    