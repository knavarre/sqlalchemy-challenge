#import dependencies
import numpy as np
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

#set variables to be used later
last_date = dt.date(2017, 8, 23)
one_year_prior = last_date - dt.timedelta(days = 365)
best_station = 'USC00519281'

#Flask set up 
app = Flask(__name__)

@app.route('/')
def homepage():
    #Provide list of all available routes
    return f'''
    Welcome to surf API<br>
    <br>
    Available routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    <br>
    For the following routes, please use YYYY-MM-DD as the format for inserting dates.<br> 
    /api/v1.0/input_date<br> 
    /api/v1.0/input_start_date/input_end_date<br>
    '''

@app.route('/api/v1.0/precipitation')
def precipitation():
    #open session
    session = Session(engine)

    #Query measurement table for date and precipitation data
    results = session.query(measurement.date, measurement.prcp).\
        filter((measurement.date >= one_year_prior) & (measurement.date <= last_date)).all()

    #Convert query results to a dictionary using date as the key and prcp as the value
    precp_results = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precp_results.append(precip_dict)
    
    #close session
    session.close()

    #jsonify and return results
    return jsonify(precp_results)


@app.route('/api/v1.0/stations')
def stations():
    #open session
    session = Session(engine)

    #Query station table for stations
    station_results = session.query(station.station).all()

    #Convert station_results to list
    station_list = list(np.ravel(station_results))

    #close session
    session.close()

    #jsonify and return results
    return jsonify(station_list)



@app.route('/api/v1.0/tobs')
def tobs():
    #open session
    session = Session(engine)

    #Query measurement table for temperature observation data
    temp_data = session.query(measurement.tobs).\
        filter((measurement.date >= one_year_prior) & (measurement.date <= last_date) & (measurement.station == best_station)).\
        all()
    
    #Convert station_results to list
    temp_list = list(np.ravel(temp_data))

    #close session
    session.close()
    
    #jsonify and return results
    return jsonify(temp_list)

@app.route('/api/v1.0/<start>')
def start_date(start):
    #open session
    session = Session(engine)

    #Convert start input into datetime format
    start = dt.datetime.strptime(start, '%Y-%m-%d').date()

    #Query measurements table for min, max, and avgerage values based on start input 
    day_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()

    #close session
    session.close()

    #return results in f'string
    return f'The lowest temperature is {day_results[0][0]}. The highest temperature is {day_results[0][1]}.\
         The average temperature is {day_results[0][2]}.'
    

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    #open session
    session = Session(engine)

    #Convert start and end inputs to datetime format
    start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end = dt.datetime.strptime(end, '%Y-%m-%d').date()

    #Query measurements table for min, max, and avgerage values based on start and end inputs 
    day_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter((measurement.date >= start) & (measurement.date <= end)).all()

    #close session
    session.close()

    #return results in f'string
    return f'The lowest temperature is {day_results[0][0]}. The highest temperature is {day_results[0][1]}.\
         The average temperature is {day_results[0][2]}.'

if __name__ == "__main__":
    app.run(debug=True)
