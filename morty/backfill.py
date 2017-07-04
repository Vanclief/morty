""" Tools for filling trade data """
import sys
import requests
import time
import pandas as pd
import os.path
from datetime import datetime
from numpy import nan

from requests.packages.urllib3.exceptions import InsecureRequestWarning

class Backfiller:

    def __init__(self, exchange, pair, amount, days):
        self.exchange = exchange
        self.pair = pair
        self.amount = int(amount)
        self.days = int(days)
        self.headers = {'XXX'}
        self.url = 'XXX'
        self.pem = 'certs/cert.pem'
        self.dataframe = pd.DataFrame([], columns=["Timestamp", "Avg_Buy", "Avg_Sell"])

    def day_to_timestamp(self, day):
        return 0

    def timestamp_to_date(self, timestamp):
        return 0

    def fetch_data(self, start_time_t, end_time_t):
        payload = {
            'exchange': self.exchange,
            'symbol1': self.pair[0],
            'symbol2': self.pair[1],
            'amount': self.amount,
            'start_time': start_time_t,
            'end_time': end_time_t
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        return requests.get(self.url,
                headers=self.headers,
                params=payload,
                verify=False,
                cert=self.pem
        )

    def append_data(self, data):
        data = data.json()["payload"]
        if (data == []):
            print('Error')
        else:
            print('OK')
            data_df = pd.DataFrame(data, columns=["Timestamp", "Avg_Buy", "Avg_Sell"])
            self.dataframe = self.dataframe.append(data_df)

    def save_data(self, file_name):
        self.dataframe.to_pickle(file_name)

    def load_data(self, file_name):
        data = pd.read_pickle(file_name)
        data = data.fillna(value=nan).dropna(how='any')
        print ("Loaded saved data. Ready for backtesting.")
        return data.drop_duplicates(subset=['Timestamp'], keep='last')

    def run(self):

        now = int(time.time())
        start_date = datetime.utcfromtimestamp(
                now - self.days * 86400).strftime("%Y-%m-%d")
        end_date = datetime.utcfromtimestamp(now).strftime("%Y-%m-%d")

        file_name = ('data/{:}-{:}-{:}_{:}_{:}_{:}.pkl').format(self.exchange, self.pair[0],
                self.pair[1], self.amount, start_date, end_date)
        hours = self.days * 24

        # Check if there is not a file already with the data we want

        if not(os.path.isfile(file_name)):

            for hour in range(hours, 0, -1):
                start_time = (now - (3600 * hour))
                end_time = (now - (3600 * (hour-1)))
                start_time_d = datetime.utcfromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
                end_time_d = datetime.utcfromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")
                print('Backfilling data for: {:} {:} from {:} to {:} ({:})'
                .format(self.exchange, self.pair, start_time_d, end_time_d,
                    self.amount))
                data = self.fetch_data(start_time, end_time)
                self.append_data(data)

            self.save_data(file_name)
            print ("Data saved.")

        # Load the data

        load_data = self.load_data(file_name)
        return load_data



