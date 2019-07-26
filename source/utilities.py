import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(sender_email, password, receiver_email, receiver_name, subject,\
              salutation, body_plain, body_html, html):
    
    sender_email = sender_email#"fab.alwaysme@gmail.com"  # Enter sender gmail address
    receiver_email = receiver_email#"iitbguha@gmail.com"  # Enter receiver address
    password = password#'bg06071994' #password of sender's gmail

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
    
    try: 
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        return 1
    
    except smtplib.SMTPException:
        print('SMTPAuthenticationError: %s' % 'Your account name or password is\
              incorrect, please try again using the correct stuff')
        return -1


    