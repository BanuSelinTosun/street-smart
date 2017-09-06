import pandas as pd
# pd.set_option('display.max_columns', None)

def zipcode_simplifier(df):
    df['ZipCode_reduced'] = df['ZipCode'].map(lambda x: str(x)[:5])
    df = df[(df['ZipCode_reduced'].map(lambda x: len(x) == 5)) & (df['ZipCode_reduced'].map(lambda x: x.isdigit())) & (df['ZipCode_reduced'].map(lambda x: x[:2]=='98'))]
    df = df.drop('ZipCode', axis=1)
    return df

def DayLightBasement_simplifier(df):
    df['DaylightBasement'].loc[df['DaylightBasement'] == 'y'] = 'Y'
    df['DaylightBasement'].loc[df['DaylightBasement'] == 'n'] = 'N'
    return df

def NaN_DaylightBasement(df):
    df['DaylightBasement'].loc[(df['DaylightBasement'] != 'Y') & (df['DaylightBasement'] != 'N')] = 'NaN'
    return df

def DaylightBasement_converter(df):
    DLB_dummies = pd.get_dummies(df.DaylightBasement, prefix='DLB', drop_first=False)
    df = pd.concat([df, DLB_dummies], axis=1).drop('DaylightBasement', axis=1)
    return df

def NaN_HistoricProperty(df):
    df['AFHistoricProperty'].loc[(df['AFHistoricProperty'] != 'Y') & (df['AFHistoricProperty'] != 'N')] = 'NaN'
    return df

def AFHistoricProperty_converter(df):
    HP_dummies = pd.get_dummies(df.AFHistoricProperty, prefix='HP', drop_first=False)
    df = pd.concat([df, HP_dummies], axis=1).drop('AFHistoricProperty', axis=1)
    return df

def DocumentDate(df):
    df['DocumentDate'] = pd.to_datetime(df['DocumentDate'])
    df = df.loc[(df['DocumentDate'] > '1985-01-01') & (df['DocumentDate'] < '2017-08-08')]
    return df

def drop_outliers_saleprice(df):
    df = df[df.SalePrice > 15000]
    return df

def isSeattle(df):
    Seattle_Zipcodes = [98101, 98102, 98103, 98104, 98105, 98106, 98107, 98108, 98109, 98112, 98115, 98116, 98117, 98118, 98119, 98121, 98122, 98125, 98126, 98133, 98134, 98136, 98144, 98146, 98154, 98164, 98174, 98177, 98178, 98195, 98199]
    Seattle_zipcodes = [str(x) for x in Seattle_Zipcodes]
    mask = df['ZipCode_reduced'].isin(Seattle_zipcodes)
    df['isSeattle'] = mask*1.0
    return df

def isBellevue(df):
    Bellevue_Zipcodes = [98004, 98005, 98006, 98007, 98008, 98027, 98033, 98039, 98052, 98059]
    Bellevue_zipcodes = [str(x) for x in Bellevue_Zipcodes]
    mask = df['ZipCode_reduced'].isin(Bellevue_Zipcodes)
    df['isBellevue'] = mask*1.0
    return df

def isKirkland(df):
    Kirkland_Zipcodes = [98033, 98034, 98052]
    Kirkland_zipcodes = [str(x) for x in Kirkland_Zipcodes]
    mask = df['ZipCode_reduced'].isin(Kirkland_Zipcodes)
    df['isKirkland'] = mask*1.0
    return df

def isRedmond(df):
    Redmond_Zipcodes = [98007, 98008, 98034, 98052, 98053]
    Redmond_zipcodes = [str(x) for x in Redmond_Zipcodes]
    mask = df['ZipCode_reduced'].isin(Redmond_Zipcodes)
    df['isRedmond'] = mask*1.0
    return df

def Buyer_Seller_cleaner(df):
    df = df[(df['BuyerName'] != df['SellerName'])]
    return df

def ViewUtilization_simplifier(df):
    df['ViewUtilization'].loc[df['ViewUtilization'] == 'y'] = 'Y'
    df['ViewUtilization'].loc[(df['ViewUtilization'] != 'Y') & (df['ViewUtilization'] != 'N')] = 'NaN'
    return df

def CurrentUseLand_simplifier(df):
    df['AFCurrentUseLand'].loc[df['AFCurrentUseLand'] == '0'] = 'N'
    df['AFCurrentUseLand'].loc[(df['AFCurrentUseLand'] != 'Y') & (df['AFCurrentUseLand'] != 'N')] = 'NaN'
    return df

