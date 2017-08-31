from collections import defaultdict
import pandas as pd
pd.set_option('display.max_columns', None)

HS_Rankings = defaultdict(list)
MS_Rankings = defaultdict(list)
ES_Rankings = defaultdict(list)

def create_ES_rating(df):
    ES_Ratings = {'Adams': 9, 'Alki': 9, 'Arbor Heights': 6, 'B.F. Day': 6, 'Bagley': 9, "Beacon Hill Int'l": 7, 
              'Broadview-Thomson K-8': 6, 'Bryant': 10, 'Catharine Blaine K-8': 10, 'Coe': 10, "Concord Int'l": 3, 
              "Dearborn Park Int'l": 5, 'Dunlap': 3, 'Emerson': 2, 'Fairmount Park': 10, 'Gatewood': 7, 'Gatzert': 3, 
             'Graham Hill': 3, 'Green Lake': 9, 'Greenwood': 9, 'Hawthorne': 5, 'Hay': 10, 'Highland Park': 2, 'John Muir': 4, 
             'John Rogers': 7, 'Kimball': 7, 'Lafayette': 9, 'Laurelhurst': 9, 'Lawton': 10, 'Leschi': 4, 'Lowell': 4, 
             'Loyal Heights': 10, 'MLK Jr.': 2, 'Madrona K-8': 4, 'Maple': 8, 'McGilvra': 9, 'Montlake': 10, 'North Beach': 10, 
             'Northgate': 3, 'Olympic Hills': 9, 'Olympic View': 9, 'Rainier View': 9, 'Roxhill': 3, 'Sacajawea': 8, 
             'Sand Point': 7, 'Sanislo': 2, 'Schmitz Park': 10, 'Stevens': 7, 'Thurgood Marshall': 10, 'Van Asselt': 5,
             'View Ridge': 10, 'Viewlands': 6, 'Wedgwood': 10, 'West Seattle Elem': 5, 'West Woodland': 10, 'Whittier': 10, 
              'Wing Luke': 7}
    df['ES_Ranking'] = df['ES_ZONE'].map(lambda x: ES_Ratings[x])
    return df

def create_MS_rating(df):
    MS_Ratings = {'Washington': 8, "Denny Int'l": 7, 'Eckstein':10, 'Whitman':9, 'McClure': 9, "Hamilton Int'l": 10, 
              'Aki Kurose': 5, 'Madison': 9, "Mercer Int'l": 9, 'Jane Addams': 9}
    df['MS_Ranking'] = df['MS_ZONE'].map(lambda x: MS_Ratings[x])
    return df

def create_HS_rating(df):
    HS_Ratings = {'Ballard': 10, "Chief Sealth Int'l": 6, 'Franklin': 8, 'Garfield': 5, "Ingraham Int'l": 9, 'Nathan Hale': 9, 
              'Rainier Beach': 2, 'Roosevelt': 10, 'West Seattle HS': 5}
    df['HS_Ranking'] = df['HS_ZONE'].map(lambda x: HS_Ratings[x])
    return df

def load_data():
    df_parcel_school = pd.read_pickle('parcel_school_cleaned_df.p')
    df_res_Real_est = pd.read_pickle('cleaned_df.p')
    res_RE_w_school = pd.merge(df_res_Real_est, df_parcel_school, on='parcel_number', how='inner', suffixes=('_1', '_2'))
    del(df_parcel_school)
    del(df_res_Real_est)
    res_RE_w_school.drop(['ZIP5', 'CTYNAME', 'LAT', 'LON', 'POINT_X', 'POINT_Y', 'PLAT_NAME', 'KCTP_PAR', 'CONDOSITUS', 'FULLNAME', 'OBJECTID', 'PropertyType', 'PropertyClass', 'PrincipalUse', 'PIN', 'Shape_Leng', 'Shape_Area', 'isSeattle', 'BldgNbr', 'BuildingNumber', 'Fraction', 'BldgGradeVar', 'PcntComplete', 'Obsolescence', 'PcntNetCondition'], inplace = True, axis=1)
    res_RE_w_school = create_ES_rating(res_RE_w_school)
    res_RE_w_school = create_MS_rating(res_RE_w_school)
    res_RE_w_school = create_HS_rating(res_RE_w_school)
    return res_RE_w_school
    

def main():
    res_RE_w_school = load_data()
    res_RE_w_school.to_pickle('ResAss_w_PbSch_Rtngs_Clnd_df.p')

if __name__=="__main__":
    main()