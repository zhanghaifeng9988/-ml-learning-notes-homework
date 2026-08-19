from flask import Flask, request, jsonify
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
    dv, model = pickle.load(f_in)


app = Flask('churn')


@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0, 1]
    churn = y_pred >= 0.5
    result = {
      'churn': bool(churn),
      'probability': float(y_pred)
    }
    
    return jsonify(result)

#""" result = {
#    'churn': bool(churn),
#    'probability': float(y_pred)
#  } """

# print('input the customer data:', customer)
# print(f'the probability of churn is {y_pred}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
