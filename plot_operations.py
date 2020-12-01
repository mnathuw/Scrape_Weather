"""
Create a plot_operations.py module with a PlotOperations class inside.
By: Ha Phuong Le & Nguyen Anh Thu Mai
"""
import logging
import matplotlib.pyplot as plt

class PlotOperations:
    """
    Use Python matplotlib to create a basic boxplot or lineplot of mean temperatures in a date range
    """
    def __init__(self):
        """
        Initialize the attributes
        By: Nguyen Anh Thu Mai
        """
        try:
            self.title = ""
            self.label = ""
        except Exception as exception:
            logging.error(f"PlotOperations:__init__:{exception}")

    def display_box_plot(self, mydict, from_year, to_year):
        """
        Display a box plot for mean temperatures in a range of years
        By: Nguyen Anh Thu Mai
        """
        try:
            self.title = f'Monthly Temperature Distribution for: {from_year} to {to_year}'
            location = 'center'
            font_dict = {'fontsize': 14, 'fontweight': 8.2,
                        'verticalalignment': 'baseline',
                        'horizontalalignment': location}
            plt.title(self.title, fontdict=font_dict, loc=location)
            plt.ylabel('Temperature (Celsius)')
            plt.xlabel('Month')

            # mean temperatures in a range of years
            means = []

            for value in mydict.values():
                try:
                    means.append(value)
                except Exception as exception:
                    logging.error(f"PlotOperations:display_box_plot:loop: {exception}")

            # Create the box plot
            plt.boxplot(means)
            plt.show()

        except Exception as exception:
            logging.error(f"PlotOperations:display_box_plot: {exception}")

    def display_line_plot(self, dates, means, month):
        """
        Display a line plot of mean temperature in a particular month
        By: Ha Phuong Le
        """
        try:
            self.label = 'Temperature (Celsius)'

            plt.plot(dates, means)
            plt.xlabel('Day')
            plt.ylabel(self.label)
            plt.title('Daily Temperature Distribution for: ' + month)
            plt.show()
        except Exception as exception:
            logging.error(f"PlotOperations:display_line_plot: {exception}")
