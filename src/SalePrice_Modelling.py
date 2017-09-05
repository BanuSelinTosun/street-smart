import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np

def feature_importance_cal(Model):
    importances = Model.feature_importances_
    std = np.std([tree.feature_importances_ for tree in FSM.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]
    return importances[indices]

def modelling(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
    Model = RandomForestRegressor(n_estimators=300, n_jobs=-1, random_state=0)
    Model.fit(X_train, y_train)
    y_predict = Model.predict(X_test).astype(int)
    score = Model.score(X_test, y_test)
    y_true = y_test.as_matrix()
    residuals = np.log(y_true) - np.log(y_predict)
    error = abs(1 - np.exp(sum(abs(residuals))/len(y_predict)))*100
    return score, Model, y_predict, residuals, error

def NumLivingUnits_check(df):
    df = df[df.NbrLivingUnits <= 2]
    return df

def SqFTLiving_check(df):
    df = df[df.SqFtTotLiving > 500]
    return df

def HeatSystem_converter(df):
    HeatSystem_dummies = pd.get_dummies(df.HeatSystem, drop_first=False, prefix='HeatSystem')
    df = pd.concat([df, HeatSystem_dummies], axis=1).drop('HeatSystem', axis=1)
    return df

def HeatSource_converter(df):
    HeatSource_dummies = pd.get_dummies(df.HeatSource, drop_first=False, prefix='HeatSource')
    df = pd.concat([df, HeatSource_dummies], axis=1).drop('HeatSource', axis=1)
    return df

def SaleWarning_conv(df):
    df.SaleWarning = df.SaleWarning.apply(lambda x: x.split())
    warningdummies = pd.get_dummies(df.SaleWarning.apply(pd.Series).stack(), prefix='SWarn', drop_first=False).sum(level=0)
    df = df.join(warningdummies, how='left').fillna(0.0)
    df = df.drop('SaleWarning', axis=1)
    return df

def Zipcode_converter(df):
    Zipcode_dummies = pd.get_dummies(df.Zipcode, drop_first=False)
    df = pd.concat([df, Zipcode_dummies], axis=1).drop('Zipcode', axis=1)
    return df

def load_data():
    df = pd.read_pickle('ResAss_w_PbSch_Rtngs_Clnd_df.p')
    df['Zipcode'] = df['ZipCode_reduced'].astype(int)
    df['Documentation_YearAge'] = 2017.0 - df['DocumentDate'].dt.year
    df['Documentation_month'] = df['DocumentDate'].dt.month
    df = df[df.Documentation_YearAge <= 1]
    df['TotalCost'] = df['SalePrice'] + df['AddnlCost']
    uplimit = min(df.TotalCost.mean() + df.TotalCost.std()*3.5, 2000000)
    bottomlimit = 100000 # min(abs(df.TotalCost.mean() - df.TotalCost.std()*4), df.TotalCost.min())
    df = df[(df.TotalCost > bottomlimit) & (df.TotalCost < uplimit)]
    df = df.drop(['Address', 'StreetName', 'StreetType', 'SellerName', 'BuyerName', 'DirectionSuffix', 
         'parcel_number', 'PROP_NAME', 'ES_ZONE', 'MS_ZONE', 'HS_ZONE', 'LEVY_JURIS', 'SalePrice', 
         'AddnlCost', 'ExciseTaxNbr', 'BldgGrade', 'SaleReason', 'SaleInstrument', 'FinBasementGrade', 
         'ZipCode_reduced', 'DocumentDate'], axis=1, inplace=True)
    df = Zipcode_converter(df)
    df = SaleWarning_conv(df)
    df = HeatSource_converter(df)
    df = HeatSystem_converter(df)
    df = SqFTLiving_check(df)
    df = NumLivingUnits_check(df)
    y = df.TotalCost
    X = df.drop('TotalCost', axis=1)
    del(df)
    return X, y

def main():
    X, y = load_data()
    score, Model, predicted_cost, residuals, error = modelling(X, y)
    return 'Model Fit Score:', score, 'Model:', Model, 'predicted_cost:', predicted_cost, 'Error:', error

if __name__=="__main__":
    main()
