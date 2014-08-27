# Ben Brooks
 
# Plots average state sentiment score as calculated by a logistic regression classifier vs. 
# H1N1 vaccination rates amongst high risk groups.
# Correlation r2 = 0.40


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

vac_rates = pd.read_csv('./vaccination_rates_2010.csv')
h1n1_vac_rates = pd.read_csv('./h1n1_vaccination_rates_2010.csv')
mumps_outbreaks = pd.read_csv('./mumps_incidence_2006-2013.csv')
sentiment = pd.read_csv('./state_sentiment_scores.csv')
sentiment_2014 = pd.read_csv('./state_sentiment_scores_2014.csv')
combined = pd.merge(h1n1_vac_rates, sentiment, on = 'state')

combined_outbreak = pd.merge(mumps_outbreaks, sentiment_2014, on = 'state')

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
plt.close()

x = np.arange(85, 95, 1)
m, b = np.polyfit(combined['mmr'], combined['init_target_groups'], 1)

plt.scatter(x = combined['mmr'], y = combined['init_target_groups'])
plt.grid()
plt.plot(x, m*x + b, '-', color = 'red', linewidth = 2)
plt.xlabel('MMR vaccination rate by state, 2012')
plt.ylabel('H1N1 vaccination rate in 2010 in high risk groups (%)')
plt.rcParams['xtick.major.pad'] = 8
plt.rcParams['ytick.major.pad'] = 8
plt.savefig('./mmr_v_h1n1.png')
plt.close()

remove_outliers_2009 = combined_outbreak[combined_outbreak['incidence_2009_2013'] < 5]
remove_outliers_2009 = remove_outliers_2009[remove_outliers_2009['state'] != 'Rhode Island']
x = np.arange(0.77, 0.81, 0.01)
m, b = np.polyfit(remove_outliers_2009['mean'], remove_outliers_2009['incidence_2009_2013'], 1)

plt.scatter(x = remove_outliers_2009['mean'], y = remove_outliers_2009['incidence_2009_2013'])
# plt.plot(x, m*x + b, '-', color = 'red', linewidth = 2)
plt.ylim([0,2.5])
plt.grid()
plt.xlabel('Average user sentiment score by state, 2014')
plt.ylabel('Mumps incidence per 100,000 population, 2009-2013')
plt.rcParams['xtick.major.pad'] = 8
plt.rcParams['ytick.major.pad'] = 8
plt.savefig('./mumps_v_sentiment_2009_2013.png')
plt.close()

remove_outliers_2006 = combined_outbreak[combined_outbreak['incidence_2006_2013'] < 100]

plt.scatter(x = remove_outliers_2006['mean'], y = remove_outliers_2006['incidence_2006_2013'])
plt.grid()
plt.xlabel('Average user sentiment score by state, 2014')
plt.ylabel('Mumps incidence per 100,000 population, 2006-2013')
plt.rcParams['xtick.major.pad'] = 8
plt.rcParams['ytick.major.pad'] = 8
plt.savefig('./mumps_v_sentiment_2006_2013.png')
