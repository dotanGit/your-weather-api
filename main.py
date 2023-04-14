from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data-jupyter-notebook/data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

@app.route("/")
def home():   # when a visitor clicks home the function is called
    return render_template("home.html", data=stations.to_html())

@app.route("/api/v1/<station>/<date>")
def about(station, date):   # when a visitor clicks home the function is called
    filename = "data-jupyter-notebook/data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]["   TG"].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}

@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data-jupyter-notebook/data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient='records')   # orient='records' change the format of the dictionary
    return result

@app.route("/api/v1/<station>")
def all_data_station(station):
    filename = "data-jupyter-notebook/data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient='records')   # orient='records' change the format of the dictionary
    return result

@app.route("/api/v1/yearly/<station>/<year>")
def all_data_station_year(station, year):
    filename = "data-jupyter-notebook/data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient='records')
    return result

if __name__ == "__main__":
    app.run(debug=True)
