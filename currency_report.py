import sys
import pickle
import os.path
import urllib.request
from trackers import CurrencyTracker
from datetime import datetime
from decimal import Decimal
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

def main():
    file_name = 'rates_to_watch.pkl'
    email = ''
    password = ''

    if len(sys.argv) == 1:
        if os.path.isfile(file_name):
            rates_to_watch = read_file(file_name)

            for rate in rates_to_watch:
                rate.add_rate(grab_rate(rate.get_currencies()))

            send_email(rates_to_watch, email, password)
        else:
            print("Error: No currencies are being tracked.")
            print("Please run the following command:")
            print("python currency_report.py CURRENCY1 CURRENCY2")
            print("eg. python currency_report.py GBP JPY")
    elif len(sys.argv) == 3:
        valid_currencies = open('currencies.txt').read()

        if sys.argv[1] in valid_currencies and sys.argv[2] in valid_currencies:
            currencies = (sys.argv[1], sys.argv[2])
            new_tracker = CurrencyTracker(currencies, grab_rate(currencies))

            if os.path.isfile(file_name):
                rates_to_watch = read_file(file_name)
                rates_to_watch.append(new_tracker)
                write_file(file_name, rates_to_watch)
            else:
                rates_to_watch = [new_tracker]
                write_file(file_name, rates_to_watch)
        else:
            print("Error: Invalid currency codes.")
    else:
        print("Error: Invalid number of arguments. %s argument(s)." %
                (len(sys.argv)))

def read_file(file_name):
    with open(file_name, 'rb') as pkl:
        return pickle.load(pkl)

def write_file(file_name, contents):
    with open(file_name, 'wb') as pkl:
        pickle.dump(contents, pkl)

def grab_rate(currencies):
    url = ('http://finance.yahoo.com/d/quotes.csv?e=.csv&f=l1&s=%s%s=X' %
            (currencies[0], currencies[1]))
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    rate = (datetime.now(), Decimal(data[:-1]))
    print("Current rate: %s" % (str(rate[1])))
    return rate

def send_email(rates_to_watch, email, password):
    text = ""

    for rate in rates_to_watch:
        cur_rate = rate.get_current_rate()[1]

        report = """
        ----%s----
        Rate: %s
        10: %s
        100: %s
        1,000: %s
        10,000: %s
        \n
        """ % (rate.get_currencies(), cur_rate, cur_rate * 10, cur_rate * 100,
                cur_rate * 1000, cur_rate * 10000)

        text += report

    msg = MIMEText(text, 'plain')
    msg['Subject'] = "Currency Report"
    msg['To'] = email

    try:
        connection = SMTP('smtp.gmail.com')
        connection.login(email, password)
        try:
            connection.sendmail(email, email, msg.as_string())
        finally:
            connection.close()
    except Exception as e:
        print("Error: Email failed to send %s" % (str(e)))

if __name__ == '__main__':
    main()
