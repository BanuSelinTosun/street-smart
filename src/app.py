from flask import Flask, request
import Output
import pandas as pd
app = Flask(__name__)
Matrix = pd.read_pickle('Predicted_Matrix.p')

# Form page to submit text
@app.route('/')
def submission_page():
    return '''
        <h1>Maximize Life Within Budget</h1>
        <style type="text/css">
        h1 {font-family: Arial; color: white; text-shadow: 1px 1px #ff0000;}
        tr {font-family: Arial; color: white; font-weight: bold}
        body {background-image: url("static/Seattle_SeaFront.jpg");}
        </style>
        <body>
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
        </body>
        '''

# My Zipcode Recommender app
@app.route('/Zipcode_Recommender', methods=['POST'])
def list_zipcodes():
    ages = str(request.form['ages'])
    age_lst = [int(x) for x in ages.split()]
    SqFtLiving = str(request.form['SqFtLiving'])
    Bedrooms = str(request.form['Bedrooms'])
    output_table = Output.output_html(Matrix, age_lst, float(SqFtLiving), float(Bedrooms))
    table = '\n'.join(list(output_table))
    head = """
    <!DOCTYPE html>
    <html>
    <head>
    <script src="static/sorttable.js"></script>
    <style type="text/css">
    table, td, th {border: 1px solid black; border-collapse: collapse; background: rgba(25,25,25,0.3)}
    th {font-family: Arial; padding: 5px; padding-left: 20px; color: white;}
    td {font-family: Arial; padding: 5px; padding-left: 20px; color: white}
    td.num {text-align:right}
    body {background-image: url("static/Seattle_SeaFront.jpg");}
    </style>
    </head>
    <h2>You can click on the column names to sort the table.</h2>
    <style type="text/css">
    h2 {font-family: Arial; color: white; text-shadow: 1px 1px #ff0000;}
    </style>
    """
    return head + '<body>' + table + '</body>' + '</html>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
