from http.server import BaseHTTPRequestHandler, HTTPServer

import EOZ_IP40 as Keypad
import RS_Pro_150N as Lock
import RPi.GPIO as GPIO  


class RequestHandler_httpd(BaseHTTPRequestHandler):
  Request = []
  
  maincode = []
  tempcode = []
  
  Lock1 = Lock.Maglock()
  Keypad1 = Keypad.Keypad()
  
  def do_GET(self):
    messagetosend = bytes('Hello world',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    self.Request = self.requestline
    Request = Request[5 : int(len(Request)-9)]
    
    print(Request)
    
    if self.Request == 'on':
      Lock1.activate_lock() #should activate lock
      print(Lock1.lock_pin) #testing the lock pin

    if self.Request == 'off':
      Lock1.deactivate_lock()

    code = self.Request[int(len(Request)-5):]    
    print(code)
    self.Request = self.Request[:int(len(Request)-5)]
    print(self.Request)

    if self.Request == 'setMain':
      self.maincode = code
    
    if self.Request == 'setTemp':
      self.tempcode = code

    return

server_address_httpd = ('192.168.0.120',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Starting Server')
httpd.serve_forever()
