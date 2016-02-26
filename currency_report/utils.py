"""
currency_report.utils
~~~~~~~~~~~~~~~~~~~~~~~

This module provides utility functions that are used within currency_exchang.
"""

import pickle
import smtplib
import email.mime.text

def read_file(file_name):
    """Unpickles a file"""
    with open(file_name, 'rb') as pkl:
        return pickle.load(pkl)


def write_file(file_name, contents):
    """Pickles a file"""
    with open(file_name, 'wb') as pkl:
        pickle.dump(contents, pkl)

def send_email(subject, message, recipient, email_address, password):
    """Sends an email message via smtplib"""
    msg = email.mime.text.MIMEText(message, 'plain')
    msg['Subject'] = subject
    msg['To'] = email_address

    try:
        connection = smtplib.SMTP_SSL('smtp.gmail.com')
        with connection.login(email_address, password):
            connection.sendmail(email_address, recepient, msg.as_string())
    except Exception as e:
        print("Error sending email: {error}".format(error=str(e)))
