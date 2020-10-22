#-----------------------------------------------
#Libraries
#-----------------------------------------------

#Libraries used:
#RPi.GPIO - Standard Raspberry Pi GPIO library

#Try to import the libraries and exit the program if some are missing
try:
    import RPi.GPIO as GPIO
except RuntimeError as e:
    print(e)
    sys.exit(1)


#-----------------------------------------------
#Constants
#-----------------------------------------------

#Default Pins
DEFAULT_HIGHLOCK = 37 #sets to voltage high for on, and low for off
DEFAULT_GROUNDLOCK = 39 #always set to ground, never used

#-----------------------------------------------
#Global Variables
#-----------------------------------------------

#Flags
#-----------------------------------------------
_lock_open = None

#-----------------------------------------------
#Functions
#-----------------------------------------------

#Setup Functions
#-----------------------------------------------
def initialize_gpio(high_lock=DEFAULT_HIGHLOCK,lock_open = True):
    global _lock_open

    #Set all the global variables
    _lock_open = lock_open
    
    #Set GPIO mode to board
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    #Initialize row pins as output pins with a default high logic value
    GPIO.setup(high_lock, GPIO.OUT)
    if _lock_open == True:
      GPIO.output(high_lock, GPIO.LOW)
    else:
      GPIO.output(high_lock, GPIO.HIGH)

#Boolean Functions
#-----------------------------------------------
def close_lock():
  global _lock_open
  GPIO.output(DEFAULT_HIGHLOCK, GPIO.HIGH)
  _lock_open = False

def open_lock():
  global _lock_open
  GPIO.output(DEFAULT_HIGHLOCK, GPIO.LOW)
  _lock_open = True
  
#Main function
#-----------------------------------------------
#Dispose of this when done. Shouldn't be part of library, its only for testing

if __name__ == "__main__":
    try:
        initialize_gpio()
        while True:
            lockstate = input("Close lock? (Y/N) ")
            print("your input was: "+lockstate)

            if lockstate=="Y":
                close_lock()
            elif lockstate=="N":
                open_lock()
            else:
                print("invalid input")


    except Exception as e:
        print(e)

#TODO: Figure out how how to make the GPIO.LOW voltage even lower so magnet isn't semi hard
#TODO: Figure out why the code runs on a Thonny IDE but not on the commandline
