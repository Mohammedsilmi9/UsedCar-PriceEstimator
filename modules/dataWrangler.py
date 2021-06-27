import pandas as pd
import numpy as np
from scipy import stats
# All raw data is scarpped and loaded into a file directory where it can be loaded
# into a data frame which could be passed to the Process function. 
# first parameter is a a pandas DataFrame.
# second parameter is optional used to process  specific make&model combo for the available vehicles
# Process returns a cleaned, unscaled ,includes no nulls , proper type , no duplicate and ready to scale data.
def Process(df,makemodel=0):

    df= df[df['price:'].notna()]
    df['Make&Model'] = df[['make:', 'model:']].apply(lambda x: ' '.join(x), axis=1)
    if(makemodel!=0):
        df=df[df['Make&Model']==makemodel]
        df=df[['year:','score:','odometer:',
               'cylinders:','price:']]
    else:
        df=df[['Make&Model','year:','score:','odometer:',
               'cylinders:','price:']]
    df=df.drop_duplicates()
    df=df.reset_index(drop=True)
    return df

def Spell(df_):
       
    df_= df_[df_['price:'].notna()]
    df_['make:'].replace(['mazda','MAZDA'],'mazda',inplace=True)
    df_['make:'].replace(['MITSUBISHI'],'mitsubishi',inplace=True)
    df_['make:'].replace(['MERCEDS','mercedes','Mercedes-benz','Mercedez','Mersedes','mbz','Mbz',
                          'mercedez','mercedes-benz','Mercedes',
                          'Benz','MERCEDES','Merceds','MERCEDES-BENZ',
                          'Mercedes-Benz','mersedes'],'mercedes-benz',inplace=True)
    df_['make:'].replace([ 'Cevrolet','Chaey','Chebrolet','Chevelle','Chevorlet','Chevroler',
                          'Chevrolet','Chevrolete','Chevy.','chevrolet','Chverolet','Shevrolet',
                          'chevrolet','Chevi','CHEVY','Chevrolet',
                          'chevorlet','chevy','CHEVRLET','Cheverolet','Chevy','Chev',
                          'CHEVROLET','chev'],'chevrolet',inplace=True)
    df_['make:'].replace(['volkseagen','volkswagon','volkwagen', 'Volkswagon',
                          'Volkswangen','Volkwagen','volkswagen',
                          'Vw','VW','vw','VOLKSWAGEN','V.W'],'volkswagen',inplace=True)
    df_['make:'].replace(['Toyota','TOYOYA','toyta','Toyot','Toyoda','TOYOTA',
                          'toyota'],'toyota',inplace=True)
    df_['make:'].replace(['Mini','MINI'],'mini',inplace=True)
    df_['make:'].replace(['Isuzu','Izusu','Izuzu','izuzu','isuzu'],'isuzu',inplace=True)
    df_['make:'].replace(['huyndai','hyndai','hynduia','Hyuandi','Hunday','hundai','hyundia',
                          'HYUNDAI'],'hyundai',inplace=True)
    df_['make:'].replace(['Bmw','bimmer','Bmw'],'bmw',inplace=True)
    df_['make:'].replace(['Audi','AUDI'],'audi',inplace=True)
    df_['make:'].replace(['LEXUS','Lexus'],'lexus',inplace=True)
    df_['make:'].replace(['KIA','Kia'],'kia',inplace=True)
    df_['make:'].replace(['Ford','FORD','for'],'ford',inplace=True)
    df_['make:'].replace(['HUMMER','Hummer','hummer','Gmc','GMC','Gmc'],'gmc',inplace=True)
    df_['make:'].replace(['HONDA','Houda','honda'],'Honda',inplace=True)
    df_['make:'].replace(['jeep','Jeeb','JEEP'],'Jeep',inplace=True)
    df_['make:'].replace(['audi','AUDI'],'Audi',inplace=True)
    df_['make:'].replace(['VOLVO', 'volvo'],'Volvo',inplace=True)
    df_['make:'].replace(['Infinti','infinti','INFINITI','infiniti',
                          'infinity'],'Infinity',inplace=True)
    df_['make:'].replace(['FIAT', 'fiat'],'Fiat',inplace=True)
    df_['make:'].replace(['Nissin','NISSAN','Nissan'],'nissan',inplace=True)
    df_['make:'].replace(['PORSCHE','porsche'],'Porsche',inplace=True)
    df_['make:'].replace(['model','Model','TESLA','TELSA','Tesla'],'tesla',inplace=True)
    df_['make:'].replace(['alfa Romeo','Alfa','alfa'],'Alfa Romeo',inplace=True)
    df_['make:'].replace(['land-rover','LANDROVER','Rover','rover','land','Land rover',
                          'land rover'],'land rover',inplace=True)
    df_['make:'].replace([ 'chryler','chrystler','chyrsler','chysler',
                          'chrysler','CRYSLER','Cheysler'],'chrysler',inplace=True)
    df_['make:'].replace(['pontaic','pontiac'],'pontiac',inplace=True)
    
    df_['model:'].replace(['Rav 4','rav 4'],'rav4',inplace=True)

    df_['make:']=df_['make:'].apply(lambda x: x.lower())
    df_['model:']=df_['model:'].apply(lambda x: x.lower())
    df_['trim:'].fillna('', inplace=True)
    
    df_['trim:']=df_['trim:'].apply(lambda x: x.lower() if (type(x)=='str') else x)
    df_['model:']=df_['model:'].apply(lambda x: x.replace('-',""))
    df_['model:']=df_['model:'].apply(lambda x: x.replace(',',""))
    df_['model:']=df_['model:'].apply(lambda x: x.replace('.',""))
    df_['model:']=df_['model:'].apply(lambda x: x.replace(' ',""))
    df_['model:'] = np.where(df_['model:'] == 'benz', df_['trim:'], df_['model:'])
    df_['model:'] = np.where(df_['model:'] == 'model', df_['trim:'], df_['model:'])
   
    
    return df_

