import imaplib
import email
from email.header import decode_header
from tkinter import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter.messagebox as mbox

root = Tk()

username = StringVar()
password = StringVar()
imap_server = StringVar()
smtp_server = StringVar()
to_address = StringVar()

listbox = Listbox(root, height=15, width=100)
listbox.pack()

def get_subjects():
    listbox.delete(0, END)
    try:
        mail = imaplib.IMAP4_SSL(imap_server.get())
        mail.login(username.get(), password.get())
        mail.select("inbox")

        result, data = mail.uid('search', None, "ALL")

        email_ids = data[0].split()
        email_ids = email_ids[-10:]

        subjects = []
        for e_id in email_ids:
            result, data = mail.uid('fetch', e_id, '(BODY[HEADER.FIELDS (SUBJECT)])')
            raw_email = data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)
            subject = decode_header(email_message['Subject'])[0][0]
            if isinstance(subject, bytes):
                listbox.insert(END, subject.decode())
            else:
                listbox.insert(END, subject)
    except Exception as e:
        mbox.showerror("Error", str(e))

def send_email():
    try:
        from_address = username.get()
        to_address_str = to_address.get()  
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address_str
        subject = listbox.get(0)  
        msg['Subject'] = "First subject: " + subject

        body = "This is the first subject of the last 10 emails: " + subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server.get(), 587)
        server.starttls()
        server.login(from_address, password.get())
        text = msg.as_string()
        server.sendmail(from_address, to_address_str, text)
        server.quit()
    except Exception as e:
        mbox.showerror("Error", str(e))

Label(root, text="Email:").pack()
Entry(root, textvariable=username).pack()
Label(root, text="Password:").pack()
Entry(root, textvariable=password, show='*').pack()
Label(root, text="IMAP Server:").pack()
Entry(root, textvariable=imap_server).pack()
Label(root, text="SMTP Server:").pack()
Entry(root, textvariable=smtp_server).pack()
Label(root, text="Recipient Email:").pack() 
Entry(root, textvariable=to_address).pack()
Button(root, text="Get subjects", command=get_subjects).pack()
Button(root, text="Send first subject", command=send_email).pack()

root.mainloop()
