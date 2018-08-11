import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct
import datetime as dt

#Flask
from flask import Flask, jsonify

#Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

date = dt.date(2017, 8, 23)
year_ago = date - dt.timedelta(days= 365)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes.""" 
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation in last year"""
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).all()

    all_prec = list(np.ravel(results))
    return jsonify(all_prec)
       
@app.route("/api/v1.0/stations")
def station():
    results = session.query(distinct(Measurement.station)).all()

    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temp():
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago).all()

    temp_results = list(np.ravel(results))
    return jsonify(temp_results)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).filter(Measurement.date >=start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
    

if __name__ == '__main__':
    app.run(debug=True)