from flask import Flask, request
import Output
import pandas as pd
app = Flask(__name__)
Matrix = pd.read_pickle('Predicted_Matrix.p')

def dict_to_html(d):
    return '<br>'.join('{0}: {1}'.format(k, d[k]) for k in sorted(d))


# Form page to submit text
@app.route('/')
def submission_page():
    return '''
        <form action="/Zipcode_Recommender" method='POST' >
        <table>
        <tr>
          <td> Please enter the average SqFT you are looking for: </td>
          <td> <input type="text" name="SqFtLiving" /> </td>
        </tr>
        <tr>
          <td> Please enter the number of Bedrooms you are looking for: </td>
          <td> <input type="text" name="Bedrooms" /> </td>
        </tr>
        <tr>
          <td> Please enter the age of each kid in the household, (in format e.g. 1 2 3) </td>
          <td> <input type="text" name="ages" /> </td>
        </tr>
        </table>
            <input type="submit" />
        </form>
        '''


# My Zipcode Recommender app
@app.route('/Zipcode_Recommender', methods=['POST'])
def list_zipcodes():
    ages = str(request.form['ages'])
    age_lst = [int(x) for x in ages.split()]
    SqFtLiving = str(request.form['SqFtLiving'])
    Bedrooms = str(request.form['Bedrooms'])
    #Zipcode_Matrix = Output.subsetting(Matrix, float(SqFtLiving), float(Bedrooms))
    output_table = Output.output_html(Matrix, age_lst, float(SqFtLiving), float(Bedrooms))
    #return '<PRE>'+'\n'.join(list(output_table))+'</PRE>' #str(Zipcode_Matrix)
    table = '\n'.join(list(output_table))
    head = """
    <!DOCTYPE html>
    <html>
    <head>
    <script src="static/sorttable.js"></script> 
    <style type="text/css">
    table, td, th {border: 1px solid black; border-collapse: collapse}
    td {font-family: Arial; padding: 5px; padding-left: 20px}
    td.num {text-align:right}
    </style>
    </head>
    """
    return head + '<body>' + table + '</body>' + '</html>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
