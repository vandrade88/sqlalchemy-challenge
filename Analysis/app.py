#%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

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
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    prev_year_prcp = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= previous_year)\
        .order_by(Measurement.date).all()

    session.close()

    prev_year_prcp_list = []
    for date, prcp in prev_year_prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prev_year_prcp_list.append(prcp_dict)

    return jsonify(prev_year_prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = session.query(Station.station).all()

    session.close()
    
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    prev_year_tobs = session.query(Measurement.station, Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= previous_year)\
        .filter(Measurement.station == 'USC00519281').all()

    session.close()

    return jsonify(prev_year_tobs)

""" @app.route("/api/v1.0/<start>")
def tobs(start):
    session = Session(engine)

    session.close()

    return hello_dict """

""" @app.route("/api/v1.0/tobs/<start>/<end>")
def tobs(start/end):
    session = Session(engine)

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return hello_dict     """

if __name__ == "__main__":
    app.run(debug=True)
