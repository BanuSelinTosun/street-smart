import pandas as pd
import numpy as np
from collections import OrderedDict

def Private_Schooling(age):
    """This function calculates the total Private School Cost per kid until College
        input: age of the kid, integer
        output: total cost until collage
        Note: This calculation excludes bussing which is ~1100 $/year as of September 2017 in the city of Seattle"""
    Ave_Ann_Tuition_increase = 0.06
    Prv_ES_MS_Tuiton = 13801
    Prv_HS_Tuiton = 14473

    if age<14:
        Prv_ES_MS_Cost = [Prv_ES_MS_Tuiton]
        Prv_HS_Cost = [Prv_HS_Tuiton]
        for i in range(0, 14-age):
            Cost_ES_MS = Prv_ES_MS_Cost[i]*(1+Ave_Ann_Tuition_increase)
            Prv_ES_MS_Cost.append(Cost_ES_MS)
        for i in range(0, 18-age):
            Cost_HS = Prv_HS_Cost[i]*(1+Ave_Ann_Tuition_increase)
            Prv_HS_Cost.append(Cost_HS)
        if age<=5:
            Total_Prv_ES_MS_Cost = sum(Prv_ES_MS_Cost[5-age:14-age])
            Total_Prv_HS_Cost = sum(Prv_HS_Cost[14-age:18-age])
        if age>5:
            Total_Prv_ES_MS_Cost = sum(Prv_ES_MS_Cost[0:14-age])
            Total_Prv_HS_Cost = sum(Prv_HS_Cost[14-age:18-age])

    if age>=14:
        Prv_HS_Cost = [Prv_HS_Tuiton]
        for i in range(0, 18-age):
            Cost_HS = Prv_HS_Cost[i]*(1+Ave_Ann_Tuition_increase)
            Prv_HS_Cost.append(Cost_HS)
        Total_Prv_ES_MS_Cost = 0
        Total_Prv_HS_Cost = sum(Prv_HS_Cost[0:18-age])

    Total = Total_Prv_ES_MS_Cost + Total_Prv_HS_Cost
    return Total

def total_kids_edu(age_lst):
    """input: age_lst (list for the ages of the kids)
       output: total education cost for all kids"""
    total = []
    for age in age_lst:
        total_cost_per_kid = Private_Schooling(age)
        total.append(total_cost_per_kid)
    return sum(total)

def subsetting(Matrix, SqFtLiving=700, Bedrooms=1):
    Matrix_subset = Matrix[(Matrix.SqFtTotLiving > (SqFtLiving*0.90)) &
                           (Matrix.SqFtTotLiving < (SqFtLiving*1.1)) &
                           (Matrix.Bedrooms <= (Bedrooms+1)) &
                           (Matrix.Bedrooms >= (Bedrooms-1))]
    Seattle_Zipcodes = [98102, 98103, 98104, 98105, 98106, 98107, 98108, 98109,
                        98112, 98115, 98116, 98117, 98118, 98119, 98122, 98125,
                        98126, 98133, 98136, 98144, 98146, 98177, 98178, 98199]
    Zipcode_Matrix = OrderedDict()
    for zipcode in Seattle_Zipcodes:
        Zipcode_Matrix[zipcode]=Matrix_subset[Matrix_subset[zipcode]==1]
    return Zipcode_Matrix

def output_app(Matrix, age_lst, SqFtLiving, Bedrooms):
    Zipcode_Matrix = subsetting(Matrix, SqFtLiving, Bedrooms)
    total_edu_cost = total_kids_edu(age_lst)
    yield "{:5s}  {:4s} {:10s}   {:10s}  {:10s}  {:3s} {:3s} {:3s} {:10s}".format('Zip', 'Num', 'Min Cost', 'Ave Cost','Max Cost', 'ES', 'MS', 'HS', 'PrEdu Cst')
    for code, matrix in Zipcode_Matrix.items():
        if len(matrix)!=0:
            yield "{:5d} {:4d} {:10.2f} < {:10.2f} < {:10.2f} {:3.0f} {:3.0f} {:3.0f} {:10.2f}".format(code, len(matrix),
                                                                                 matrix.TotalCost.mean() - matrix.TotalCost.std()*1.96, matrix.TotalCost.mean(),
                                                                                 matrix.TotalCost.mean() + matrix.TotalCost.std()*1.96, matrix.ES_Ranking.median(),
                                                                                 matrix.MS_Ranking.median(), matrix.HS_Ranking.median(), total_edu_cost)


def load_data(SqFtLiving, Bedrooms, age_lst):
    Matrix = pd.read_pickle('Predicted_Matrix.p')
    for row in output_app(Matrix, age_lst, SqFtLiving, Bedrooms):
        print row

def main():
    SqFtLiving = raw_input('Please enter the average SqFT you are looking for:')
    Bedrooms = raw_input('Please enter the number of Bedrooms you are looking for:')
    ages = raw_input('Please enter the age of each kid in the household, (in format e.g. 1 2 3):')
    age_lst = [int(x) for x in ages.split()]
    load_data(float(SqFtLiving), float(Bedrooms), age_lst)

if __name__=="__main__":
    main()
