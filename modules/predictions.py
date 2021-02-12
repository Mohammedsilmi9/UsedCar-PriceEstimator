from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV, learning_curve
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scrape_craigslist import Scrape
from dataWrangler import *
from sklearn.ensemble import RandomForestRegressor
from scipy import stats
import pandas as pd
import numpy as np


def singlePredict(lin,frame,r=25):
    link=[lin]
    raw=Scrape(link)
    df1=Spell(raw)
    df2=Replace(df1)
    df3=Process(df2)
    inputcar=df3.iloc[0,0]
    df_spelled=Spell(frame)
    df_replaced=Replace(df_spelled)
    df_=Process(df_replaced)
    make_dict=dict(df_['Make&Model'].value_counts())
    for i,x in make_dict.items():
        if(x>2 and i==inputcar):
            proccessed=Process(df_replaced,i)
            df=Outliers_light(proccessed)
            df=delete_outliers(df)
            X=df.drop(columns='price:')
            scaler = StandardScaler()
            scaler.fit(X)
            scaler.transform(X)
            y=df['price:']
            train_features, test_features, train_labels, test_labels = \
            train_test_split(X, y, test_size = 0.1, random_state = r*3)
            #n_estimators down below can be specified
            #max_depth
            rf = RandomForestRegressor(n_estimators=r*4,random_state = (r*2),max_depth=r)
            rf.fit(train_features, train_labels);
            # Calculate mean absolute percentage error (MAPE)
            y_pred=rf.predict(test_features)
            errors=np.abs((test_labels - y_pred))
            mape = 100 * (errors / test_labels)
            accuracy = 100 - np.mean(mape)
            print(f'{i} Accuracy:', round(accuracy, 2), '%.')
    if(len(df.columns)==5):
        x_feat=df3.drop(['Make&Model','price:'],axis=1)
    if(len(df.columns)==4):
        x_feat=df3.drop(['Make&Model','cylinders:','price:'],axis=1)
    x_feat=x_feat.reset_index(drop=True)
    scaler = StandardScaler()
    scaler.fit(x_feat)
    scaler.transform(x_feat)
    y_actual=df3[['price:']]
    result="predicted:",int(2**rf.predict(x_feat)[0]),"actual:",y_actual.values[0][0]
    return result
