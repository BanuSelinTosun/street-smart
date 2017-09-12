from flask import Flask, request
import matplotlib.pyplot as plt
from StringIO import StringIO
import base64
import Output
import pandas as pd
app = Flask(__name__)
Matrix = pd.read_pickle('Predicted_Matrix.p')
with open ('../google_api_key') as f:
    google_api_key = f.read()

# Form page to submit text
@app.route('/')
def submission_page():
    return '''
        <h1>Maximize Life Within Budget</h1>
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
        p {font-family: Arial; font-weight: bold; color: white;
        text-shadow: 2px 2px 4px #000000;}
        tr {font-family: Arial; color: white; font-weight: bold}
        body {background-image: url("static/Seattle_SeaFront.jpg"); background-size:cover; text-shadow: 2px 2px 4px #000000;}
        </style>
        <body>
        <form action="/Zipcode_Recommender" method='POST' >
        <table>
        <tr>
          <td> The average SqFT you are looking for: </td>
          <td> <input type="text" name="SqFtLiving" /> </td>
        </tr>
        <tr>
          <td> The number of Bedrooms you are looking for: </td>
          <td> <input type="text" name="Bedrooms" /> </td>
        </tr>
        <tr>
          <td> The age of each kid in the household, (in format e.g. 1 2 3)
               If not don't have kids and not planning to, just leave it empty.
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
    age_lst = [int(x) for x in ages.split()]
    SqFtLiving = str(request.form['SqFtLiving'])
    Bedrooms = str(request.form['Bedrooms'])
    output_table = Output.output_html(Matrix, age_lst, float(SqFtLiving), float(Bedrooms))
    fig = Output.outplot(Matrix, age_lst, float(SqFtLiving), float(Bedrooms))
    image_file = StringIO()
    fig.savefig(image_file, facecolor=fig.get_facecolor(), edgecolor='none')
    image_file.seek(0)
    table = '<table>' + '\n'.join(list(output_table)) + '</table>'
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
    iframe {position:absolute; top:349px; left:710px; right:0; bottom:0; height:100%;
    width:100%;}
    h2 {font-family: Arial; color: white; color: white; text-shadow: 2px 2px 4px #000000;}
    </style>
    </head>
    <h2>You can click on the column names to sort the table.</h2>
    """
    image = '<img  src="data:image/png;base64,' + base64.b64encode(image_file.read()) + '"/>'
    gmap = """
    <iframe id="map" style="width:544px; height:640px"
    src="//www.google.com/maps/embed/v1/place?q=Seattle,WA,USA&zoom=11&key={}">
    </iframe>
    """.format(google_api_key)
    return (head + '<body>' + image + table + gmap + '</body>' + '</html>')



@app.route('/plot.png')
def get_graph():
    plt.figure()
    n = 10
    plt.plot(range(n), [random() for i in xrange(n)])
    image = StringIO()
    plt.savefig(image)
    return image.getvalue(), 200, {'Content-Type': 'image/png'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
