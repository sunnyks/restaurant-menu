
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Hello!</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                where_do_you_wanna_eat = session.query(Restaurant).all()
                output = ""
                output += "<html><h1>Where you tryna eat?</h1><body>"

                for restaurant in where_do_you_wanna_eat:
                    output += restaurant.name + "</br>"

                    output += "<a href=/restaurants/" + str(restaurant.id) + "/edit> Edit </a> </br>"
                    output += "<a href=/restaurants/" + str(restaurant.id) + "delete> Delete </a></br>"

                output +=  '''<a href=/restaurants/new> New Restaurant </a>
                            </body></html>'''
                self.wfile.write(output)
                return

            if self.path.endswith("restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                newForm = '''<html>
                            <form method='POST' enctype='multipart/form-data' action = '/restaurants/new'>
                            <h4> A new grub spot????? lay it on me bro! </h4>
                            <input name='tacobell' type='text'>
                            <input type='submit' value='Submit'>
                            </form>
                            </html>
                            '''

                self.wfile.write(newForm)
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                editForm = '''<html>
                            <form method='POST' enctype='multipart/form-data' action = 'resaurants/{}/edit'>
                            <h4> whats in a name, man </h4>
                            <input name='tacobell' type='text' placeholder = {}>
                            <input type='submit' value='Rename'>
                            </form>
                            </html>
                            '''.format(str(restaurantIDPath), str(myRestaurantQuery.name))

                self.wfile.write(editForm)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            #self.send_response(303)
            #self.send_header('Location', '/restaurants')
            #self.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                   fields = cgi.parse_multipart(self.rfile, pdict)
                   messagecontent = fields.get('tacobell')
                   newRestaurant = Restaurant(name = messagecontent[0])
                   session.add(newRestaurant)
                   session.commit()
                #read_formdata("add")
                self.send_response(303)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('tacobell')
                    path = str(self.path)
                    restaurantId = [int(s) for s in path.split() if s.isdigit()]
                    editRestaurant = session.query(Restaurant).filter_by(restaurant_id = restaurantId).one()
                    editRestaurant.name = messagecontent[0]
                    session.add(editRestaurant)
                    session.commit()
                #read_formdata("edit")
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('tacobell')
                    path = str(self.path)
                    restaurantId = [int(s) for s in path.split() if s.isdigit()]
                    closeRestaurant = session.query(Restaurant).filter_by(restaurant_id = restaurantId).one()
                    session.delete(closeRestaurant)
                    session.commit()
                #read_formdata("delete")
                self.send_response(303)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers

        except:
            pass

        # def read_formdata(self, action):
        #     ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        #     if ctype == 'multipart/form-data':
        #         fields = cgi.parse_multipart(self.rfile)
        #         messagecontent = fields.get('tacobell')
        #     if action == "add":
        #         newRestaurant = Restaurant(name = messagecontent[0])
        #         session.add(newRestaurant)
        #         session.commit()
        #     else:
        #          editRestaurant = session.query(Restaurant).filter_by(restaurant_id = get_rest_id()).one()
        #          if action == "edit":
        #              editRestaurant.name = messagecontent[0]
        #              session.add(editRestaurant)
        #              session.commit()
        #          if action == "delete":
        #              session.delete(editRestaurant)
        #              session.commit()
        #
        #
        # def get_rest_id(self):
        #     path = str(self.path)
        #     restaurantId = [int(s) for s in path.split() if s.isdigit()]
        #     return restaurantId


def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "okay bye"
        server.socket.close()


####

if __name__ == '__main__':
    main()
