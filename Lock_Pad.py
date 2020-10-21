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
#Variables
#-----------------------------------------------

#Constants
#-----------------------------------------------
#Default Pins
DEFAULT_HIGHLOCK = 37 #sets to voltage high for on, and low for off
DEFAULT_GROUNDLOCK = 39 #always set to ground, never used

#Global Variables
#-----------------------------------------------

#Flags
#-----------------------------------------------
_lock_open_en = None

#-----------------------------------------------
#Functions
#-----------------------------------------------

#Setup Functions
#-----------------------------------------------
def initialize_gpio(high_lock=DEFAULT_HIGHLOCK,lock_open_en=False):
    global _lock_open_en

    #Set all the global variables
    _lock_open_en = lock_open_en

    #Set GPIO mode to board
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    #Initialize row pins as output pins with a default high logic value
    GPIO.setup(high_lock, GPIO.OUT)
    GPIO.output(high_lock, GPIO.LOW)

#Boolean Functions
#-----------------------------------------------
def enable_lock_open(bool):
    global _lock_open_en
    _lock_open_en = bool

def close_lock():
  print("about to close lock") #for testing
  GPIO.output(DEFAULT_HIGHLOCK, GPIO.HIGH)
  print("closing lock") #for testing purposes

def open_lock():
  print("about to open lock") #for testing
  GPIO.output(DEFAULT_HIGHLOCK, GPIO.LOW)
  print("opening lock") #for testing purposes

#Main function
#-----------------------------------------------
#Dispose of this when done. Shouldn't be part of library, its only for testing

if __name__ == "__main__":
    try:
        initialize_gpio(lock_open_en=True)
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
