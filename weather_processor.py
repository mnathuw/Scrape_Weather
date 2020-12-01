"""
Create a processor to handle user inputs and execute WeatherScraper.
By: Ha Phuong Le
"""
from datetime import datetime
import logging
from dateutil.relativedelta import relativedelta
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations

class WeatherProcessor:
    """
    Prompt user for weather process selection and execute all the tasks
    By: Ha Phuong Le
    """
    def __init__(self):
        """
        Initialize the attributes
        By: Ha Phuong Le
        """
        try:
            # Scrape weather data
            self.today = datetime.now()
            self.scraper = WeatherScraper(self.today)

            # Initialize database
            self.database = DBOperations("weather.sqlite")
            self.database.initialize_db()

            # Access plot operator
            self.plot = PlotOperations()

            # Create log file
            logging.basicConfig(filename='errors.log', filemode='w', level=logging.ERROR)
        except Exception as exception:
            logging.error(f"WeatherProcessor:__init__: {exception}")

    def get_weather(self):
        """
        Present user with a menu of choices and get the user selection
        By: Ha Phuong Le
        """
        try:
            print("Download a full set of weather data or Update the current dataset?")
            user_choice = input("Enter 'D' or 'U': ")
            while user_choice not in ('D', 'U'):
                user_choice = input("Enter 'D' or 'U': ")

            if user_choice == "D":
                print("\nDownloading started.")
                self.get_fullset()
            if user_choice == "U":
                print("\nUpdating started.")
                self.update_weather()
        except Exception as exception:
            logging.error(f"WeatherProcessor:get_weather: {exception}")

    def get_fullset(self):
        """
        Download a full set of weather data
        By: Ha Phuong Le
        """
        try:
            # Delete existing db
            self.database.purge_data()

            # Load new data
            print("\nScraping weather data from the website...")
            self.database.initialize_db()
            self.scraper.load_data()

            while self.scraper.available_date:
                try:
                    # Save data to database
                    self.database.save_data(self.scraper.weather)

                    # Load data from the next page
                    self.today -= relativedelta(months=1)

                    self.scraper = WeatherScraper(self.today)
                    self.scraper.load_data()
                except Exception as exception:
                    logging.error(f"WeatherProcessor:get_fullset:loop {exception}")

            print("\nDownloading completed.")
        except Exception as exception:
            logging.error(f"WeatherProcessor:get_fullset: {exception}")

    def update_weather(self):
        """
        Update the set of weather data
        By: Ha Phuong Le
        """
        try:
            # Get the latest date of data in db
            print("\nChecking the latest date of weather data...")
            db_date = self.database.get_latest_date()

            # Create a new db if not exists
            if db_date is None:
                self.get_fullset()
            # Update current db if exists
            else:
                latest_date = datetime.strptime(db_date, "%Y-%m-%d")

                # Update data
                print("\nScraping weather data from the website...")
                self.scraper.load_data()

                while self.today > latest_date:
                    try:
                        # Save new data to database
                        self.database.save_data(self.scraper.weather)

                        self.today -= relativedelta(months=1)

                        self.scraper = WeatherScraper(self.today)
                        self.scraper.load_data()
                    except Exception as exception:
                        logging.error(f"WeatherProcessor:update_weather:loop: {exception}")

            print("\nUpdating completed.")
        except Exception as exception:
            logging.error(f"WeatherProcessor:update_weather: {exception}")

    def get_boxplot(self):
        """
        Get user input of year range to generate the box plot
        By: Ha Phuong Le
        """
        try:
            # Get from year
            invalid_from = True
            print("\nEnter a year range of interest to generate the box plot.")
            from_year = input("From Year (YYYY): ")

            while invalid_from:
                try:
                    from_year = datetime.strptime(from_year, "%Y")
                    title_start = from_year.strftime("%Y")
                    invalid_from = False
                except ValueError:
                    from_year = input("Enter from year as YYYY: ")

            # Get to year
            invalid_to = True
            to_year = input("To Year (YYYY): ")
            while invalid_to:
                try:
                    to_year = datetime.strptime(to_year, "%Y")
                    title_end = to_year.strftime("%Y")
                    invalid_to = False
                except ValueError:
                    to_year = input("Enter to year as YYYY: ")

            # Populate dictionary of weather data
            mydict = {}
            for i in range(1, 13):
                mydict[i] = []

            while from_year.strftime("%Y") <= to_year.strftime("%Y"):
                try:
                    mean = self.database.fetch_data(from_year.strftime("%Y-%m-%d"))

                    if mean is not None:
                        mydict[int(from_year.strftime("%-m"))].append(mean)

                    from_year += relativedelta(days=1)

                except Exception as exception:
                    logging.error(f"WeatherProcessor:get_boxplot:whileloop: {exception}")

            # Generate box plot
            self.plot.display_box_plot(mydict, title_start, title_end)

            print("\nThe box plot is generated successfully.")
            self.get_choice()

        except Exception as exception:
            logging.error(f"WeatherProcessor:get_boxplot: {exception}")

    def get_lineplot(self):
        """
        Get user input of a month and a year to generate the line plot
        By: Ha Phuong Le
        """
        try:
            # Get user input
            invalid_input = True
            month_year = input("\nEnter a month and a year to generate the line plot (MM-YYYY): ")
            while invalid_input:
                try:
                    month_year = datetime.strptime(month_year, "%m-%Y")
                    invalid_input = False
                except ValueError:
                    month_year = input("Enter month and year as MM-YYYY: ")

            # Populate dictionary of weather data
            title_month = month_year.strftime("%B, %Y")
            month = (month_year.strftime("%-m"),)
            dates = []
            means = []

            while month_year.strftime("%-m") == month[0]:
                try:
                    mean = self.database.fetch_data(month_year.strftime("%Y-%m-%d"))

                    if mean is not None:
                        dates.append(month_year.strftime("%-d"))
                        means.append(mean)

                    month_year += relativedelta(days=1)

                except Exception as exception:
                    logging.error(f"WeatherProcessor:get_lineplot:whileloop: {exception}")

            # Generate line plot
            self.plot.display_line_plot(dates, means, title_month)

            print("\nThe line plot is generated successfully.")
            self.get_choice()

        except Exception as exception:
            logging.error(f"WeatherProcessor:get_lineplot: {exception}")

    def get_choice(self):
        """
        Prompt user to continue with boxplot, lineplot or exit
        By: Ha Phuong Le
        """
        try:
            print("\nPlot another chart?")
            user_choice = input("Enter 'B' for boxplot, 'L' for lineplot, or 'E' to exit: ")
            while user_choice not in ('B', 'L', 'E'):
                user_choice = input("Enter 'B', 'L' or 'E': ")

            if user_choice == "B":
                self.get_boxplot()
            if user_choice == "L":
                self.get_lineplot()
            if user_choice == "E":
                print("\nGoodbye!\n")
        except Exception as exception:
            logging.error(f"WeatherProcessor:get_choice: {exception}")

# Main
if __name__ == "__main__":
    try:
        weather_processor = WeatherProcessor()
        weather_processor.get_weather()
        weather_processor.get_boxplot()
    except Exception as exception:
        logging.error(f"main: {exception}")
