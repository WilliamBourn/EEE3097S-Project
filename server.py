from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time

import EOZ_IP40 as Keypad
import RS_Pro_150N as Lock
import RPi.GPIO as GPIO  

Lock1 = Lock.Maglock()
Keypad1 = Keypad.Keypad(key_buffer_en=True)

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
      return     

    elif self.Request == 'off':
      Lock1.deactivate_lock()
      print("Lock deactivation request sent")
      return
      
    else: #else statement is here so the code bellow doesn't break it
      code = self.Request[int(len(self.Request)-4):] 
      self.Request = self.Request[:int(len(self.Request)-5)]
      print("the passcode command is: "+  self.Request)
      print("the code to be set is: "+ code)
      
    if self.Request == 'setMain':
      self.maincode = code
      print("MainPasscode change request sent")
      return
    
    elif self.Request == 'setTemp':
      self.tempcode = code
      print("TempPasscode change request sent")
      return
    
    return

def start_server():
  server_address_httpd = ('192.168.0.120',8080)
  httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
  thread = threading.Thread(target=httpd.serve_forever)
  thread.start()
  print('Starting Server')


start_server()

while True:
  
  close_lock_after_delay = False
  
  if len(Keypad1.key_buffer) == 4:
    x = Keypad1.fetch_all()
    if (len(maincode) == 4) & (x == maincode):
      print("maincode entered correctly")
      Lock1.deactivate_lock()
      close_lock_after_delay = True
    elif (len(tempcode) == 4) & (x == tempcode):
      print("tempcode entered correctly")
      Lock1.deactivate_lock()
      close_lock_after_delay = True
      tempcode = []
    else:
      print("Password incorrect")
      
  elif len(Keypad1.key_buffer) > 4:
    print("Error: too many inputs")
    x = Keypad1.fetch_all()

  if close_lock_after_delay == True:
    time.sleep(5)
    Lock1.activate_lock()
