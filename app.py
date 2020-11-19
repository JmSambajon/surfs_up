# Importing the Flask Dependency
from flask import Flask

# Create a New Flask App Instance
app = Flask(__name__)

# Create Flask Routes
@app.route('/')
def hello_world():
    return 'Hello world'

##test route
@app.route('/test')
def whats_up():
    return "What's up"

# Importing Dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Importing SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Setting up Database

# Accessing the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflecting the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Creating variables that reference specific tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Creating session link from Python to our database
session = Session(engine)

# Defining our Flask app
app = Flask(__name__)

# Creating a welcome statement with route references
# /api/v1.0/ signifies this is V1 of our application
# <br/> for new line via https://stackoverflow.com/questions/12244057/any-way-to-add-a-new-line-from-a-string-with-the-n-character-in-flask

@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end
    ''')

# Creating precipitation route
@app.route("/api/v1.0/precipitation")

def precipitation():
    # retrieves date and precipitation for previous year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    # returns file in json structured file
    return jsonify(precip)

# Creating stations route
@app.route("/api/v1.0/stations")

def stations():
    # retrieves all of the stations in our database
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    # returns file in json structured file
    return jsonify(stations=stations)


# Creating temperatures route
@app.route("/api/v1.0/tobs")

def temp_monthly():
    # Selecting the previous year data
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    # returns file in json structured file 
    return jsonify(temps=temps)

# Creating statistics route for minimum, average, and maximum temperatures
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    # Selecting the min, avg, and max temperatures
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        # returns file in json structured file    
        return jsonify(temps)

    # calculating the results with the temperature minimum, average, and maximum with the start and end dates
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    # returns file in json structured file    
    return jsonify(temps=temps)