! pip install --upgrade pandas

"""# Import Packages"""

import pandas as pd
import numpy as np
import seaborn as sns
import requests

"""# Importing and Extracting Data"""

# Importing simple csv
# https://github.com/fivethirtyeight/data/tree/master/forecast-review
election_df = pd.read_csv('forecast_results_2018.csv')

# Importing file with no headers and whitespace as separator
wind_df = pd.read_table('wind.data', header=None, sep='\s+')

# Importing nested json file
json_df = pd.read_json('example_2.json')

# More in-depth explanation of working with json data: https://realpython.com/python-json/
# Access data in nested json request response
r = requests.get('http://api.zippopotam.us/us/ma/belmont')
j = r.json()

print(j)
print('\nState: ' + j['state'])
for each in j['places']:
    print('Latitude of ' + j['place name'] + ': ' + each['latitude'])

"""# Tidy data"""

# Create and tidy dataset so that all values to have same units
#values_df = pd.DataFrame(columns=['values','units'])
values_data = {'values': [100, 2, 38, 25, 1000, 52, 365, 10], 'units': ['cm', 'm', 'cm', 'm', 'cm', 'm', 'mm', 'm']}
values_df = pd.DataFrame(data=values_data)
values_df

def value_conversion(series):
    if series['units'] == 'm':
        return series['values']
    elif series['units'] == 'cm':
        return series['values'] / 100
    else:
        return 0

values_df['values_in_m'] = values_df.apply(lambda x: value_conversion(x),axis=1)
values_df

"""# High Level Exploration of Data"""

# Dataset dimensions
election_df.shape

# Find the total number of na values in dataframe
election_df.isna().sum().sum()

# Last n number of observations in dataset
election_df.tail(10)

# Basic metrics of dataset
election_df.describe()

# All values of variable and counts of each level -- helpful for categorical variables
print('Branch value counts:')
print(election_df['branch'].value_counts())
print('\nWin Likelihood Category:')
election_df['category'].value_counts()

# Select subsets of data
# Reference: https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/
election_df.loc[election_df['category'] == 'Lean D'].head()

# Select subsets of data
# Reference: https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/

# Locate the last 5 observations in the dataset where a Republican won even though the categorization was that the race
# was leaning Democrat. Try adding parentheses if you're getting an error.
election_df.loc[(election_df['Republican_Won'] == 1) & (election_df['category'] == 'Lean D')].tail()

# Select subsets of data
# Reference: https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/

# Locate the 5 Democratic wins that were least likely to occur based on predictions. Try using sort_values.
election_df.loc[election_df['Democrat_Won'] == 1].sort_values(by='Democrat_WinProbability').head()

# Select subsets of data
# Reference: https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/

# Locate the 7 house races that, according the deluxe prediction model, were a forgone conclusion.
election_house = election_df.loc[(election_df['branch'] == 'House') & (election_df['version'] == 'deluxe')]
election_house['prob_diff'] = abs(election_house['Democrat_WinProbability'] - election_house['Republican_WinProbability'])
election_house.sort_values(by='prob_diff', ascending= False).head(7)



