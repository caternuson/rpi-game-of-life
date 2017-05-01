#===============================================================================
# web16x16.py
#
# Web interface for controlling 16x16 LED matrix.
#
# Uses Tornado to create web frame work for serving content. Matrix is
# comprised of two Adafruit 8x16 LED matrix displays.
#
# 16x16 LED Matrix Configuration
#
#       ---x   
#       | +--------+
#       y |        |
#         |        |
#         |        |
#         +--------+
#
# 2017-04-30
# Carter Nelson
#===============================================================================
import os
import json

import tornado.httpserver
import tornado.web

import Matrix16x16

ROOT_DIR = os.getcwd()
PORT = 8080

m = Matrix16x16.Matrix16x16()

class MainHandler(tornado.web.RequestHandler):
    """Handler for server root."""
   
    def get(self, ):
        print "Main handler."
        self.render("web16x16.html")
        
class AjaxClickHandler(tornado.web.RequestHandler):
    """Handle AJAX button clicks."""
    
    def post(self, ):
        json_data = json.loads(self.request.body)
        #print("Button click handler: {0}".format(json_data))
        state = self.__handleClick(json_data)
        resp = {'state': state}
        self.write(json.dumps(resp))
        
    def __handleClick(self, json_data):
        val = int(json_data['id'],0)
        x = val % 16
        y = val / 16
        state = not json_data['state']
        #print("val={0},x={1},y={2},state={3}".format(val,x,y,state))
        m.set_pixel(x,y, state)
        m.write_display()
        return state

class MainServerApp(tornado.web.Application):
    """Main Server application."""
    
    def __init__(self):
        handlers = [
            (r"/",                  MainHandler),
            (r"/ajaxclick",         AjaxClickHandler),
        ]
        
        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        }
        
        tornado.web.Application.__init__(self, handlers, **settings)

#--------------------------------------------------------------------
# M A I N 
#--------------------------------------------------------------------
if __name__ == '__main__':
    tornado.httpserver.HTTPServer(MainServerApp()).listen(PORT)
    print "Server started on port {0}.".format(PORT)
    tornado.ioloop.IOLoop.instance().start()
