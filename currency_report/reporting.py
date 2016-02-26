"""
currency_exchange.reporting

This module grabs exchange rates, writes CurrencyTracker
objects to a file and emails a report to the given email.
"""

import sys
import os.path
import urllib.request
import datetime
import decimal
import utils


def main():
    FILE_NAME = 'rates_to_watch.pkl'
    EMAIL = ''
    PASSWORD = ''

    arg_count = len(sys.argv)

    # Load trackers and record new rates to them.
    if arg_count == 1:

        # Check if tracking file exists.
        if os.path.isfile(FILE_NAME):
            rates_to_watch = utils.read_file(FILE_NAME)

            for rate in rates_to_watch:
                rate.add_rate(grab_rate(rate.get_currencies()))
                utils.write_file(FILE_NAME, rates_to_watch)

            report = generate_report(rates_to_watch)
            utils.send_email('Exchange Rate Report', report,
                                             EMAIL, EMAIL, PASSWORD)

        # Tracking file doesn't exist, tell user to add trackers.
        else:
            print("Error: No currencies are being tracked.")
            print("Please run the following command:")
            print("python currency_report.py CURRENCY1 CURRENCY2")
            print("eg. python currency_report.py GBP JPY")

    # Create new currency tracker.
    elif arg_count == 3:
        __, currency_1, currency_2 = sys.argv
        valid_currencies = open('currencies.txt').read()

        # Check if currencies are valid.
        if currency_1 in valid_currencies and currency_1 in valid_currencies:
            currencies = (currency_1, currency_2)
            new_tracker = trackers.CurrencyTracker(currencies,
                                                  grab_rate(currencies))

            # Edit existing tracker file.
            if os.path.isfile(FILE_NAME):
                rates_to_watch = utils.read_file(FILE_NAME)
                rates_to_watch.append(new_tracker)
                utils.write_file(FILE_NAME, rates_to_watch)

            # Create new tracker file.
            else:
                rates_to_watch = [new_tracker]
                utils.write_file(FILE_NAME, rates_to_watch)
        else:
            print("Error: Invalid currency codes.")
    else:
        print("Error: Invalid number of arguments. {count}"
              "argument(s).".format(count=arg_count))


def grab_rate(currencies):
    """Grabs exchange rate from Yahoo Finance.

    :param currencies: A tuple containing the currencies to get the
    rare for.
    """

    currency_1, currency_2 = currencies

    # Build request url.
    url_template = ('http://finance.yahoo.com/d/quotes.csv?e=.csv&f=l1&'
                    's={cur1}{cur2}=X')
    url = url_template.format(cur1=currency_1, cur2=currency_2)

    # Grab data from url.
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    rate = (datetime.datetime.now(), decimal.Decimal(data[:-1]))

    print("Current rate: {rate}".format(rate=str(rate[1])))

    return rate


def generate_report(rates_to_watch):
    """ Generates a report on tracked rates and emails them.

    :param rates_to_watch: A list of CurrencyTrackers.
    :param email: The email to send report to.
    :param password: The password for the email account.
    """

    # Create email report.
    complete_report = ""

    for rate in rates_to_watch:
        cur_rate = rate.get_current_rate()[1]
        streak_dir, streak_mag = rate.get_streak()

        one_report = """
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
            streak_report = ("This exchange rate has been increasing for"
                             "{count} day(s).\n").format(count=streak_mag)
        elif streak_dir < 0:
            streak_report = ("This exchange rate has been decreasing for"
                             "{count} day(s).\n").format(count=streak_mag)
        else:
            streak_report = ("This exchange rate has been stable for {count}"
                             "day(s).\n)").format(count=streak_mag)

        one_report += streak_report
        complete_report += one_report

    return complete_report


if __name__ == '__main__':
    main()
