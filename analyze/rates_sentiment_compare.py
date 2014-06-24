# Ben Brooks
 
# Plots average state sentiment score as calculated by a logistic regression classifier vs. 
# H1N1 vaccination rates amongst high risk groups.
# Correlation r2 = 0.40


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

vac_rates = pd.read_csv('./vaccination_rates_2010.csv')
h1n1_vac_rates = pd.read_csv('./h1n1_vaccination_rates_2010.csv')
sentiment = pd.read_csv('./state_sentiment_scores.csv')
combined = pd.merge(h1n1_vac_rates, sentiment, on = 'state')

correlation = combined.corr()
print "AFINN:", correlation['score_afinn']
print "Bayes:", correlation['score_bayes']
print "Logistic:", correlation['score_logistic']

x = np.arange(0.80, 0.86, 0.01)
m, b = np.polyfit(combined['score_logistic'], combined['init_target_groups'], 1)

plt.scatter(combined['score_logistic'], combined['init_target_groups'])
plt.grid()
plt.plot(x, m*x + b, '-', color = 'red', linewidth = 2)
plt.xlabel('Average user sentiment score by state')
plt.ylabel('H1N1 vaccination rate in 2010 in high risk groups (%)')
plt.rcParams['xtick.major.pad'] = 8
plt.rcParams['ytick.major.pad'] = 8
plt.savefig('./logistic_sentiment_vacc_rate.png')
