import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

database_path = "../Resources/hawaii.sqlite"

engine = create_engine(f"sqlite:///{database_path}")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

hello_dict = {"Hello": "World!"}

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

    return hello_dict

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    return hello_dict

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    return hello_dict

@app.route("/api/v1.0/<start>")
def tobs(start):
    session = Session(engine)

    return hello_dict

@app.route("/api/v1.0/tobs/<start>/<end>")
def tobs(start/end):
    session = Session(engine)

    return hello_dict    

if __name__ == "__main__":
    app.run(debug=True)
