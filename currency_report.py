import sys
import pickle
import os.path
from trackers import CurrencyTracker

def main():
    if len(sys.argv) == 0:
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
        print("Error: Invalid number of arguments.")

def read_file(file_name):
    pkl = open(file_name)
    contents = pickle.load(pkl)
    pkl.close()
    return contents

def write_file(file_name, contents):
    pkl = open(file_name, "w")
    pickle.dump(contents, pkl)
    pkl.close

def grab_rate(currencies):

