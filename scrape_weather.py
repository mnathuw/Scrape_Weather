"""
Create a class to scrape Winnipeg weather data from the Environment Canada website.
By: Ha Phuong Le
"""
from html.parser import HTMLParser
import urllib.request
from datetime import datetime
import logging

class WeatherScraper(HTMLParser):
    """
    Use the Python HTMLParser class to scrape weather data from the website
    By: Ha Phuong Le
    """
    def __init__(self, input_time):
        """
        Initialize the attributes
        By: Ha Phuong Le
        """
        try:
            HTMLParser.__init__(self)

            self.year = input_time.strftime("%Y")
            self.month = input_time.strftime("%m")

            # a dictionary of weather data
            self.weather = {}

            # a flag to indicate whether the date has available data
            self.available_date = True

            start_url = "https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2020&Day=1&"
            values = {"Year": input_time.strftime("%Y"), "Month": input_time.strftime("%-m")}
            self.final_url = start_url + urllib.parse.urlencode(values) + "#"

            self.date = ""
            self.is_body = False
            self.is_tr = False
            self.is_th = False
            self.is_date = False
            self.is_weather = False
            self.valid_date = False
            self.i = 1
            self.missing_data = False
            self.first_check = True
        except Exception as exception:
            logging.error(f"WeatherScraper:__init__: {exception}")

    def handle_starttag(self, tag, attrs):
        """
        Check and handle the start tags that need to be used
        By: Ha Phuong Le
        """
        try:
            if tag == "tbody":
                self.is_body = True

            if self.is_body and tag == "tr":
                self.is_tr = True

            if self.is_tr and tag == "th":
                self.is_th = True

            if self.is_th and tag == "abbr":
                self.is_date = True
                self.valid_date = True

            if self.is_tr and tag == "td" and self.i <= 3:
                self.is_weather = True

            # process available_date
            if self.valid_date and self.first_check:
                for attr in attrs:
                    try:
                        if "title" in attr:
                            actual_date = datetime.strptime(attr[1], "%B %d, %Y")
                            self.available_date = actual_date.strftime("%Y") == self.year and actual_date.strftime("%m") == self.month
                    except Exception as exception:
                        logging.error(f"WeatherScraper:handle_starttag:loop: {exception}")

                self.first_check = False

        except Exception as exception:
            logging.error(f"WeatherScraper:handle_starttag: {exception}")

    def handle_endtag(self, tag):
        """
        Check and handle the end tags that need to be used
        By: Ha Phuong Le
        """
        try:
            if tag == "tbody":
                self.is_body = False

            if tag == "tr":
                self.is_tr = False
                self.valid_date = False
                self.i = 1

            if tag == "th":
                self.is_th = False

            if tag == "abbr":
                self.is_date = False

            if tag == "td":
                self.i += 1
                self.is_weather = False
        except Exception as exception:
            logging.error(f"WeatherScraper:handle_endtag: {exception}")

    def handle_data(self, data):
        """
        Process data that needs to be used
        By: Ha Phuong Le
        """
        try:
            if self.is_date:
                if self.missing_data:
                    del self.weather[self.date]
                    self.missing_data = False

                # Check if the data is a date
                try:
                    int(data)

                    self.date = self.year + "-" + self.month + "-" + data
                    self.weather[self.date] = {}
                except ValueError:
                    self.valid_date = False

            if self.is_weather and self.valid_date:
                if self.i == 1:
                    try:
                        self.weather[self.date]["Max"] = float(data)
                    except ValueError:
                        self.missing_data = True

                if not self.missing_data and self.i == 2:
                    try:
                        self.weather[self.date]["Min"] = float(data)
                    except ValueError:
                        self.missing_data = True

                if not self.missing_data and self.i == 3:
                    try:
                        self.weather[self.date]["Mean"] = float(data)
                    except ValueError:
                        self.missing_data = True

        except Exception as exception:
            logging.error(f"WeatherScraper:handle_data: {exception}")

    def load_data(self):
        """
        Scrape weather data from given page
        By: Ha Phuong Le
        """
        try:
            with urllib.request.urlopen(self.final_url) as response:
                html = str(response.read())

            self.feed(html)
        except Exception as exception:
            logging.error(f"WeatherScraper:load_data: {exception}")
