from flask import Flask, render_template

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
@app.route('/area/<int:area_id>/<int:catalogitem_id>/')
def myAreas(area_id, catalogitem_id):
    #area = session.query(Area).all()
    areas = session.query(Area).filter_by(id = area_id)
    properties = session.query(CatalogItem).filter_by(id = catalogitem_id)
    return render_template('areas.html', areas=areas, properties=properties)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)