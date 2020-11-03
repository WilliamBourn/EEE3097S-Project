#-----------------------------------------------
#Libraries
#-----------------------------------------------

#Libraries used:
#sys - System
#BaseHTTPRequestHandler - A request handler for the HTTP protocol
#HTTPServer - Server implementation for the HTTP protocol
#threading - Concurrent thread implementation
#time - Standard timing library
#RPi.GPIO - Standard Raspberry Pi GPIO library
#EOZ_IP40 - API module for keypad
#RS_Pro_150N - API module for magnetic lock

#Try to import the libraries and exit the program if some are missing
import sys
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import threading
    
    import time

    import RPi.GPIO as GPIO  
    import EOZ_IP40 as Keypad
    import RS_Pro_150N as Lock
except Exception as e:
    print(e)
    sys.exit(1)


#-----------------------------------------------
#Global Variables
#-----------------------------------------------

#Hardware module objects
Lock1 = Lock.Maglock(lock_open=False)       #The object associated with the magnetic lock hardware module
Keypad1 = Keypad.Keypad(key_buffer_en=True)     #The object associated with the keypad hardware module

#Passcodes
maincode = []       #The permanent passcode, does not reset after use
tempcode = []       #The temporary passcode, resets after use


#-----------------------------------------------
#Class Definition
#-----------------------------------------------

#N.B.!: Due to time contraints, this demonstrator does not possess end-to-end encryption, or device authentication measures. This demonstrator was meant to show
# how the hardware modules could be remotely accessed and does not contain the security features that a real world implementation of the hardware would require
# to function without security breaches.
class RequestHandler_httpd(BaseHTTPRequestHandler):
  
  
#-----------------------------------------------
#Class Variables
#-----------------------------------------------
  
    Request = []      #The HTTP request message received by the server


#-----------------------------------------------
#Class Functions
#-----------------------------------------------

    def do_GET(self):
        """The server receive callback method for use by the server thread"""
        
        global maincode, tempcode
        
        #Catch exceptions
        try:
            #Send message to accessing device
            messagetosend = bytes('Connection Established',"utf")
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', len(messagetosend))
            self.end_headers()
            self.wfile.write(messagetosend)
        
            #Receive HTTP request from accessing device
            self.Request = self.requestline
        
            #Remove extraneous information
            self.Request = self.Request[5 : int(len(self.Request)-9)]

            #Parse Request
            if self.Request =="favicon.ico":
                pass #do nothing, this thing is just annoying
            elif self.Request == 'on':
                #Activate Lock1
                Lock1.activate_lock()
                print("Lock activation request received")
                return     
            elif self.Request == 'off':
                #Deactivate Lock1
                Lock1.deactivate_lock()
                print("Lock deactivation request received")
                return
            else:
                #Extract 4-digit code from HTTP request
                code = self.Request[int(len(self.Request)-4):] 
                self.Request = self.Request[:int(len(self.Request)-5)]
            
            #Parse Request and Code
            if self.Request == 'setMain':
                #Set Permanent Passcode
                maincode = []
                for char in code:
                    maincode.append(char)
                print("MainPasscode change request received")
                return
            
            elif self.Request == 'setTemp':
                #Set Temporary Passcode
                tempcode = []
                for char in code:
                    tempcode.append(char)
                print("TempPasscode change request received")
                return
        except Exception as e:
            print(e)


#-----------------------------------------------
#Functions
#-----------------------------------------------


#Server Functions
#-----------------------------------------------

def start_server():
    """Creates a thread and runs the server on it indefinately"""
    
    #Start the server and run it until the user interupts it
    try:
        #Define the IP address of the server
        server_address_httpd = ('192.168.0.120',8080)       #I don't know how to implement this in a non-static manner
        
        #Create server and server thread
        httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
        server_thread = threading.Thread(target=httpd.serve_forever)
        
        #Start server
        server_thread.start()
        print('Starting Server')
    except KeyboardInterrupt:
        #Exit the system when the user requests
        sys.exit(0)


#Main Function
#-----------------------------------------------

def main():
    """Begins the HTTP server and listens for valid inputs from both the server and Keypad1 to control Lock1"""
    
    global maincode, tempcode
    
    #Initialize the server
    start_server()
    
    #Run until the user interupts the thread
    try:
        while True:
            
            #Reset the flag that controls automatic locking after a period of time
            close_lock_after_delay = False
            
            #Pass if a 4-digit code has not been entered
            if len(Keypad1.key_buffer) == 4:
                x = Keypad1.fetch_all()
                
                #Compare input code to the permanent and temporary codes
                if (len(maincode) == 4) & (x == maincode):
                    print("maincode entered correctly")
                    
                    #Deactivate Lock1
                    Lock1.deactivate_lock()
                    
                    #Raise flag
                    close_lock_after_delay = True
                elif (len(tempcode) == 4) & (x == tempcode):
                    print("tempcode entered correctly")
                    
                    #Deactivate Lock1
                    Lock1.deactivate_lock()
                    
                    #Raise flag
                    close_lock_after_delay = True
                    
                    #Empty the temporary code array, effectively deleting the code
                    tempcode = []
                else:
                    print("Password incorrect")
            
            #Check if error has occured and more than 4-digits have been inputted
            elif len(Keypad1.key_buffer) > 4:
                print("Error: too many inputs")
                
                #Remove all charcters from array and discard them
                x = Keypad1.fetch_all()
            
            #Begin countdown to automaticly lock after a certain period of time, if flag is raised
            if close_lock_after_delay == True:
                #Sleep for 10 seconds
                time.sleep(10)
                
                #Activate Lock1
                Lock1.activate_lock()
    
    except KeyboardInterrupt:
        #Cleanup the GPIO pins and exit the system when the user requests it
        Lock1.cleanup_gpio()
        Keypad1.cleanup_gpio()
        sys.exit(0)

#Run main method if file is called directly
if __name__ == "__main__":
    main()