from flask import Flask

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
def HelloWorld(area_id):
    area = session.query(Area).filter_by(id = area_id)
    output = ''
    for i in area:
        output += i.name
        output += '</br>'
    return output

@app.route('/area/<int:area_id>/new/')
def newAreaItem(area_id):
    return "this is the new area page"

@app.route('/area/<int:area_id>/<int:catalogitem_id>/edit/')
def editAreaItem(area_id, catalogitem_id):
    return "this is the edit area page"

@app.route('/area/<int:area_id>/<int:catalogitem_id>/delete/')
def deleteAreaItem(area_id, catalogitem_id):
    return "This is the delete area page"


@app.route('/area/catalogitem/<int:catalogitem_id>/')
def HelloWorld1(catalogitem_id):
    itemById = session.query(CatalogItem).filter_by(id = catalogitem_id)
    #allItems = session.query(CatalogItem).all()
    output = ''
    for i in itemById:
        output += i.name
        output += i.description
        output += i.price
        output += i.city
        output += '</br>'
    return output




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)