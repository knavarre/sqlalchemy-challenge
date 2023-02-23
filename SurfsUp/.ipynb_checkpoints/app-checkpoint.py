# import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify

#Database Setup
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(autoload_with=engine)

measurement = Base.classes.measurement
station = Base.classes.station

last_date = dt.date(2017, 8, 23)
one_year_prior = last_date - dt.timedelta(days = 365)
best_station = 'USC00519281'

#Flask set up 
app = Flask(__name__)

@app.route('/')
def homepage():
    return f'''
    Welcome to surf API<br>
    Available routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    '''

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).\
        filter((measurement.date >= one_year_prior) & (measurement.date <= last_date)).all()

    precp_results = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precp_results.append(precip_dict)
    
    session.close()
    return jsonify(precp_results)


@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    station_list = session.query(station.station).all()

    session.close()
    return jsonify(station_list)



@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

    temp_data = session.query(measurement.date, measurement.tobs).\
        filter((measurement.date >= one_year_prior) & (measurement.date <= last_date) & (measurement.station == best_station)).\
        all()
    
    return jsonify(temp_data)

@app.route('/api/v1.0/<start>')
def start_date(start):
    session = Session(engine)

    day_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).all()

    session.close()
    return jsonify(day_results)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):

    return

if __name__ == "__main__":
    app.run(debug=True)
