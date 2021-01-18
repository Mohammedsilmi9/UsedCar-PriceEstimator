import pandas as pd
import numpy as np
from scipy import stats

def Process(df_,makmod=1):
   
    df_= df_[df_['price:'].notna()]
    df_['make:'].replace(['mazda','MAZDA'],'mazda',inplace=True)
    df_['make:'].replace(['MITSUBISHI'],'mitsubishi',inplace=True)
    df_['make:'].replace(['mercedes','Mercedes-benz','Mercedez','Mersedes','mbz','Mbz',
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

    df_['make:']=df_['make:'].apply(lambda x: x.lower())
    df_['model:']=df_['model:'].apply(lambda x: x.lower())
    df_['trim:'].fillna('', inplace=True)
    df_['trim:']=df_['trim:'].apply(lambda x: x.lower())
    df_['model:']=df_['model:'].apply(lambda x: x.replace('-',""))
    df_['model:']=df_['model:'].apply(lambda x: x.replace(',',""))
    df_['model:']=df_['model:'].apply(lambda x: x.replace('.',""))
    
    
    df_['model:'] = np.where(df_['model:'] == 'benz', df_['trim:'], df_['model:'])
    #can do some model replacement of miss spelled values here before concatinating
    df_['Make&Model'] = df_[['make:', 'model:']].apply(lambda x: ' '.join(x), axis=1)
    df=df_[['year:','Make&Model','trim:','condition:','odometer:',
                              'cylinders:','color:','transmission:',
                              'type:','status:','drive:','fuel:','price:']]
    
    
    if(makmod!=1):
        df=df[df_['Make&Model']==makmod]
        df.drop(columns='Make&Model',axis=1,inplace=True)
    
    col_drop=['trim:','color:','type:','fuel:','drive:','transmission:']
    df['year:']=df['year:'].astype(int)
    df['year:']=df['year:'].apply(lambda x:(2022-x))
    df['price:']=df['price:'].astype(int)
    if(len(df)>12):
        df=df[(np.abs(stats.zscore(df['price:'])) < 3)]
        df=df[(np.abs(stats.zscore(df['odometer:'])) < 3)]
    df=df[df['price:']>1000]
    df['odometer:']=df['odometer:'].apply(lambda x: x*1000 if x<999 else x )
    #odometer under 100 can be multiplied by 1000.
    df=df.drop_duplicates()
    df.drop(columns=col_drop, inplace=True)
    df=df.reset_index(drop=True)
    df['condition:']=df['condition:'].fillna("good")
    df['cylinders:']=df['cylinders:'].fillna("4")
    df['cylinders:']=df['cylinders:'].replace('other','4')
    df['cylinders:']=df['cylinders:'].apply(lambda x: int(x))
    cleanup_nums = {"condition:": {"new":3,"good": 2, "excellent": 3,"like": 3,"fair": 1,"salvage": 1},
                    "transmission:": {"automatic": 1, "manual": 2, "other":3 },
                   "status:":{"clean": 2, "salvage": 1, "missing":1,"lien":1,"parts":1,"rebuilt":1},
                   "drive:":{"4wd": 3, "rwd": 2, "fwd":1},
                   "fuel:":{'electric':5,"gas": 4, "diesel": 3, "hybrid":2,"other":1}}
    df= df.replace(cleanup_nums)
    cyl_min=df['cylinders:'].value_counts().min()
    cyl_max=df['cylinders:'].value_counts().max()
    if(cyl_min/cyl_max)<(0.2)or(cyl_min/cyl_max==1):
        df.drop(columns='cylinders:',axis=1,inplace=True)
    df=df.drop_duplicates()
    df=df.reset_index(drop=True)
    return df