import sys
import pickle
import os.path
import csv
import urllib.request
from trackers import CurrencyTracker
from datetime import datetime

def main():
    if len(sys.argv) == 0:
        print("test")
        #TODO: currency updating and emailing
    elif len(sys.argv) == 2:
        valid_currencies = open("currencies.txt").read()

        if sys.argv[0] in valid_currencies and sys.argv[1] in valid_currencies:
            currencies = (sys.argv[0], sys.argv[1])
            new_tracker = CurrencyTracker(currencies, grab_rate(currencies))

            if os.path.isfile("rates_to_watch.pkl"):
                rates_to_watch = read_file("rates_to_watch.pkl")
                rates_to_watch.append(new_tracker)
                write_file(rates_to_watch, "rates_to_watch.pkl")
            else:
                rates_to_watch = [new_tracker]
                write_file(rates_to_watch, "rates_to_watch.pkl")
        else:
            print("Error: Invalid currency codes.")
    else:
        print("Error: Invalid number of arguments.")

def read_file(file_name):
    pkl = open(file_name, "rb")
    contents = pickle.load(pkl)
    pkl.close()
    return contents

def write_file(file_name, contents):
    pkl = open(file_name, "wb")
    pickle.dump(contents, pkl)
    pkl.close

def grab_rate(currencies):
    url = "http://finance.yahoo.com/d/quotes.csv?e=.csv&f=l1&s=%s%s=X" % (currencies[0], currencies[1])
    response = urllib2.urlopen(url)
    reader = csv.reader(response)
    rate = (datetime.now(), reader.next())
    print(rate)
    return rate
