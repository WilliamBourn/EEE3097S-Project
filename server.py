from http.server import BaseHTTPRequestHandler, HTTPServer

import EOZ_IP40 as Keypad
import RS_Pro_150N as Lock
import RPi.GPIO as GPIO  

Request = None


class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global Request
    messagetosend = bytes('Hello world',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    Request = self.requestline
    Request = Request[5 : int(len(Request)-9)]
    
    print(Request)
    Lock1 = Lock.Maglock()
    
    if Request == 'on':
      Lock1.activate_lock() #should activate lock
      print(Lock1.lock_pin) #testing the lock pin

    if Request == 'off':
      Lock1.deactivate_lock()
    return


server_address_httpd = ('192.168.0.120',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Starting Server')
httpd.serve_forever()
