"""
python-mailer.py
Author: Vishnu Ashok
Contact: thisisvishnuashok@gmail.com
         thisisvishnuashok@hotmail.com
GitHub: http://github.com/p53ud0k0d3

This is a simple email client program that can be used to send emails from Gmail and Hotmail.
You must enable "Allow less secure apps" in Gmail settings.
"""

import smtplib

def main():
    print("======")
    print("MAILER")
    print("======\n\n")
    print("1. Gmail\n2. Hotmail\n3. Exit")
    ch = int(input("Select an option: "))
    if ch == 1:
        gmail()
    elif ch == 2:
        hotmail()
    elif ch == 3:
        exit()
    else:
        print("Invalid option")

def gmail():
    print("\n")   
    uid = input("Gmail_id: ")
    pwd = input("Password: ")
    to = input("\nTo: ")
    subject = input("Subject: ")
    content = input("Message: ")
    mail_server = 'smtp.gmail.com'
    message = "\r\n".join((
        "From: %s" % uid,
        "To: %s" % to,
        "Subject: %s" % subject,
        "",
        content,
    ))
    send_mail(uid, pwd, to, message, mail_server)

def hotmail():
    print("\n")
    uid = input("Hotmail_id: ")
    pwd = input("Password: ")
    to = input("\nTo: ")
    subject = input("Subject: ")
    content = input("Message: ")
    mail_server = 'smtp.live.com'
    message = "\r\n".join((
        "From: %s" % uid,
        "To: %s" % to,
        "Subject: %s" % subject,
        "",
        content,
    ))
    send_mail(uid, pwd, to, message, mail_server)

def send_mail(uid, pwd, to, message, mail_server):
    server = smtplib.SMTP(mail_server, 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(uid, pwd)
    server.sendmail(uid, to, message)
    server.close()

if __name__ == "__main__":
    main()
