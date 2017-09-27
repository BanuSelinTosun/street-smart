from flask import Flask, request
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from StringIO import StringIO
import base64
import Output
import pandas as pd
import re
app = Flask(__name__)
Matrix = pd.read_pickle('Predicted_Matrix.p')
#Matrix = pd.read_pickle('GB_Pickled_Mtrx.p')
with open ('../google_api_key') as f:
    google_api_key = f.read()

# Form page to submit text
@app.route('/')
def submission_page():
    return '''
        <h1>Maximize Your Family's Real Estate Investment</h1>
        <h2>The details of this work is explained in the GitHub repo below:</h2>
	<h2>https://github.com/BanuSelinTosun/street-smart</h2>
	<p> Seattle house prices are going up rapidly.
            Everyone is on a budget; how should you invest your money?
        </p>
        <p>
            Here, with this app, you can learn about the estimated house prices
            in each Seattle zipcode.
        </p>
        <p>
            If you are planning to have kids, or already have kids, you need to
            consider their education as well. This app will help you to compare
            the estimated housing prices within in each zipcode, show you the
            public school rankings in these locations. It also compares the
            Private school cost until they graduate from high school.
        </p>
        <style type="text/css">
        h1 {font-family: Arial; color: white; color: white; text-shadow: 2px 2px 4px #000000;}
        h2 {font-family: Arial; color: white; color: white; text-shadow: 2px 2px 4px #000000;}
	p {font-family: Arial; font-weight: bold; color: white;
        text-shadow: 2px 2px 4px #000000;}
        tr {font-family: Arial; color: white; font-weight: bold}
        body {background-image: url("static/Seattle_SeaFront.jpg"); background-size:cover; text-shadow: 2px 2px 4px #000000;}
        </style>
        <body>
        <form action="/Zipcode_Recommender" method='POST' >
        <table>
        <tr>
          <td> The approximate SqFT you are looking for: </td>
          <td> <input type="text" name="SqFtLiving" /> </td>
        </tr>
        <tr>
          <td> The number of Bedrooms you are looking for: </td>
          <td> <input type="text" name="Bedrooms" /> </td>
        </tr>
        <tr>
          <td> The age of each kid in the household, (in format e.g. 1 2 3)
               If kids are not a part of the plan, just leave it empty.
          </td>
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
    if len(ages) == 0:
        age_lst = []
    else:
        lst = re.split('; |, |\*|\t| |,|;',ages)
        age_lst = [int(x) for x in lst]
    # SqFtLiving = str(request.form['SqFtLiving'])
    num1 = str(request.form['SqFtLiving'])
    if int(num1) <= 500:
        SqFtLiving = '500'
    elif int(num1) >= 12400:
        SqFtLiving = '12400'
    else:
        SqFtLiving = num1
    num2 = str(request.form['Bedrooms'])
    if int(num2) <= 0:
        Bedrooms = '0'
    elif int(num2) >= 34:
        Bedrooms = '34'
    else:
        Bedrooms = num2
    # Bedrooms = str(request.form['Bedrooms'])
    output_table = Output.output_html(Matrix, age_lst, float(SqFtLiving), float(Bedrooms))
    fig = Output.outplot(Matrix, age_lst, float(SqFtLiving), float(Bedrooms))
    image_file = StringIO()
    fig.savefig(image_file, facecolor=fig.get_facecolor(), edgecolor='none')
    image_file.seek(0)
    table = '\n'.join(list(output_table))
    head = """
    <!DOCTYPE html>
    <html>
    <head>
    <script src="static/jquery-3.2.1.min.js"></script>
    <script src="static/sorttable.js"></script>
    <script src="static/app.js"></script>
    <style type="text/css">
    table, td, th {border: 1px solid black; border-collapse: collapse; background: rgba(25,25,25,0.6)}
    th {font-family: Arial; padding: 5px; padding-left: 20px; color: white;}
    td {font-family: Arial; padding: 5px; padding-left: 20px; color: white;}
    td.num {text-align:right}
    body {background-image: url("static/Seattle_SeaFront.jpg");
    background-size:cover;}
    img {width:1250px; height: auto;}
    iframe {position:absolute; top:458px; left:742px; right:0; bottom:0; height:100%;
    width:100%;}
    h3 {font-family: Arial; color: white; color: white; text-shadow: 2px 2px 4px #000000;}
    .highlight {background-color: red;}
    </style>
    </head>
    <h3>Click on the column names to sort the table.</h3>
    <h3>ES, MS, HS represents the allocated public school ratings.</h3>
    <h3>Average private school (K-12) cost is abbreviated as PrvEd Cst.</h3>
    <h3>Click on the rows to show the zipcode in GoogleMaps.</h3>
    """
    image = '<img  src="data:image/png;base64,' + base64.b64encode(image_file.read()) + '"/>'
    gmap = """
    <iframe id="map" style="width:512px; height:668px"
    src="//www.google.com/maps/embed/v1/place?q=Seattle,WA,USA&zoom=10&key={}">
    </iframe>
    """.format(google_api_key)
    return (head + '<body>' + image + table + gmap + '</body>' + '</html>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
