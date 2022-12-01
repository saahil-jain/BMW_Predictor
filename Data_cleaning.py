import pandas as pd
import numpy as np
import re 

def clean_features(df, fillna=False):
    import numpy as np
    if "Features" not in df.columns:
        return df
    features = df["Features"].values
    new_features = {"Mileage":[], "Transmission":[], "Drive_Side":[], "Condition":[]}
    for row in features:
        row = str(row)
        if row != "nan":
            values = row.split(" · ")
        else:
            values = []

        #Setting Milage
        if len(values) and ("mi" in values[0] or  "km" in values[0]):
            values[0] = values[0].strip()
            if "km" in values[0]:
                if "mi" in values[0]:
                    values[0] = int(values[0].split("(")[1][:-4].replace(',', ''))
                else:
                    values[0] = int(values[0][:-3].replace(',', '')) / 1.60933
            else:
                values[0] = int(values[0][:-3].replace(',', ''))
            new_features['Mileage'].append(values[0])
            values = values[1:]
        elif len(values) and values[0] == "TMU":
            new_features['Mileage'].append(np.nan)
            values = values[1:]
        else:
            new_features['Mileage'].append(np.nan)

        #Setting Transmission
        if values and values[0] in ["Manual", "Automatic"]:
            values[0] = values[0].strip()
            new_features['Transmission'].append(values[0])
            values = values[1:]
        else:
            new_features['Transmission'].append(np.nan)

        #Setting Drive_Side
        if values and values[0] in ["LHD", "RHD"]:
            values[0] = values[0].strip()
            new_features['Drive_Side'].append(values[0])
            values = values[1:]
        else:
            new_features['Drive_Side'].append(np.nan)

        #Setting Condition
        if values and values[0]:
            values[0] = values[0].strip()
            new_features['Condition'].append(values[0])
            values = values[1:]
        else:
            new_features['Condition'].append(np.nan)

    new_features = pd.DataFrame(new_features)
    result = pd.concat([df, new_features], axis=1)
    result = result.drop(columns=['Features'])

    # if fillna:
    #   for feature in ["Transmission", "Drive_Side", "Condition"]:
    #     result[feature] = result[feature].fillna(result[feature].mode()[0])
    #   for feature in ["Mileage"]:
    #     result[feature] = result[feature].fillna(result[feature].median())
    return result

def clean_date(df):
    import pandas as pd
    df["Date"] = pd.to_datetime(df["Date"])
    return df

def clean_name(df):
    import numpy as np
    if "Name" not in df.columns:
        return df
    first_column=df.loc[:,"Name"]
    col=first_column.to_numpy(dtype=object)
    year=[]
    nameCleaned=[]
    for item in col:
        if item!="":
            itemsinList=item.split(" ")
            year.append(itemsinList[0])
            # print(item, itemsinList)
            nameCleaned.append(itemsinList[1:])
        else:
            year.append(np.nan)
            nameCleaned.append(np.nan)
    df["NameOfModel"]=nameCleaned
    df["YearOfManufacture"]=year
    df = df.drop(columns=['Name'])
    return df

def binarize_auctiontype(df):
    import numpy as np
    if "Auction_Type" not in df.columns:
        return df
    auction_column=df.loc[:,"Auction_Type"]
    colu=auction_column.to_numpy(dtype=object)
    binarized=[]
    for item in colu:
        if item=="Auction":
            binarized.append(1)
        elif item=="Fixed-price":
            binarized.append(0)
        else:
            binarized.append(np.nan)
    df["AuctionType"]=binarized
    df=df.drop(columns=['Auction_Type'])
    return df

def binarize_transmission(df):
    import numpy as np
    if "Transmission" not in df.columns:
        return df
    auction_column=df.loc[:,"Transmission"]
    colu=auction_column.to_numpy(dtype=object)
    binarized=[]
    for item in colu:
        if item=="Manual":
            binarized.append(1) #Manual is 1
        elif item=="Automatic":
            binarized.append(0) #Automatic is 0
        else:
            binarized.append(np.nan)
    df["Transmission_type"]=binarized
    df=df.drop(columns=['Transmission'])
    return df

def binarize_drive_side(df):
    import numpy as np
    if "Drive_Side" not in df.columns:
        return df
    auction_column=df.loc[:,"Drive_Side"]
    colu=auction_column.to_numpy(dtype=object)
    binarized=[]
    for item in colu:
        if item=="LHD":
            binarized.append(1) #Left hand side is 1
        elif item=="RHD":
            binarized.append(0) # Right hand side is 0
        else:
            binarized.append(np.nan)
    df["DriveSide"]=binarized
    df=df.drop(columns=['Drive_Side'])
    return df

def clean_prices(df):
    import numpy as np
    import re 
    pound = 1.2064 
    euros = 1.04
    regex = '\d+'
    
    prices = df["Price"].values
    new_prices = []
    
    for item in prices:
        
        if item[0]=='$':
            price = re.sub(',', '', item)
            new_prices.append(int(re.findall(regex,price)[0]))

        elif item[0]=='£':
            price = re.sub(',', '', item)
            price = int(re.findall(regex,price)[0])*pound
            new_prices.append(price)

        elif item[0]=='€':
            price = re.sub(',', '', item)
            price = int(re.findall(regex,price)[0])*euros
            new_prices.append(price)
        
        else:
            new_prices.append(np.nan)
      
    new_prices = pd.DataFrame(new_prices)
    df['Price'] = new_prices
    result = df

    return result