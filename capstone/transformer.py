import pymongo
import numpy as np
import pandas as pd
import tkinter as tk
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from pymongo import MongoClient
from statistics import mean
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from tkinter import messagebox

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
df.columns = headers
## Remove duplicates based on the film ID, keeping the most recent version
df.drop_duplicates(subset='id', keep='last', inplace=True)
## Set dependent variable (revenue or popularity)
dependent_variable = 'revenue'

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
#normalise('budget')
#normalise('popularity')
#normalise('runtime')
#normalise('vote_average')
#normalise('vote_count')
dummy('adult')
dummy('genres')
dummy('original_language')
dummy('production_companies')
dummy('production_countries')
dummy('status')
dummy('year')
dummy('month')
## Drop rows with revenue of 0 (incomplete data)
df = df[df.revenue != 0]
## Remove columns that can't logically affect revenue
df.drop(columns=['_id', 'id', 'release_date', 'spoken_languages', 'title'], inplace=True)

## Determine features with good correlation (closer to 1 or -1 is best)
cor = df.corr()
## Absolute value to remove negative
cor_target = abs(cor[dependent_variable])
## Acceptance factor (closer to 1 being stricter selection of variables)
acceptance_factor = 0.5
relevant_features = cor_target[cor_target>acceptance_factor]
## Set independent variables according to those determined above
independent_variables = list(relevant_features.index)
## Remove dependent variable from list
if dependent_variable in independent_variables:
	independent_variables.remove(dependent_variable)

## Set x and y for modelling
x = df[independent_variables]
y = df[dependent_variable]

## Create training and testing splits
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

## Model using training data
model = lm.fit(x_train, y_train)

## Accuracy based on test data, via cross-validation
print(mean(cross_val_score(model, x_test, y_test, cv=3)))

## Equation for revenue based off of selected features
equation = dependent_variable + ' = '
index = 0
for coef in model.coef_:
	equation = equation + str(int(coef)) + ' * ' + independent_variables[index] + ' + '
	index += 1
equation = equation + str(int(model.intercept_))

print(equation)

## Make equation pop-up for Nifi flow
root = tk.Tk()
root.withdraw()
messagebox.showwarning('Revenue Equation', equation)
