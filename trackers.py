from datetime import datetime

class CurrencyTracker:
    """CurrencyTracker stores information on a currency exchange rate"""

    def __init__(self, currencies, rate):
        self.CURRENCIES = currencies
        self.created = datetime.now()
        self.updated = datetime.now()
        self.all_time_high = rate
        self.last_high = rate
        self.all_time_low = rate
        self.last_low = rate
        seld.data = [rate]

    def add_rate(self, rate):
        self.data.append(rate)

        if rate[1] > self.last_high[1]:
            self.last_high = rate

            if rate[1] > self.all_time_high[1]:
                self.all_time_high = rate

        elif rate[1] < self.last_low:
            self.last_low = rate

            if rate[1] < self.all_time_low[1]:
                self.all_time_low = rate

        self.updated = datetime.now()

    def get_current_rate(self):
        return self.data[-1]

    def get_all_time_high(self):
        return self.all_time_high

    def get_last_high(self):
        return self.last_high

    def get_all_time_low(self):
        return self.all_time_low

    def get_last_low(self):
        return self.last_low

    def get_currencies(self):
        return self.CURRENCIES

    def get_created(self):
        return self.created
