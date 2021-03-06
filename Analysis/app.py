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

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
        
    results = session.query(Measurement.station, Measurement.date,\
        func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(func.strftime("%y-%m-%d", Measurement.date) == start).all()
    
    session.close()
    
    results_details = []
    for result in results:
        date_dict = {}
        date_dict["Station"] = result[0]
        date_dict["Date"] = result[1]
        date_dict["Min Temp"] = result[2]
        date_dict["Avg Temp"] = result[3]
        date_dict["Max Temp"] = result[4]
        results_details.append(date_dict)

    return jsonify(results_details)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)

    tobs = [Measurement.station, Measurement.date, 
       func.min(Measurement.tobs),
       func.avg(Measurement.tobs),
       func.max(Measurement.tobs)]

    results2 = session.query(*tobs)\
        .filter(func.strftime("%y-%m-%d", Measurement.date) >= start)\
        .filter(func.strftime("%y-%m-%d", Measurement.date) <= end).all()
    
    session.close()
    
    results2_details = []
    for result2 in results2:
        date_dict2 = {}
        date_dict2["Station"] = result2[0]
        date_dict2["Date"] = result2[1]
        date_dict2["Min Temp"] = result2[2]
        date_dict2["Avg Temp"] = result2[3]
        date_dict2["Max Temp"] = result2[4]
        results2_details.append(date_dict2)

    return jsonify(results2_details)  

if __name__ == "__main__":
    app.run(debug=True)
