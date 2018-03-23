import json

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    data = {'chart_data': [
                            {'Date': '2008-03-31 20:00:00', 'Label': 18.79},
                            {'Date': '2009-03-30 21:00:00', 'Label': 17.76},
                            {'Date': '2009-03-27 04:01:21', 'Label': 18.62},
                            {'Date': '2009-01-02 14:15:04', 'Label': 20.4}
                          ]
           }


    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)