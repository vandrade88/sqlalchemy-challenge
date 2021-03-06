import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify

database_path = "../Resources/hawaii.sqlite"

engine = create_engine(f"sqlite:///{database_path}")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
    f"Welcome to my Climate App!<br/>"
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    prev_year_prcp = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= previous_year).all()

    session.close()

    precip = {date: prcp for date, prcp in prev_year_prcp}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = session.query(Station.station).all()

    session.close()

    station_details = list(np.ravel(stations))
    
    return jsonify(station_details)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    prev_year_tobs = session.query(Measurement.station, Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= previous_year)\
        .filter(Measurement.station == 'USC00519281').all()

    session.close()

    tobs_details = list(np.ravel(prev_year_tobs))

    return jsonify(tobs_details)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    session = Session(engine)
    
    if not end:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start).all()

        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end).all()
        
    temps = list(np.ravel(results))
    return jsonify(temps)

    session.close()

if __name__ == "__main__":
    app.run(debug=True)
