from datetime import datetime
from decimal import Decimal

class CurrencyTracker:
    """CurrencyTracker stores information on a currency exchange rate"""

    def __init__(self, currencies, rate):
        self.CURRENCIES = currencies
        self.created = datetime.now()
        self.updated = datetime.now()
        self.all_time_high = rate
        self.all_time_low = rate
        self.streak = 0
        self.data = [rate]

    def add_rate(self, new_rate):
        self.data.append(new_rate)

        if new_rate[1] > self.all_time_high[1]:
            self.all_time_high = new_rate
        elif new_rate[1] < self.all_time_low[1]:
            self.all_time_low = new_rate

        if self.streak >= 0:
            if new_rate[1] >= self.data[len(self.data) - 2][1]:
                self.streak += 1
            else:
                self.streak = -1
        elif self.streak < 0:
            if new_rate[1] <= self.data[len(self.data) - 2][1]:
                self.streak -= 1
            else:
                self.streak = + 1

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
