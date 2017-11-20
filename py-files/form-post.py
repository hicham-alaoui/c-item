from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from properties_db import Base, Area, CatalogItem

import cgi
app = Flask(__name__)

# Create session and connect to DB
engine = create_engine('sqlite:///properties_list.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Objective 3 Step 2 - Create /restarants/new page
            if self.path.endswith("/areas/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Area</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/areas/new'>"
                output += "<input name = 'newAreaName' type = 'text' placeholder = 'New Area Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/areas"):
                myAreas = session.query(Area).all()
                output = ""
                # Objective 3 Step 1 - Create a Link to create a new menu item
                output += "<a href = '/areas/new' > Add new Area </a></br></br>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for myArea in myAreas:
                    output += myArea.name
                    output += "</br>"
                    # Objective 2 -- Add Edit and Delete Links
                    output += "<a href ='#' >Edit </a> "
                    output += "</br>"
                    output += "<a href =' #'> Delete </a>"
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Objective 3 Step 3- Make POST method
    def do_POST(self):
        try:
            if self.path.endswith("/areas/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newAreaName')

                    # Create new Restaurant Object
                    newArea = Restaurant(name=messagecontent[0])
                    session.add(newArea)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/areas')
                    self.end_headers()

        except:
            pass




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=9000)