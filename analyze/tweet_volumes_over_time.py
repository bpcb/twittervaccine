# Ben Brooks
# Plotting tweet volumes over time for 2014 data.

import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

from db import get_database_connection

import datetime as DT
from matplotlib import pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker
from collections import defaultdict
import numpy as np

query_2014 = 'SELECT created_at FROM tweets_2014'
query_2009 = 'SELECT timestamp FROM tweets_tweet'

def execute_query(query):
    conn = get_database_connection(port = 2001)
    cursor = conn.cursor()

    # Select all dates from 2014 tweets table.
    cursor.execute(query)

    # Results are returned as a tuple of tuples; making a list of tuples instead.
    results = cursor.fetchall()
    results_list = [x[0] for x in results]
    
    cursor.close()
    conn.close()

    return results_list
    
def parse_2009(results_list):
     # Counting the number of tweets for each day.
    date_freq = defaultdict(int)
    for date in results_list:
        date_string =  str(date.month) + ' ' + str(date.day)
        
        date_freq[date_string] += 1   
    
    return date_freq
    
def create_data_2009(date_freq_2009):
    data = [(DT.datetime.strptime(date, '%m %d'), value) for (date, value) in date_freq_2009.items()]
    data.sort(key = lambda tup: tup[0])
    x = [dates.date2num(date) for (date, value) in data]
    y = [value for (date, value) in data]
    
    return x, y

def parse_2014(results_list):
    # Counting the number of tweets for each day.
    date_freq = defaultdict(int)
    for date in results_list:
        # Date field starts looking like this: "Tue Apr 15 17:38:49 +0000 2014"
        # and ends looking like this: "Tue Apr 15 2014"
        date_list = date.split()
        del date_list[3:6]
        date_trimmed = " ".join(date_list)
        
        date_freq[date_trimmed] += 1
        
    return date_freq

def create_data_2014(date_freq_2014):
    # Converting into datetime format and sorting by date.
    # Creating lists of x (time) and y (tweet count) for plot.
    data = [(DT.datetime.strptime(date, '%a %b %d'), value) for (date, value) in date_freq_2014.items()]
    data.sort(key = lambda tup: tup[0])
    x = [dates.date2num(date) for (date, value) in data]
    y = [value for (date, value) in data]
    
    return x, y

def plot(x_2009, y_2009, x_2014, y_2014):
    fig, ax = plt.subplots()
    
    # There was a hole in data collection in the 2014 data. 
    # Separating into two lines for clarity.
    ax.plot(x_2014[0:7], y_2014[0:7], 'b-', label = "2014 data")
    ax.plot(x_2014[8:], y_2014[8:], 'b-')
    
    # A fraction of tweets were collected in January. Removing these from figure for clarity.
    ax.plot(x_2009[19:], y_2009[19:], 'r-', label = "2009 data")
    ax.plot(x_2009[19:], y_2009[19:], 'r-')
    
    ax.xaxis.set_major_locator(dates.MonthLocator())
    ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday = 15))

    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))

    ax.set_xlim([DT.datetime.date(DT.datetime.strptime('Apr 01', '%b %d')), DT.datetime.date(DT.datetime.strptime('Dec 31', '%b %d'))])

    for tick in ax.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('center') 
    
    plt.legend()
    plt.grid()   
    plt.ylabel('Number of vaccination-related tweets per day')
    plt.savefig('./compare_2009_2014_tweet_volumes.png')

def main():
    results_list_2009 = execute_query(query_2009)
    date_freq_2009 = parse_2009(results_list_2009)
    x_2009, y_2009 = create_data_2009(date_freq_2009)

    results_list_2014 = execute_query(query_2014)
    date_freq_2014 = parse_2014(results_list_2014)
    x_2014, y_2014 = create_data_2014(date_freq_2014)    
    
    plot(x_2009, y_2009, x_2014, y_2014)

if __name__ == '__main__':
    main()