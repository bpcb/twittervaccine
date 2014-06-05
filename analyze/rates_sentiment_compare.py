import pandas as pd
import matplotlib.pyplot as plt

vac_rates = pd.read_csv('./vaccination_rates_2010.csv')
h1n1_vac_rates = pd.read_csv('./h1n1_vaccination_rates_2010.csv')
sentiment = pd.read_csv('./state_sentiment_scores.csv')
combined = pd.merge(h1n1_vac_rates, sentiment, on = 'state')

correlation = combined.corr()
print correlation['score']

plt.scatter(combined['score'], combined['6mo_17yr'])
plt.show()