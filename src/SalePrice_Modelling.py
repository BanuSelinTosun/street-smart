import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np

def feature_importance_cal(Model):
    importances = Model.feature_importances_
    std = np.std([FSM.feature_importances_ for tree in FSM.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]
    pass

def modelling(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    Model = RandomForestRegressor()
    Model.fit(X_train, y_train)
    y_predict = Model.predict(X_test).astype(int)
    score = Model.score(X_test, y_test)
    y_true = y_test.as_matrix()
    residuals = np.log(y_true) - np.log(y_predict)
    error = sum(abs(residuals))/len(y_predict)
    return score, Model, y_predict, residuals, error

def Zipcode_converter(df):
    Zipcode_dummies = pd.get_dummies(df.Zipcode, drop_first=False)
    df = pd.concat([df, Zipcode_dummies], axis=1).drop('Zipcode', axis=1)
    return df

def load_data():
    df = pd.read_pickle('ResAss_w_PbSch_Rtngs_Clnd_df.p')
    df['Zipcode'] = df['ZipCode_reduced'].astype(int)
    df['Documentation_Age'] = 2017 - df['DocumentDate'].dt.year
    df['TotalCost'] = df['SalePrice'] + df['AddnlCost']
    uplimit = df.TotalCost.mean() + df.TotalCost.std()*4
    bottomlimit = min(abs(df.TotalCost.mean() - df.TotalCost.std()*4), df.TotalCost.min())
    df = df[(df.TotalCost > df.TotalCost.min()) & (df.TotalCost < (df.TotalCost.mean() + df.TotalCost.std()*4))]
    df = df.drop(['Address', 'StreetName', 'StreetType', 'SellerName', 'BuyerName', 'DirectionSuffix', 
         'SaleWarning', 'parcel_number', 'PROP_NAME', 'ES_ZONE', 'MS_ZONE', 'HS_ZONE', 'LEVY_JURIS', 'SalePrice', 
         'AddnlCost', 'ExciseTaxNbr', 'BldgGrade', 'SaleReason', 'SaleInstrument', 'FinBasementGrade', 'ZipCode_reduced',
         'DocumentDate', 'SalePrice', 'AddnlCost'], axis=1, inplace=True)
    df = Zipcode_converter(df)
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
