# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
#1.	/
#o	Start at the homepage.
#o	List all the available routes.

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"List of available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )
#2.	/api/v1.0/precipitation
#o	Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#o	Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitaion():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_ago
    year_ago_data = session.query(Measurement.date , Measurement.prcp).\
        filter(Measurement.date >= year_ago).\
        order_by(Measurement.date).all()
    precipitation = {date: prcp for date, prcp in year_ago_data}
    return jsonify(precipitation)


#3.	/api/v1.0/stations
#o	Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    list_station = session.query(Measurement.station).distinct().all()
    list_station
    stations = list(np.ravel(list_station))
    return jsonify(stations)

#4.	/api/v1.0/tobs
#o	Query the dates and temperature observations of the most-active station for the previous year of data.
#o	Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def temperature():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_ago
    past_12_mo = session.query(Measurement.station , Measurement.tobs).\
        filter(Measurement.station =="USC00519281").\
        filter(Measurement.date >=year_ago).\
        order_by(Measurement.date).all()
    temp = list(np.ravel(past_12_mo))
    return jsonify(temp)

#5.	/api/v1.0/<start> and /api/v1.0/<start>/<end>
#o	Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#o	For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#o	For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end 
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def averages(start=None, end=None):
    
    avg = [Measurement.station,
           func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]
    active_averages = session.query(*avg).\
    filter(Measurement.date >= start).all()
    filter(Measurement.date >= end).all()
    active_averages
    
    averages = list(np.ravel(active_averages))
    return jsonify(averages)


if __name__ == "__main__":
    app.run(debug=True)