def AFForestLand_simplifier(df):
    df['AFForestLand'].loc[df['AFForestLand'] == '0'] = 'N'
    df['AFForestLand'].loc[(df['AFForestLand'] != 'Y') & (df['AFForestLand'] != 'N')] = 'NaN'
    return df

def drop_outliers_address(df):
    counts = df['Address'].value_counts()
    df = df[df['Address'].isin(counts[counts < 50].index)]
    return df

def AFForestLand_converter(df):
    AFL_dummies = pd.get_dummies(df.AFForestLand, prefix='AFL', drop_first=False)
    df = pd.concat([df, AFL_dummies], axis=1).drop('AFForestLand', axis=1)
    return df

def AFCurrentUseLand_converter(df):
    ACL_dummies = pd.get_dummies(df.AFCurrentUseLand, prefix='ACL', drop_first=False)
    df = pd.concat([df, ACL_dummies], axis=1).drop('AFCurrentUseLand', axis=1)
    return df

def ViewUtilzation_converter(df):
    VU_dummies = pd.get_dummies(df.ViewUtilization, prefix='VU', drop_first=False)
    df = pd.concat([df, VU_dummies], axis=1).drop('ViewUtilization', axis=1)
    return df

def only_Seattle(df):
    df = df[df.isSeattle > 0]
    df.drop(['isBellevue', 'isKirkland', 'isRedmond'], inplace = True, axis=1)
    return df

def load_data():
    resbldg = pd.read_csv('data/EXTR_ResBldg.csv', delimiter=',')
    resbldg['parcel_number'] = resbldg.apply(lambda x:'%s-%s' % (x['Major'],x['Minor']),axis=1)
    rpsale = pd.read_csv('data/EXTR_RPSale.csv', delimiter=',')
    rpsale['parcel_number'] = rpsale.apply(lambda x:'%s-%s' % (x['Major'],x['Minor']),axis=1)
    res_bldg_sale = pd.merge(resbldg, rpsale, on='parcel_number', how='inner', suffixes=('_1', '_2'))
    del(rpsale)
    del(resbldg)
    res_bldg_sale.drop(['Major_1', 'Minor_1', 'Major_2', 'Minor_2', 'RecordingNbr', 'DirectionPrefix', 'PlatNbr', 'PlatType', 'PlatLot', 'PlatBlock', 'AFNonProfitUse', 'Page', 'Volume'], inplace = True, axis=1)
    res_bldg_sale = zipcode_simplifier(res_bldg_sale)
    res_bldg_sale = DayLightBasement_simplifier(res_bldg_sale)
    res_bldg_sale = NaN_DaylightBasement(res_bldg_sale)
    res_bldg_sale = DaylightBasement_converter(res_bldg_sale)
    res_bldg_sale = NaN_HistoricProperty(res_bldg_sale)
    res_bldg_sale = AFHistoricProperty_converter(res_bldg_sale)
    res_bldg_sale = DocumentDate(res_bldg_sale)
    res_bldg_sale = drop_outliers_saleprice(res_bldg_sale)
    res_bldg_sale = isSeattle(res_bldg_sale)
    res_bldg_sale = isBellevue(res_bldg_sale)
    res_bldg_sale = isKirkland(res_bldg_sale)
    res_bldg_sale = isRedmond(res_bldg_sale)
    res_bldg_sale = Buyer_Seller_cleaner(res_bldg_sale)
    res_bldg_sale = ViewUtilization_simplifier(res_bldg_sale)
    res_bldg_sale = CurrentUseLand_simplifier(res_bldg_sale)
    res_bldg_sale = AFForestLand_simplifier(res_bldg_sale)
    res_bldg_sale = drop_outliers_address(res_bldg_sale)
    res_bldg_sale = AFForestLand_converter(res_bldg_sale)
    res_bldg_sale = AFCurrentUseLand_converter(res_bldg_sale)
    res_bldg_sale = ViewUtilzation_converter(res_bldg_sale)
    res_bldg_sale = only_Seattle(res_bldg_sale)
    return res_bldg_sale

def main():
    res_bldg_sale = load_data()
    res_bldg_sale.to_pickle('cleaned_df.p')

if __name__=="__main__":
    main()
