import pymongo
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

lm = LinearRegression()

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
used_headers = ['adult', 'budget', 'original_language', 'popularity', 'revenue', 'runtime', 'status', 'vote_average', 'vote_count', 'year', 'month']
independent_variables = ['adult', 'budget', 'original_language', 'runtime', 'status', 'vote_average', 'vote_count', 'year', 'month']
df.columns = headers

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
numeric('id')
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
dummy('original_language')
dummy('status')
dummy('year')
dummy('month')

## Dependent variable for linear regression model
ylm = df['revenue']
## Independent variables for linear regression model
xlm = df[['adult', 'budget', 'original_language', 'runtime', 'status', 'vote_average', 'vote_count', 'year', 'month']]

## Fit linear regression model
ylmrm = lm.fit(xlm, ylm)
## Prediction model
ylmhat = lm.predict(xlm)

## Use training set and testing set in 3 folds to give R values for model as out-sample data not in-sample data
scores = cross_val_score(ylmrm, xlm, ylm, cv=3)

print(scores)

## Get R^2 value (result of 1 is best)
print(lm.score(xlm,ylm))

## Create train/test variables
x_train, x_test, y_train, y_test = train_test_split(xlm, ylm, test_size=0.3, random_state=0)
## Check R^2 values for each polynomial regression to determine the best fitting model (highest R^2 value)
r2tests = {}
for x in independent_variables:
	for n in range(1, 5):
		pr = PolynomialFeatures(degree=n)
		x_train_pr = pr.fit_transform(x_train[[x]])
		x_test_pr = pr.fit_transform(x_test[[x]])
		lm.fit(x_train_pr, y_train)
		r2tests["r-{0}-{1}".format(x, n)] = lm.score(x_test_pr, y_test)

print(r2tests)

## Select keys from r2tests with R values above 0.95 (if any)

