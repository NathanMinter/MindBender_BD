import pymongo
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from pymongo import MongoClient

## Instantiate client
mongo_uri = 'mongodb://localhost:27017'
client = MongoClient(mongo_uri)

## Select database and collection (table)
db = client['capstone_db']
tbl = db.capstone_tbl

## Convert to dataframe
df = pd.DataFrame(list(tbl.find()))

print(df)

## Create headers for dataframe
headers = ['_id', 'adult', 'budget', 'genres', 'id', 'original_language', 'popularity', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'title', 'vote_average', 'vote_count']
df.columns = headers
## Remove duplicates based on the film ID, keeping the most recent version
df.drop_duplicates(subset='id', keep='last', inplace=True)

## Converts column 'header' to numeric values (to weed out blanks)
def numeric(header):
	df[header] = pd.to_numeric(df[header], errors = 'coerce')
## Normalise columns
def normalise(header):
	df[header] = (df[header] - df[header].mean())/df[header].std()
	df[header] = df[header].fillna(df[header].mean())
## Convert categorical variables to dummy variables (0s or 1s)
def dummy(header):
	df[header] = pd.get_dummies(df[header])

## Convert release date to categories (month and year)
df['year'] = df['release_date'].str[:4]
df['month'] = df['release_date'].str[5:7]

## Convert variables as required
numeric('budget')
numeric('popularity')
numeric('revenue')
numeric('runtime')
numeric('vote_average')
numeric('vote_count')
normalise('budget')
normalise('popularity')
normalise('runtime')
normalise('vote_average')
normalise('vote_count')
dummy('adult')
dummy('genres')
dummy('original_language')
dummy('production_companies')
dummy('production_countries')
dummy('status')
dummy('year')
dummy('month')

## Remove columns that can't logically affect revenue
df.drop(columns=['_id', 'id', 'release_date', 'spoken_languages', 'title'], inplace=True)

## Plot correlation matrix
cor = df.corr()
plt.figure(figsize=(15, 15))
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()
