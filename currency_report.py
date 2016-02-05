import sys
import pickle
import os.path
import urllib.request
from trackers import CurrencyTracker
from datetime import datetime

def main():
    if len(sys.argv) == 0:
        print("test")
        #TODO: currency updating and emailing
    elif len(sys.argv) == 3:
        valid_currencies = open('currencies.txt').read()

        if sys.argv[1] in valid_currencies and sys.argv[2] in valid_currencies:
            currencies = (sys.argv[1], sys.argv[2])
            new_tracker = CurrencyTracker(currencies, grab_rate(currencies))

            if os.path.isfile('rates_to_watch.pkl'):
                rates_to_watch = read_file('rates_to_watch.pkl')
                rates_to_watch.append(new_tracker)
                write_file(rates_to_watch, 'rates_to_watch.pkl')
            else:
                rates_to_watch = [new_tracker]
                write_file(rates_to_watch, 'rates_to_watch.pkl')
        else:
            print("Error: Invalid currency codes.")
    else:
        print("Error: Invalid number of arguments. %s argument(s)." % (len(sys.argv)))

def read_file(file_name):
    with open(file_name, 'rb') as pkl:
        return pickle.load(pkl)

def write_file(file_name, contents):
    with open(file_name, 'wb') as pkl:
        pickle.dump(contents, pkl)

def grab_rate(currencies):
    url = 'http://finance.yahoo.com/d/quotes.csv?e=.csv&f=l1&s=%s%s=X' % (currencies[0], currencies[1])
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    rate = (datetime.now(), data[:-1])
    print(rate)
    return rate

if __name__ == '__main__':
    main()
