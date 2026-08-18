
import pickle
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# parameters
C = 1.0 
model_file = f'model_C={C}.bin'


#  load the model to pickle
with open(model_file, 'rb') as f_in:
   dv, model =  pickle.load(f_in)



# 假设这个客户是新的用户信息
customer = {
'gender': 'female',
'seniorcitizen': 0,
'partner': 'yes',
'dependents': 'no',
'phoneservice': 'no',
'multiplelines': 'no_phone_service',
'internetservice': 'dsl',
'onlinesecurity':'no',
'onlinebackup': 'yes',
'deviceprotection':'no',
'techsupport':'no',
'streamingtv':'no',
'streamingmovies':'no',
'contract':'month-to-month',
'paperlessbilling': 'yes',
'paymentmethod':'electronic_check',
'tenure': 1,
'monthlycharges': 29.85,
'totalcharges': 29.85
}

print('input the customer data:', customer)
X = dv.transform([customer])
y_pred = model.predict_proba(X)[:,1]

print(f'the probability of churn is {y_pred}')

