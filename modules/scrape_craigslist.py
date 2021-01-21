import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame
import numpy as np
import urllib.request
import requests
import os
import io

def Scrape(final_links):
    
    spec_list=[]
    title_list=[]
    price_list=[]

    for lin in final_links:
        try:
            page = requests.get(lin)
            soup = BeautifulSoup(page.text, "html.parser")
        
            spec_list.append(soup.find_all("p", {"class":"attrgroup"})[1].text.strip('\n').replace("\n"," ").split(" "))
            title_list.append(soup.find_all("p", {"class": "attrgroup"})[0].text.strip('\n'))
            price_list.append(str(soup.find("span", {"class": "price"})).strip('$').replace(',',""))
        except:
            continue
                             
    df_=pd.DataFrame(columns=['year:','make:','model:','trim:','VIN:','condition:','odometer:',
                              'cylinders:','color:','transmission:',
                              'type:','status:','drive:','fuel:','price:'])
    for i,title in enumerate(title_list):
        if(len(title.split())>=4 and not(title.split()[1].isnumeric())):
                df_.loc[f'{i}','year:']=title.split()[0]
                df_.loc[f'{i}','make:']=title.split()[1]
                df_.loc[f'{i}','model:']=title.split()[2]
                df_.loc[f'{i}','trim:']=title.split()[3]
        if(len(title.split())==3 and not(title.split()[1].isnumeric())):
                df_.loc[f'{i}','year:']=title.split()[0]
                df_.loc[f'{i}','make:']=title.split()[1]
                df_.loc[f'{i}','model:']=title.split()[2]
                df_.loc[f'{i}','trim:']= np.nan
        if(len(title.split())==4 and title.split()[1].isnumeric()):
                df_.loc[f'{i}','year:']=title.split()[0]
                df_.loc[f'{i}','make:']=title.split()[2]
                df_.loc[f'{i}','model:']=title.split()[3]
                df_.loc[f'{i}','trim:']= np.nan
        if(len(title.split())>=5 and title.split()[1].isnumeric()):
                df_.loc[f'{i}','year:']=title.split()[0]
                df_.loc[f'{i}','make:']=title.split()[2]
                df_.loc[f'{i}','model:']=title.split()[3]
                df_.loc[f'{i}','trim:']= title.split()[4]

    for i,temp in enumerate(spec_list):
        for word in temp:
            if(word=='VIN:'):
                df_.loc[f'{i}','VIN:']=temp[temp.index(word)+1]    
            if(word=='condition:'):
                 df_.loc[f'{i}','condition:']=temp[temp.index(word)+1] 
            if(word=='odometer:'):
                df_.loc[f'{i}','odometer:']=temp[temp.index(word)+1]
            if(word=='cylinders:'):
                 df_.loc[f'{i}','cylinders:']=temp[temp.index(word)+1]
            if(word=='color:'):
                 df_.loc[f'{i}','color:']=temp[temp.index(word)+1]
            if(word=='transmission:'):
                 df_.loc[f'{i}','transmission:']=temp[temp.index(word)+1]
            if(word=='type:'):
                 df_.loc[f'{i}','type:']=temp[temp.index(word)+1]
            if(word=='status:'):
                 df_.loc[f'{i}','status:']=temp[temp.index(word)+1]
            if(word=='drive:'):
                 df_.loc[f'{i}','drive:']=temp[temp.index(word)+1] 
            if(word=='fuel:'):
                 df_.loc[f'{i}','fuel:']=temp[temp.index(word)+1]
    for i,p in enumerate(price_list):
        df_.loc[f'{i}','price:']=p
        
    df_['price:']=df_['price:'].apply(lambda x: x[21:-7])
    df_['price:'] = pd.to_numeric(df_['price:'])
    df_['year:'] = pd.to_numeric(df_['year:'])
    df_['odometer:'] = pd.to_numeric(df_['odometer:'])
    
    df_final=df_.dropna(axis=0, thresh=2, subset=['year:','make:','model:','trim:'])

    return df_final