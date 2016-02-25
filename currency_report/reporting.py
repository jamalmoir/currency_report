"""
currency_exchange.reporting

This module contain grabs exchange rates, writes CurrencyTracker
objects to a file and emails a report to the given email.
"""

import sys
import pickle
import os.path
import urllib.request
import datetime
import decimal
from trackers import CurrencyTracker
import smtplib
import email.mime.text


def main():
    FILE_NAME = 'rates_to_watch.pkl'
    EMAIL = ''
    PASSWORD = ''

    __, currency_1, currency_2 = sys.argv
    arg_count = len(sys.argv)

    #Load trackers and record new rates to them.
    if arg_count == 1:

        #Check if tracking file exists.
        if os.path.isfile(FILE_NAME):
            rates_to_watch = read_file(FILE_NAME)

            for rate in rates_to_watch:
                rate.add_rate(grab_rate(rate.get_currencies()))
                write_file(FILE_NAME, rates_to_watch)

            send_email(rates_to_watch, EMAIL, PASSWORD)

        #Tracking file doesn't exist, tell user to add trackers.
        else:
            print("Error: No currencies are being tracked.")
            print("Please run the following command:")
            print("python currency_report.py CURRENCY1 CURRENCY2")
            print("eg. python currency_report.py GBP JPY")

    #Create new currency tracker.
    elif arg_count == 3:
        valid_currencies = open('currencies.txt').read()

        #Check if currencies are valid.
        if currency_1 in valid_currencies and currency_1 in valid_currencies:
            currencies = (currency_1, currency_2)
            new_tracker = CurrencyTracker(currencies, grab_rate(currencies))

            #Edit existing tracker file.
            if os.path.isfile(FILE_NAME):
                rates_to_watch = read_file(FILE_NAME)
                rates_to_watch.append(new_tracker)
                write_file(FILE_NAME, rates_to_watch)

            #Create new tracker file.
            else:
                rates_to_watch = [new_tracker]
                write_file(FILE_NAME, rates_to_watch)
        else:
            print("Error: Invalid currency codes.")
    else:
        print("Error: Invalid number of arguments. {count}"
              "argument(s).".format(count=arg_count))


def read_file(file_name):
    with open(file_name, 'rb') as pkl:
        return pickle.load(pkl)


def write_file(file_name, contents):
    with open(file_name, 'wb') as pkl:
        pickle.dump(contents, pkl)


def grab_rate(currencies):
    """Grabs exchange rate from Yahoo Finance.

    :param currencies: A tuple containing the currencies to get the
    rare for.
    """

    currency_1, currency_2 = currencies

    #Build request url.
    url_template = ('http://finance.yahoo.com/d/quotes.csv?e=.csv&f=l1&'
                    's={cur1}{cur2}=X')
    url = url_template.format(cur1=currency_1, cur2=currency_2)

    #Grab data from url.
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    rate = (datetime.now(), decimal.Decimal(data[:-1]))

    print("Current rate: {rate}".format(rate=str(rate[1])))

    return rate


def send_email(rates_to_watch, email, password):
    """Complies a report on tracked rates and emails them.

    :param rates_to_watch: A list of CurrencyTrackers.
    :param email: The email to send report to.
    :param password: The password for the email account.
    """

    #Create email report.
    text = ""

    for rate in rates_to_watch:
        cur_rate = rate.get_current_rate()[1]
        streak_dir, streak_mag = rate.get_streak()

        report = """
        ----{currencies}----
        Rate: {rate}
        10: {x10}
        100: {x100}
        1,000: {x1000}
        10,000: {x10000}
        \n
        """.format(currencies=rate.get_currencies(), rate=cur_rate,
                   x10=cur_rate * 10, x100=cur_rate * 100,
                   x1000=cur_rate * 1000, x10000=cur_rate * 10000)

        if streak_dir > 0:
            streak_text = ("This exchange rate has been increasing for {count}"
                           "day(s).\n"
                           ).format(count=streak_mag)
        elif streak_dir < 0:
            streak_text = ("This exchange rate has been decreasing for {count}"
                           "day(s).\n"
                           ).format(count=streak_mag)
        else:
            streak_text = ("This exchange rate has been stable for {count}"
                           "day(s).\n)").format(count=streak_mag)

        report += streak_text
        text += report

    msg = email.mime.text.MIMEText(text, 'plain')
    msg['Subject'] = "Currency Report"
    msg['To'] = email

    #Attempt to send email.
    try:
        connection = smtplib.SMTP_SSL('smtp.gmail.com')
        connection.login(email, password)
        try:
            connection.sendmail(email, email, msg.as_string())
        finally:
            connection.close()
    except Exception as e:
        print("Error: Email failed to send {error}".format(error=str(e)))

if __name__ == '__main__':
    main()
