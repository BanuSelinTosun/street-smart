import pandas as pd
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt

def Private_Schooling(age):
    """This function calculates the total Private School Cost per kid until
        College
        input: age of the kid, integer
        output: total cost until collage
        Note: This calculation excludes bussing which is ~1100 $/year as of
        September 2017 in the city of Seattle"""
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

def outlist(Matrix, age_lst, SqFtLiving, Bedrooms):
    Zipcode_Matrix = subsetting(Matrix, SqFtLiving, Bedrooms)
    total_edu_cost = total_kids_edu(age_lst)
    Est_mean = []
    Est_min = []
    Est_max = []
    zipcodes_str = []
    num_RE = []
    ES_Rate = []
    MS_Rate = []
    HS_Rate = []
    for code, matrix in Zipcode_Matrix.items():
        if len(matrix)!=0:
            zipcodes_str.append(str(code))
            num_RE.append(len(matrix))
            Est_min.append((matrix.TotalCost.mean() - matrix.TotalCost.std()*1.96)/10**5)
            Est_mean.append((matrix.TotalCost.mean())/10**5)
            Est_max.append((matrix.TotalCost.mean() + matrix.TotalCost.std()*1.96)/10**5)
            ES_Rate.append(round(matrix.ES_Ranking.median()))
            MS_Rate.append(round(matrix.MS_Ranking.median()))
            HS_Rate.append(round(matrix.HS_Ranking.median()))
    return Est_mean, Est_min, Est_max, zipcodes_str, num_RE, ES_Rate, MS_Rate, HS_Rate

def outplot(Matrix, age_lst, SqFtLiving, Bedrooms):
    Est_mean, Est_min, Est_max, zipcodes_str, num_RE, ES_Rate, MS_Rate, HS_Rate = outlist(Matrix, age_lst, SqFtLiving, Bedrooms)
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(18, 18/4), facecolor=(0,0,0,0.65))
    legend_properties = {'weight':'bold'}
    ax1.plot(Est_mean, 'rd', label='Mean $ Estimate', markersize=13, alpha=0.7)
    ax1.plot(Est_min, 'wd', label='Min $ Estimate', markersize=8, alpha=0.7)
    ax1.plot(Est_max, 'wd', label='Max $ Estimate', markersize=8, alpha=0.7)
    ax1.grid(color='grey', linestyle='--', linewidth=1)
    ax1.set_ylim(round(min(Est_min)-1.5), round(max(Est_max)+1.5))
    ax1.set_yticks(range(int(round(min(Est_min)-1.5)), int(round(max(Est_max)+1.5)), 2))
    ax1.set_yticklabels(range(int(round(min(Est_min)-1.5)), int(round(max(Est_max)+1.5)), 2), fontweight='bold', color='white')
    ax1.set_ylabel('Estimated $ X 100K', fontweight='bold', color='white')
    ax1.legend(prop=legend_properties, framealpha=0.5)
    ax1.set_facecolor((1,1,1,0))
    ax2.plot(ES_Rate, 'gs', label='Elementary School', markersize=10, alpha=0.7)
    ax2.plot(MS_Rate, 'r^', label='Middle School', markersize=10, alpha=0.7)
    ax2.plot(HS_Rate, 'bo', label='High School', markersize=10, alpha=0.7)
    ax2.legend(prop=legend_properties, framealpha=0.5)
    ax2.grid(color='grey', linestyle='--', linewidth=1)
    ax2.set_ylim(-1, 11)
    ax2.set_yticks([0, 2, 4, 6, 8, 10])
    ax2.set_yticklabels([0, 2, 4, 6, 8, 10], fontweight='bold', color='white')
    ax2.set_ylabel('School Ratings', fontweight='bold', color='white')
    ax2.set_xlabel('Zipcodes', fontweight='bold', color='white')
    ax1.set_xticks(range(len(zipcodes_str)+3))
    ax1.set_xticklabels(zipcodes_str +['']*3, fontweight='bold', color='white')
    ax2.set_xticks(range(len(zipcodes_str)+3), zipcodes_str +['']*3)
    ax2.set_xticklabels(zipcodes_str +['']*3, fontweight='bold', color='white')
    ax2.set_facecolor((1,1,1,0))
    for t in ax1.legend(framealpha=0).get_texts():
        t.set_color('white')
    for t in ax2.legend(framealpha=0).get_texts():
        t.set_color('white')
    for spine in ax1.spines:
        ax1.spines[spine].set_color('white')
    for spine in ax2.spines:
        ax2.spines[spine].set_color('white')
    for axis in ('x', 'y'):
        ax1.tick_params(axis=axis, color='white')
        ax2.tick_params(axis=axis, color='white')
    plt.tight_layout()
    #plt.show()
    return f

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

def output_html(Matrix, age_lst, SqFtLiving, Bedrooms):
    Zipcode_Matrix = subsetting(Matrix, SqFtLiving, Bedrooms)
    total_edu_cost = total_kids_edu(age_lst)
    yield """<table class="sortable">"""
    yield """<tr>
               <th>{:5s}</th><th>{:5s}</th><th>{:10s}</th><th>{:10s}</th><th>{:10s}</th><th>{:3s}</th><th>{:3s}</th><th>{:3s}</th><th>{:10s}</th>
             </tr>
          """.format('Zipcode', 'Num', 'Min Est', 'Ave Est','Max Est', 'ES', 'MS', 'HS', 'PrvEd Cst')
    for zcode, matrix in Zipcode_Matrix.items():
        if len(matrix)!=0:
            yield """<tr id="z{:5d}" onclick="updateMap({:5d})">
                       <td>{:5d}</td><td class="num">{:5d}</td><td class="num">{:10.0f} $</td><td class="num">{:10.0f} $</td><td class="num">{:10.0f} $</td><td class="num">{:3.0f}</td><td class="num">{:3.0f}</td><td class="num">{:3.0f}</td><td class="num">{:10.0f} $</td>
                     </tr>
                  """.format(
                     zcode,zcode,zcode,
                     len(matrix),
                     round(matrix.TotalCost.mean() - matrix.TotalCost.std()*1.96),
                     round(matrix.TotalCost.mean()),
                     round(matrix.TotalCost.mean() + matrix.TotalCost.std()*1.96),
                     matrix.ES_Ranking.median(),
                     matrix.MS_Ranking.median(),
                     matrix.HS_Ranking.median(),
                     round(total_edu_cost))
    yield "</table>"

def load_data(SqFtLiving, Bedrooms, age_lst):
    Matrix = pd.read_pickle('Predicted_Matrix.p')
    outplot(Matrix, age_lst, SqFtLiving, Bedrooms)
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
