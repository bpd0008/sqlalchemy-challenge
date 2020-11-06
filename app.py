
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
b = automap_base()

# reflect the tables
b.prepare(engine, reflect=True)

# Save references to each table
Measurement = b.classes.measurement
Station = b.classes.station


session = Session(engine)
d_1y = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

d_1y =dt.datetime.strptime(d_1y, "%Y-%m-%d")

y_a = ((d_1y)) - dt.timedelta(days=365)

session.close()

app = Flask(Climate_Challenge)

@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Welcome!<br/> "
        f"Routes:<br/>"
        f"<br/>"  
        f"Precipitation Data/Dates<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Stations/Names<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"TEMPERATURES:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Min/Max/Avg. Temp<br/>"
        f"/api/v1.0/min_max_avg/&lt;start date&gt;<br/>"
        f"<br/>"
        f"Start/End Min/Max/Avg.<br/>"
        f"/api/v1.0/min_max_avg/&lt;start date&gt;/&lt;end date&gt;<br/>"
        f"<br/>"
        f"i.e. <a href='/api/v1.0/min_max_avg/2012-01-01/2016-12-31' target='_blank'>/api/v1.0/min_max_avg/2012-01-01/2016-12-31</a>"
    )


####
@app.route("/api/v1.0/precipitation")
def precipitation():
   
    session = Session(engine)
   
    res = session.query(Measurement.date, Measurement.prcp).all()
        
    session.close()
    
    
    precip = []
    for result in res:
        r = {}
        r[result[0]] = result[1]
        precip.append(r)

    return jsonify(precip)


####
@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    res = session.query(Station.station, Station.name).all()
    
    session.close()
    
    station_s = []
    for result in res:
        r = {}
        r["station"]= result[0]
        r["name"] = result[1]
        station_s.append(r)
    
    return jsonify(station_s)

####
@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    res = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= y_a).all()

    session.close()
    
    tobs_l = []
    for result in res:
        r = {}
        r["date"] = result[1]
        r["temprature"] = result[0]
        tobs_l.append(r)

    return jsonify(tobs_l)

####
@app.route("/api/v1.0/min_max_avg/<start>")
def start(start):
    
    session = Session(engine)

    dt = dt.datetime.strptime(start, '%Y-%m-%d')
    res = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= dt).all()

    session.close()

    t_l = []
    for result in res:
        r = {}
        r["StartDate"] = start_dt
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        t_l.append(r)

    return jsonify(t_l)


#####
@app.route("/api/v1.0/min_max_avg/<start>/<end>")
def start_end(start, end):
   
    session = Session(engine)
    
    
    startt = dt.datetime.strptime(start, '%Y-%m-%d')
    endt = dt.datetime.strptime(end, "%Y-%m-%d")

    res = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= startt).filter(Measurement.date <= endt)

    session.close()

    
    t_l = []
    for result in res:
        r = {}
        r["StartDate"] = startt
        r["EndDate"] = endt
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        t_l.append(r)

    
    return jsonify(t_l)

#######

if Climate_Challenge == "__main__":
    app.run(debug=True)