def Replace(df):
    df= df[df['price:'].notna()]
    df['year:']=df['year:'].astype(int)
    df['year:']=df['year:'].apply(lambda x:(2022-x))
    df['price:']=df['price:'].astype(int)
    df=df.drop_duplicates()
    
    
    df['condition:']=df['condition:'].fillna("good")
    df['cylinders:']=df['cylinders:'].fillna("4")
    df['cylinders:']=df['cylinders:'].replace('other','4')
    df['cylinders:']=df['cylinders:'].astype(int)
    df=df.drop_duplicates()
    cleanup_nums ={
    "condition:": {"new":2,"good": 1, "excellent": 2,"like": 2,"fair": 0,"salvage": 0},
     "transmission:": {"automatic": 1, "manual": 2, "other":3 },
    "status:":{"clean": 1, "salvage": 0, "missing":0,"lien":0,"parts":0,"rebuilt":0},
    "drive:":{"4wd": 3, "rwd": 2, "fwd":1},
    "fuel:":{'electric':5,"gas": 4, "diesel": 3, "hybrid":2,"other":1}}
    df= df.replace(cleanup_nums)
    df['score:']=df['condition:']+df['status:']
    
    col_drop=['condition:','status:','trim:',
              'color:','fuel:','type:','drive:','transmission:']
    df.drop(columns=col_drop, inplace=True)
    df=df.reset_index(drop=True)
    
    return df    

def Outliers_light(df): 
    df=df[df['price:']>999]
    df=df[df['odometer:']>1000]
    df=df[df['odometer:']<500000]
    df['price:']=np.log2(df['price:'])
    cyl_min=df['cylinders:'].value_counts().min()
    cyl_max=df['cylinders:'].value_counts().max()
    
    if((cyl_min/cyl_max)<(0.2)or(cyl_min/cyl_max==1)):
        df.drop(columns='cylinders:',axis=1,inplace=True)
        
    return df

def delete_outliers(df):
    try:
        m, b = np.polyfit(df['year:'], df['price:'], 1)
    except:
        m, b = np.polyfit(df['year:'], df['price:'], 1)
    df_new=df
    for x,y in zip(df['year:'], m*df['year:']+ b-1.5):
        left=x
        bottom=y
        multi_outliers = df_new[(df_new['price:'] <bottom) & (df_new['year:'] < left)]
        df_new=df_new[(~df_new.isin(multi_outliers) )]
    for x,y in zip(df['year:'], m*df['year:']+ b+1.5):
        right=x
        top=y
        multi_outliers2 = df[(df['price:'] >top) & (df['year:'] > right) ]
        df_new=df_new[(~df_new.isin(multi_outliers2) )]
        df_new=df_new.dropna()
    return df_new

def compare_2vehicles(vehicle1,vehicle2,frame):
    df=Spell(frame)
    df_all=Replace(df)
    df_1=Process(df_all,vehicle1)
    df_2=Process(df_all,vehicle2)
    df_1=Outliers_light(df_1)
    df_1=delete_outliers(df_1)
    df_2=Outliers_light(df_2)
    df_2=delete_outliers(df_2)
    
    
    df1_yearGrouped=df_1.groupby("year:",axis=0).agg({'price:' : np.mean,'odometer:' : (np.mean),'score:':np.mean})
    df2_yearGrouped=df_2.groupby("year:",axis=0).agg({'price:' : np.mean,'odometer:' : (np.mean),'score:':np.mean})
    df1_yearGrouped['price:']=2**df1_yearGrouped['price:']
    df2_yearGrouped['price:']=2**df2_yearGrouped['price:']
    df1_yearGrouped.reset_index(inplace=True)
    df2_yearGrouped.reset_index(inplace=True)
    df1_yearGrouped['year:']=df1_yearGrouped['year:'].apply(lambda x:int(2022-x))
    df2_yearGrouped['year:']=df2_yearGrouped['year:'].apply(lambda x:int(2022-x))
    merged_df=df1_yearGrouped.merge(df2_yearGrouped, how='inner', on='year:')
    merged_df=merged_df[["year:","score:_x","odometer:_x","price:_x","score:_y","odometer:_y","price:_y"]]
    merged_df.rename(columns={"year:":"Year",
                          "score:_x":vehicle1+" score",
                          "odometer:_x":vehicle1+" odometer",
                          "price:_x":vehicle1+" price",
                          "score:_y":vehicle2+" score",
                          "odometer:_y":vehicle2+" odometer",
                          "price:_y":vehicle2+" price"
                          },inplace=True)
    return merged_df





    