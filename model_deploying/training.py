#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# parameters
n_splits = 5
C = 1.0 
output_file = f'model_C={C}.bin'  #定义一个字符串变量 output_file，用来存放文件名。


# data preparation

df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv') 

df.columns = df.columns.str.lower().str.replace(' ','_')

categorical_columns = list(df.dtypes[df.dtypes == 'str'].index)

for c in categorical_columns:
    df[c] = df[c].str.lower().str.replace(' ','_')

df.totalcharges = pd.to_numeric(df.totalcharges, errors='coerce')
df.totalcharges = df.totalcharges.fillna(0)

df.churn = (df.churn == 'yes').astype(int)

print("=" * 50)  
print("快速检查数据集空值:")
print("=" * 50)
print(df.isnull().sum())


df_full_train,df_test = train_test_split(df, test_size=0.2, random_state=1)

#len(df_full_train),len(df_test)

df_train,df_val = train_test_split(df_full_train, test_size=0.25, random_state=1)

#len(df_full_train),len(df_test),len(df_train),len(df_val)

y_train = df_train.churn.values 
y_val = df_val.churn.values 
y_test = df_test.churn.values 

categorical = ['gender', 'seniorcitizen', 'partner', 'dependents','phoneservice', 'multiplelines', 'internetservice',
       'onlinesecurity', 'onlinebackup', 'deviceprotection', 'techsupport',
       'streamingtv', 'streamingmovies', 'contract', 'paperlessbilling','paymentmethod']

numerical = ['tenure','monthlycharges','totalcharges']


# training
def train(df_train, y_train,C=1.0):
    dicts = df_train[categorical + numerical].to_dict(orient='records')
    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform(dicts)
    model = LogisticRegression(C=C,solver='liblinear',max_iter=1000)
    model.fit(X_train, y_train)

    return dv, model


def predict(df_train, dv, model):
    dicts = df_train[categorical + numerical].to_dict(orient='records')
    X = dv.transform(dicts)
    y_pred = model.predict_proba(X)[:,1]
    return y_pred 


# cross-validation
print('cross-validation, C=%s' % C)
scores = []
kfold = KFold(n_splits=n_splits, shuffle=True, random_state=1)
fold = 0

for train_idx,val_idx in kfold.split(df_full_train):
        df_train = df_full_train.iloc[train_idx]
        df_val =  df_full_train.iloc[val_idx]
        y_train = df_train.churn.values
        y_val = df_val.churn.values

        dv,model = train(df_train, y_train ,C=C) 
        y_pred = predict(df_val,dv,model)
        auc =  roc_auc_score(y_val,y_pred)
        scores.append(auc)
        print(f'auc on fold {fold} is {auc}')
        fold += 1

print('validation results:')
print('C=%s mean auc is %.3f +-  auc std is %.3f' % (C, np.mean(scores), np.std(scores)))



# training the final model 
print('training the final model')
dv,model = train(df_full_train, df_full_train.churn.values ,C=1) 
y_pred = predict(df_test,dv,model)
auc =  roc_auc_score(y_test,y_pred)
print(f'final model auc is {auc}')


# save the model
#f_out = open(output_file,'wb')  #用 Python 内置的 open 函数打开一个文件,wb'：代表 Write Binary（以二进制模式写入）
#pickle.dump((dv,model),f_out)  #模型数据就已经被写入到 f_out 指向的文件中了 
#f_out.close()            # 关闭刚才打开的文件

with open(output_file, 'wb') as f_out:
    pickle.dump((dv, model), f_out)

print('the model is saved to', output_file)








