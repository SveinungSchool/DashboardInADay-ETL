import pandas as pd
from os import listdir
from os.path import isfile, join
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from datetime import datetime
import db
from db import create_database
import os

### set this
path = "C:\\data\\diad-student-english\\Data\\"
excelPath = os.path.join(path, "USSales", "bi_dimensions.xlsx")
batchSize = 500000

def insertManufacturer():
    dfMan = pd.read_excel(excelPath,sheet_name="manufacturer",header=None)
    dfMan = dfMan[1:4].T
    dfMan.columns = dfMan.iloc[0]
    dfMan = dfMan[1:]
   
    with Session(engine) as sesssion:
        for r in dfMan.itertuples():
            m = db.Manufacturer(id=r.ManufacturerID, name = r.Manufacturer)
            sesssion.add(m)
        sesssion.commit()


def insertProducts():
    proddf = pd.read_excel(excelPath,sheet_name="product",header=1)
    with Session(engine) as sesssion:
        for r in proddf.itertuples():
            p = db.Product(id=r.ProductID, name = r.Product, manufacturer_id = r.ManufacturerID)
            sesssion.add(p)
        sesssion.commit()

def insertGeo():
    dfGeo = pd.read_excel(excelPath,sheet_name="geo",header=3) 
    session = Session(engine)
    for r in dfGeo.itertuples():
        g = db.Geography( country = r.Country, zip =  r.Zip, district = r.District, state = r.State, region = r.Region, city = r.City)
        session.add(g)        
    session.commit()


def insertSales(dfSales):
    print("inserting sales for " + dfSales.iloc[0]["Country"])
    i=0
    session = Session(engine)
    for r in dfSales.itertuples():
        s = db.Sales( product_id = r.ProductID, quantity =  r.Units, revenue = r.Revenue, country = r.Country, zip = r.Zip, date = datetime.strptime( r.Date, '%Y-%m-%d' ))
        session.add(s)
        i+=1
        if(i%batchSize==0):
            print("Saving " + str(batchSize) + " records")
            session.commit()
            session = Session(engine)
    session.commit()

def getAndinsertSales():
    usSales = pd.read_csv( os.path.join( path , "USSales" , "sales.csv") )
    usSales["Country"]="USA"
    insertSales(usSales)

    folderPath = os.path.join(path,"InternationalSales")
    csvfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and f.endswith(".csv")]
    for csv in csvfiles:
        sales = pd.read_csv( os.path.join( folderPath, csv))
        insertSales(sales)




engine = create_engine("sqlite:///sales.db", echo=False)
create_database(engine)
insertGeo()
insertManufacturer()
insertProducts()
getAndinsertSales()