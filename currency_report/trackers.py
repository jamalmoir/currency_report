"""
currency_report.trackers
~~~~~~~~~~~~~~~~~~~~~~~~~~

This module stores data on currency exchanges, used to track rates and
their increases, decreases and stability.
"""

from datetime import datetime
from decimal import Decimal

class CurrencyTracker:
    """The data model to store data on exchange rates"""

    def __init__(self, currencies, rate):
        """Initilaises a CurrencyTracker.

        :param currencies: A tuple containing the currencies to track.
        :param rate: A tuple containing the exchange rate at the time
        of initialisation and the corresponding timestamp
        """
        self.CURRENCIES = currencies
        self.created = datetime.now()
        self.updated = datetime.now()
        self.all_time_high = rate
        self.all_time_low = rate
        self.streak = (0,0)
        self.data = [rate]

    def add_rate(self, new_rate):
        """Adds a new rate to the rate tracker and calculates streaks
        and highs.

        :param new_rate: A tuple containing the new rate and the
        timestamp associated with it.
        """

        direction, magnitude = self.streak
        high_time, high_val = self.all_time_high
        low_time, low_val = self.all_time_low
        prev_time, prev_val = self.data[-1]
        rate_time, rate_val = new_rate

        if rate_val > high_val:
            self.all_time_high = new_rate
        elif rate_val < low_val:
            self.all_time_low = new_rate

        if direction > 0:
            if rate_val > prev_val:
                self.streak = (1, magnitude + 1)
            elif rate_val < prev_val:
                self.streak = (-1, 1)
            else:
                self.streak = (0,1)
        elif direction < 0:
            if rate_val < prev_val:
                self.streak = (-1, magnitude + 1)
            elif rate_val > prev_val:
                self.streak = (1, 1)
            else:
                self.streak = (0, 1)
        else:
            if rate_val == prev_val:
                self.streak = (0, magnitude + 1)
            elif rate_val > prev_val:
                self.streak = (1, 1)
            else:
                self.streak = (-1, 1)

        self.data.append(new_rate)
        self.updated = datetime.now()

    def get_current_rate(self):
        return self.data[-1]

    def get_all_time_high(self):
        return self.all_time_high

    def get_all_time_low(self):
        return self.all_time_low

    def get_streak(self):
        return self.streak

    def get_currencies(self):
        return self.CURRENCIES

    def get_created(self):
        return self.created
