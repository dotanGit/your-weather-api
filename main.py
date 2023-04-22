from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Read the stations file and select only the columns we need
stations = pd.read_csv("data-jupyter-notebook/data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

# Route for the home page
@app.route("/")
def home():
    # Pass the stations data as an html table to the home.html template
    return render_template("home.html", data=stations.to_html())

# Route for returning temperature data for a specific station and date
@app.route("/api/v1/<station>/<date>")
def about(station, date):
    # Create the filename from the station id
    filename = "data-jupyter-notebook/data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    # Read the temperature data for the station
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    # Select the temperature data for the specific date and divide by 10 to get Celsius
    temperature = df.loc[df['    DATE'] == date]["   TG"].squeeze() / 10
    # Return the temperature data as a dictionary
    return {"station": station,
            "date": date,
            "temperature": temperature}

# Route for returning all temperature data for a specific station
@app.route("/api/v1/<station>")
def all_data(station):
    # Create the filename from the station id
    filename = "data-jupyter-notebook/data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    # Read the temperature data for the station
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    # Convert the data to a list of dictionaries with each dictionary representing a row of data
    result = df.to_dict(orient='records')
    # Return the list of dictionaries
    return result

# Route for returning all temperature data for a specific station
@app.route("/api/v1/<station>")
def all_data_station(station):
    # Create the filename from the station id
    filename = "data-jupyter-notebook/data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    # Read the temperature data for the station
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    # Convert the data to a list of dictionaries with each dictionary representing a row of data
    result = df.to_dict(orient='records')
    # Return the list of dictionaries
    return result

# Route for returning all temperature data for a specific station and year
@app.route("/api/v1/yearly/<station>/<year>")
def all_data_station_year(station, year):
    # Create the filename from the station id
    filename = "data-jupyter-notebook/data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    # Read the temperature data for the station
    df = pd.read_csv(filename, skiprows=20)
    # Convert the date column to a string to check for the year
    df["    DATE"] = df["    DATE"].astype(str)
    # Select only the rows that have a date that starts with the year
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient='records')
    # Return the list of dictionaries
    return result

if __name__ == "__main__":
    app.run(debug=True)
