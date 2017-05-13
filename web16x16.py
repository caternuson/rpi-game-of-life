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
import tornado.websocket

import Matrix16x16
import GOL

ROOT_DIR = os.getcwd()
PORT = 80

m = Matrix16x16.Matrix16x16()
gol = GOL.GOL()
someoneConnected = False

class MainHandler(tornado.web.RequestHandler):
    """Handler for server root."""
   
    def get(self, ):
        print "Main handler."
        if someoneConnected:
            self.render("404.html")
        else:
            gol.pause()
            self.render("web16x16.html")

class WSCounterHandler(tornado.websocket.WebSocketHandler):
    """Handle the websocket connection for monitoring user connectedness."""
    
    def open(self,):
        """Callback for when websocket is opened."""
        global someoneConnected
        someoneConnected = True
        
    def on_close(self, ):
        """Callback for when websocket is closed."""
        global someoneConnected
        someoneConnected = False
        gol.restart()
        
class AjaxDisplayHandler(tornado.web.RequestHandler):
    """Handle grid display button clicks."""
    
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
    
class AjaxRunHandler(tornado.web.RequestHandler):
    """Handle RUN button."""
    
    def post(self, ):
        json_data = json.loads(self.request.body)
        json_uni = json_data['uni']
        U = [[0 for x in xrange(18)] for y in xrange(18)]
        for y in xrange(16):
            rowByte = json_uni['{0}'.format(y)]
            for x in xrange(16):
                U[1+15-x][1+y] = rowByte & 0x01
                rowByte >>= 1
        gol.runUniverse(U)
        resp = {'':''}
        self.write(json.dumps(resp))

class MainServerApp(tornado.web.Application):
    """Main Server application."""
    
    def __init__(self):
        handlers = [
            (r"/",                  MainHandler),
            (r"/ajax_display",      AjaxDisplayHandler),
            (r"/ajax_run",          AjaxRunHandler),
            (r"/ws_counter",        WSCounterHandler),
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
    try:
        gol.start()
        tornado.httpserver.HTTPServer(MainServerApp()).listen(PORT)
        print "Server started on port {0}.".format(PORT)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        gol.kill()
        gol.join()