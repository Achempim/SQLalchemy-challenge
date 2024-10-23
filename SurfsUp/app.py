# Import the dependencies
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Connect to the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session (link) from Python to the database
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home route
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

# Route for precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data."""
    results = session.query(Measurement.date, Measurement.prcp).all()
    precip_data = {date: prcp for date, prcp in results}
    return jsonify(precip_data)

# Route for station data
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations."""
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# Route for temperature observations (tobs)
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations for the previous year."""
    last_year = "2016-08-23"  # Example: Define last year’s start date
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_year).all()
    temp_data = {date: tobs for date, tobs in results}
    return jsonify(temp_data)

# Route for temperature stats with start date only
@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return temperature stats from the start date onward."""
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()
    temp_stats = list(np.ravel(results))
    return jsonify(temp_stats)

# Route for temperature stats with start and end dates
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return temperature stats for a given date range."""
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp_stats = list(np.ravel(results))
    return jsonify(temp_stats)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

