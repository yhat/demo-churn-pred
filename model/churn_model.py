
# coding: utf-8
from __future__ import division
import pandas as pd
import numpy as np

import json

from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC

from yhat import Yhat,YhatModel,preprocess,df_to_json

print "Importing data"
churn_df = pd.read_csv('churn.csv')
churn_df.columns = ['state',
'account_length',
'area_code',
'phone',
'intl_plan',
'vmail_plan',
'vmail_message',
'day_mins',
'day_calls',
'day_charge',
'eve_minutes',
'eve_calls',
'eve_charge',
'night_mins',
'night_calls',
'night_charge',
'intl_mins',
'intl_calls',
'intl_charge',
'custserv_calls',
'churn']

print "Formatting feature space"
# Isolate target data
churn_result = churn_df['churn']
y = np.where(churn_result == 'True.',1,0)

# We don't need these columns
to_drop = ['state','area_code','phone','churn']
churn_feat_space = churn_df.drop(to_drop,axis=1)

yes_no_cols = ["intl_plan","vmail_plan"]
churn_feat_space[yes_no_cols] = churn_feat_space[yes_no_cols] == 'yes'

features = churn_feat_space.columns
X = churn_feat_space.as_matrix().astype(np.float)

print "Scaling features"
# This is important
scaler = StandardScaler()
X = scaler.fit_transform(X)

print "Generating training data"
train_index, test_index = train_test_split(churn_df.index)

clf = SVC(probability=True, verbose=True)
clf.fit(X[train_index],y[train_index])

class ChurnModel(YhatModel):
    @preprocess(in_type=pd.DataFrame,out_type=pd.DataFrame)
    def execute(self,data):
        response = pd.DataFrame(data)
        charges = ['day_charge','eve_charge','night_charge','intl_charge']
        response['customer_worth'] = data[charges].sum(axis=1)
        # Convert yes no columns to bool
        data[yes_no_cols] = data[yes_no_cols] == 'yes'
        # Create feature space
        X = data[features].as_matrix().astype(float)
        X = scaler.transform(X)
        # Make prediction
        churn_prob = clf.predict_proba(X)
        response['churn_prob'] = churn_prob[:,1]
        # Calculate expected loss by churn
        response['expected_loss'] = response['churn_prob'] * response['customer_worth']
        response = response.sort('expected_loss',ascending=False)
        response = response[['customer_worth','churn_prob', 'expected_loss']]
        # Return response DataFrame
        return response

yh = Yhat(raw_input("Yhat username: "), raw_input("Yhat apikey: "), "http://sandbox.yhathq.com/")

print "Deploying model"
response = yh.deploy("PythonChurnModel",ChurnModel,globals())

print df_to_json(churn_df[:1])



