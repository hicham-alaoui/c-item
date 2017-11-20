from flask import Flask, render_template, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from properteez_db import Base, Area, CatalogItem

import cgi
app = Flask(__name__)

# Create session and connect to DB
engine = create_engine('sqlite:///properteez_list.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/area/<int:area_id>/')
def myAreas(area_id):
    #area = session.query(Area).all()
    areas = session.query(Area).filter_by(id = area_id).one()
    properties = session.query(CatalogItem).filter_by(area_id = area_id)
    return render_template('areas.html', area=areas, properties=properties)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)