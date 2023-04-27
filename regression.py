# -*- coding: utf-8 -*-
"""Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18UANKJZCBDCX_QdXdMLQCWhx9HIzrkoz

!pip install pycaret

!pip install polygon-api-client pymongo 
!apt-get update && apt-get install -y mongodb

!pip install sqlite3

!pip install polygon-api-client pymongo 
!apt-get update && apt-get install -y mongodb

!pip install mysql-connector-python

!pip install pymysql
"""

import pandas as pd
from pycaret.regression import *
import os

import pandas as pd
import os
import numpy as np
import datetime
from pymongo import MongoClient
from sqlalchemy import create_engine

# Set up the MongoDB client and database
client = MongoClient('mongodb://localhost:27017/')
db = client["Multiple_Currency_Pairs1"]

# Set up the MySQL engine and database
my_conn = create_engine("mysql+pymysql://root@localhost/Multiple_Currency_Pairs1")

# Establishing path for the folder which contains all the csv files.
input_folder = "/content/drive/MyDrive/Spring23/DE/a"

# Get a list of all csv files in the input folder
csv_files = [csv_file for csv_file in os.listdir(input_folder) if csv_file.endswith('.csv')]

df_list = []

for csv_file in csv_files:
    # Read the csv file and only extract three required columns
    df_list.append(pd.read_csv(os.path.join(input_folder, csv_file)))

from google.colab import drive
drive.mount('/content/drive')

df = pd.concat(df_list, ignore_index=True)

regression_setup = setup(data = df, target='vw', train_size=0.7)

best = compare_models()

scores = []

for i, df_ in enumerate(df_list):
    print(csv_files[i])
    predict_model(best, data = df_)
    scores.append((csv_files[i][:-4], pull()["RMSE"][0]))
    print()

pair_errors = sorted(scores, key = lambda a: a[1])

classes = [*["Forecastable"]*3, *["Partially Forecastable"]*4, *["Non Forecastable"]*3]

data = {"Currency Pairs": [], "Errors": [], "Class": []} 

for i in range(10):
    data["Currency Pairs"].append(pair_errors[i][0])
    data["Errors"].append(pair_errors[i][1])
    data["Class"].append(classes[i])

pd.DataFrame(data).to_csv("/content/drive/MyDrive/Spring23/DE/regression_output.csv")