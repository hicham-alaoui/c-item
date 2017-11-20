from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from properteez_db import Base, Area, CatalogItem

import cgi
app = Flask(__name__)

# Create session and connect to DB
engine = create_engine('sqlite:///properteez_list.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#all areas
@app.route('/')
@app.route('/areas/')
def allAreas():
	
    	all_areas = session.query(Area).all()
    	return render_template('all_areas.html', area=all_areas)

#new area
@app.route('/areas/new', methods=['GET','POST'])
def newArea():
	if request.method == 'POST':
		newarea = Area(name = request.form['name'])
		session.add(newarea)
		session.commit()
		return redirect(url_for('allAreas'))
	else:
		return render_template('new_area.html')

#edit area
@app.route('/areas/<int:area_id>/edit', methods=['GET','POST'])
def editArea(area_id):
	editarea = session.query(Area).filter_by(id=area_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editarea.name = request.form['name']
			session.add(editarea)
			session.commit()
			return redirect(url_for('allAreas'), )
	else:
		return render_template('edit_area.html', i=editarea)

#edit area
@app.route('/areas/<int:area_id>/delete', methods=['GET','POST'])
def deleteArea(area_id):
	deletearea = session.query(Area).filter_by(id=area_id).one()
	if request.method == 'POST':
		session.delete(deletearea)
		session.commit()
		return redirect(url_for('allAreas'))
	else:
		return render_template('delete_area.html', i=deletearea)

#single area method
@app.route('/area/<int:area_id>/')
def myAreas(area_id):
    areas = session.query(Area).filter_by(id = area_id)
    properties = session.query(CatalogItem).filter_by(area_id = area_id)
    return render_template('single_area.html', a=areas, properties=properties)

#Create a new catalog item
@app.route('/area/<int:area_id>/catalogitem/new', methods=['GET','POST'])
def newCatalogItem(area_id):
  area = session.query(Area).filter_by(id = area_id).one()
  if request.method == 'POST':
     newCatalogItem = CatalogItem(name = request.form['name'], description = request.form['description'],
                        city = request.form['city'], price = request.form['price'],
                        id = area_id)
     session.add(newCatalogItem)
     session.commit()
     return redirect(url_for('myAreas', id = area_id))
  else:
      return render_template('create_catalogitem.html', id = area_id)

#Edit a catalog item
@app.route('/area/<int:area_id>/catalogitem/<int:catalogitem_id>/edit', methods=['GET','POST'])
def editCatalogItem(area_id, catalogitem_id):
    editedItem= session.query(CatalogItem).filter_by(id = catalogitem_id).one()
    area = session.query(Area).filter_by(id = area_id)


    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['city']:
            editedItem.city = request.form['city']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
       
        return redirect(url_for('myAreas', area_id = area_id))
    else:
        return render_template('edit_catalogitem.html', area_id = area_id,
                                catalogitem_id = catalogitem_id, i=editedItem)

#Delete a catalog item
@app.route('/area/<int:area_id>/catalogitem/<int:catalogitem_id>/delete', methods = ['GET','POST'])

def deleteCatalogItem(area_id,catalogitem_id):
    itemArea = session.query(Area).filter_by(id = area_id)
    deletedCatalogItem = session.query(CatalogItem).filter_by(id = catalogitem_id).one()
   
    if request.method == 'POST':
        session.delete(deletedCatalogItem)
        session.commit()
        return redirect(url_for('allAreas'))
    else:
        return render_template('delete_catalogitem.html', item = deletedCatalogItem)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)