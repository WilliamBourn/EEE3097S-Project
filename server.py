from http.server import BaseHTTPRequestHandler, HTTPServer

import EOZ_IP40 as Keypad
import RS_Pro_150N as Lock
import RPi.GPIO as GPIO  

Lock1 = Lock.Maglock()
Keypad1 = Keypad.Keypad()

class RequestHandler_httpd(BaseHTTPRequestHandler):
  Request = []
  
  maincode = []
  tempcode = []
  
  
  
  def do_GET(self):
    messagetosend = bytes('Welcome to the dodgy security way of transferring data to the pi api',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    self.Request = self.requestline
    self.Request = self.Request[5 : int(len(self.Request)-9)]
    
    #print(self.Request)
    
    if self.Request =="favicon.ico":
      pass #do nothing, this thing is just annoying

    elif self.Request == 'on':
      Lock1.activate_lock() #should activate lock
      print("Lock activation request sent")      

    elif self.Request == 'off':
      Lock1.deactivate_lock()
      print("Lock deactivation request sent")

    else: #else statement is here so the code bellow doesn't break it
      code = self.Request[int(len(self.Request)-4):] 
      self.Request = self.Request[:int(len(self.Request)-5)]
      print("the passcode command is: "+  self.Request)
      print("the code to be set is: "+ code)
      
    if self.Request == 'setMain':
      self.maincode = code
      print("MainPasscode change request sent")

    
    if self.Request == 'setTemp':
      self.tempcode = code
      print("TempPasscode change request sent")

    return

server_address_httpd = ('192.168.0.120',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Starting Server')
httpd.serve_forever()
