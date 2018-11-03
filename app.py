
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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







@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        
    )


@app.route("/api/v1.0/precipitation")
def preceipitation():
    """Return the justice league data as json"""
  
    
    measurement_list = []
    measurement_query = session.query(Measurement).filter(Measurement.date > '2016-08-24').filter(Measurement.date <= '2017-08-23').\
    order_by(Measurement.date).all()
    for measurement in measurement_query:
        measurement_dict = {}
        measurement_dict[measurement.date] = measurement.tobs
        measurement_list.append(measurement_dict)
        
    return jsonify(measurement_list)

@app.route("/api/v1.0/stations")
def stations():
    
    station_query = session.query(Station.station).all()

    station_list = list(np.ravel(station_query))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():


    tobs_query = session.query(Measurement.tobs).all()

    tobs_list = list(np.ravel(tobs_query))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<startdate>")
def tobs_by_date(startdate):

    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).all())


@app.route("/api/v1.0/<startdate>/<enddate>")
def tobs_by_date_range(startdate, enddate):

    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all())
#  /api/v1.0/'2016-08-24'/'2017-08-23'
if __name__ == "__main__":
    app.run(debug=True)
