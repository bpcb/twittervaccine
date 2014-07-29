# Ben Brooks
# Plotting tweet volumes over time for 2014 data.

import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

from db import get_database_connection

import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num
from collections import defaultdict

conn = get_database_connection(port = 2001)
cursor = conn.cursor()

# Select all dates from 2014 tweets table.
query = 'SELECT created_at FROM tweets_2014'
cursor.execute(query)

# Results are returned as a tuple of tuples; making a list of tuples instead.
results = cursor.fetchall()
results_list = [x[0] for x in results]

cursor.close()
conn.close()

# Counting the number of tweets for each day.
date_freq = defaultdict(int)
for date in results_list:
    # Date field starts looking like this: "Tue Apr 15 17:38:49 +0000 2014"
    # and ends looking like this: "Tue Apr 15 2014"
    date_list = date.split()
    del date_list[3:5]
    date_trimmed = " ".join(date_list)
    
    date_freq[date_trimmed] += 1

# Converting into datetime format and sorting by date.
# Creating lists of x (time) and y (tweet count) for plot.
data = [(DT.datetime.strptime(date, '%a %b %d %Y'), value) for (date, value) in date_freq.items()]
data.sort(key = lambda tup: tup[0])
x = [date2num(date) for (date, value) in data]
y = [value for (date, value) in data]

fig = plt.figure()

graph = fig.add_subplot(111)

# Plot the data as a red line with round markers
graph.plot(x,y,'r-o')

# Set the xtick locations to correspond to just the dates you entered.
graph.set_xticks(x)

# Set the xtick labels to correspond to just the dates you entered.
graph.set_xticklabels(
        [date.strftime("%a %b %d %Y") for (date, value) in data]
        )

plt.show()