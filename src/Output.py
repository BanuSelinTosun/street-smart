import pandas as pd
import numpy as np

def subsetting(Matrix, SqFtLiving=700, Bedrooms=1):
    Matrix_subset = Matrix[(Matrix.SqFtTotLiving > (SqFtLiving*0.90)) & (Matrix.SqFtTotLiving < (SqFtLiving*1.1)) & (Matrix.Bedrooms <= (Bedrooms+1)) & (Matrix.Bedrooms >= (Bedrooms-1))]
    Matrix_98102 = Matrix_subset[Matrix_subset[98102]==1]
    Matrix_98103 = Matrix_subset[Matrix_subset[98103]==1]
    Matrix_98104 = Matrix_subset[Matrix_subset[98104]==1]
    Matrix_98105 = Matrix_subset[Matrix_subset[98105]==1]
    Matrix_98106 = Matrix_subset[Matrix_subset[98106]==1]
    Matrix_98107 = Matrix_subset[Matrix_subset[98107]==1]
    Matrix_98108 = Matrix_subset[Matrix_subset[98108]==1]
    Matrix_98109 = Matrix_subset[Matrix_subset[98109]==1]
    Matrix_98112 = Matrix_subset[Matrix_subset[98112]==1]
    Matrix_98115 = Matrix_subset[Matrix_subset[98115]==1]
    Matrix_98116 = Matrix_subset[Matrix_subset[98116]==1]
    Matrix_98117 = Matrix_subset[Matrix_subset[98117]==1]
    Matrix_98118 = Matrix_subset[Matrix_subset[98118]==1]
    Matrix_98119 = Matrix_subset[Matrix_subset[98119]==1]
    Matrix_98122 = Matrix_subset[Matrix_subset[98122]==1]
    Matrix_98125 = Matrix_subset[Matrix_subset[98125]==1]
    Matrix_98126 = Matrix_subset[Matrix_subset[98126]==1]
    Matrix_98133 = Matrix_subset[Matrix_subset[98133]==1]
    Matrix_98136 = Matrix_subset[Matrix_subset[98136]==1]
    Matrix_98144 = Matrix_subset[Matrix_subset[98144]==1]
    Matrix_98146 = Matrix_subset[Matrix_subset[98146]==1]
    Matrix_98177 = Matrix_subset[Matrix_subset[98177]==1]
    Matrix_98178 = Matrix_subset[Matrix_subset[98178]==1]
    Matrix_98199 = Matrix_subset[Matrix_subset[98199]==1]
    zipcode_lst = [Matrix_98102, Matrix_98103, Matrix_98104, Matrix_98105, Matrix_98106, Matrix_98107, Matrix_98108, Matrix_98109, Matrix_98112, Matrix_98115, Matrix_98116, Matrix_98117,
               Matrix_98118, Matrix_98119, Matrix_98122, Matrix_98125, Matrix_98126, Matrix_98133, Matrix_98136, Matrix_98144, Matrix_98146, Matrix_98177, Matrix_98178, Matrix_98199]
    Seattle_Zipcodes = [98102, 98103, 98104, 98105, 98106, 98107, 98108, 98109, 98112, 98115, 98116, 98117, 98118, 98119, 98122, 98125, 98126, 98133, 98136, 
                    98144, 98146, 98177, 98178, 98199]
    for code, matrix in zip(Seattle_Zipcodes, zipcode_lst):
        if len(matrix)!=0:
            print "{:5d} {:4d} {:10.2f} < {:10.2f} < {:10.2f} {:3.0f} {:3.0f} {:3.0f}".format(code, len(matrix), 
                                                                                     matrix.TotalCost.mean() - matrix.TotalCost.std()*1.96, matrix.TotalCost.mean(), 
                                                                                     matrix.TotalCost.mean() + matrix.TotalCost.std()*1.96, matrix.ES_Ranking.median(), 
                                                                                     matrix.MS_Ranking.median(), matrix.HS_Ranking.median())


def load_data(SqFtLiving, Bedrooms):
    Matrix = pd.read_pickle('./src/Predicted_Matrix.p')
    Output = subsetting(Matrix, SqFtLiving, Bedrooms)
    return Output

def main(SqFtLiving, Bedrooms):
    Output = load_data(SqFtLiving, Bedrooms)
    
if __name__=="__main__":
    SqFtLiving = raw_input('Please enter the average SqFT you are looking for:')
    Bedrooms = raw_input('Please enter the number of Bedrooms you are looking for:')
    main(float(SqFtLiving), float(Bedrooms))