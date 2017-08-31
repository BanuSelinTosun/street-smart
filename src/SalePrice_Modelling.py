import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np

def feature_importance_cal(Model):
    importances = Model.feature_importances_
    std = np.std([FSM.feature_importances_ for tree in FSM.estimators_],
             axis=0)
    indices = np.argsort(importances)[::-1]
    pass

def modelling(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    Model = RandomForestRegressor()
    Model.fit(X_train, y_train)
    y_predict = Model.predict(X_test).astype(int)
    score = Model.score(X_test, y_test)
    return score, Model, y_predict

def load_data():
    df = pd.read_pickle('ResAss_w_PbSch_Rtngs_Clnd_df.p')
    df['Zipcode'] = df['ZipCode_reduced'].astype(int)
    subset_df['DocumentationYear'] = subset_df['DocumentDate'].dt.year
    subset_df['TotalCost'] = subset_df['SalePrice'] + subset_df['AddnlCost']
    subset_df = df.drop(['Address', 'StreetName', 'StreetType', 'SellerName', 'BuyerName', 'DirectionSuffix',
                     'SaleWarning', 'ZipCode_reduced', 'parcel_number', 'PROP_NAME', 'ES_ZONE', 'MS_ZONE',
                     'HS_ZONE', 'LEVY_JURIS', 'DocumentDate', 'SalePrice', 'AddnlCost', 'ExciseTaxNbr',
                     'BldgGrade', 'SaleReason', 'SaleInstrument'], axis=1)
    y = subset_df.TotalCost
    X = subset_df.drop('TotalCost', axis=1)
    return X, y

def main():
    X, y = load_data()
    score, _, predicted_cost = modelling(X, y)
    return score, predicted_cost

if __name__=="__main__":
    main()
