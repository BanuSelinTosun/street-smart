import pandas as pd
# pd.set_option('display.max_columns', None)

def load_data():
    parcel_w_school = pd.read_csv('./Data/Parcel_w_ES_MS_HS_Districts.csv', delimiter=',')
    parcel_w_school['parcel_number'] = parcel_w_school.apply(lambda x:'%s-%s' % (x['MAJOR'],x['MINOR']),axis=1)
    parcel_w_school.drop(['MAJOR', 'MINOR', 'COMMENTS', 'SITETYPE', 'Alias1', 'Alias2', 'SITEID', 'ADDR_HN', 'ADDR_PD', 'ADDR_PT', 'ADDR_SN', 'ADDR_ST', 'ADDR_SD', 'ADDR_NUM', 'ADDR_FULL', 'PLUS4', 'POSTALCTYN', 'COUNTY', 'KROLL', 'JURIS', 'BIG_TEN', 'BUDGET_UNI', 'KCTP_CITY', 'KCTP_STATE', 'PLSS', 'PLAT_LOT', 'PLAT_BLOCK', 'PRESENTUSE', 'LEVYCODE', 'NEW_CONSTR', 'TAXVAL_RSN', 'APPRLNDVAL', 'APPR_IMPR', 'TAX_LNDVAL', 'TAX_IMPR', 'ACCNT_NUM', 'KCTP_TAXYR', 'UNIT_NUM', 'BLDG_NUM', 'QTS', 'SEC', 'TWP', 'RNG', 'PRIMARY_AD', 'legaldesc'], inplace = True, axis=1)
    return parcel_w_school

def main():
    parcel_w_school = load_data()
    parcel_w_school.to_pickle('parcel_school_cleaned_df.p')

if __name__=="__main__":
    main()
