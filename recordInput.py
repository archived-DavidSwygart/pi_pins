#! /bin/python
import argparse, time, csv, warnings, signal, sys, os
from gpiozero import Button 
from datetime import datetime
from csv import DictWriter

#Parse recording settings
parser = argparse.ArgumentParser(description='Record GPIO pin 16')
parser.add_argument('--duration', '-d', 
                    type=int, 
                    help='Recording duration in seconds (default=86400s)',
                    default='86400')
parser.add_argument('--session', '-s', 
                    help='Name session, which determines the folder name in which the video will be saved defaults to date and time)'
                    )
args = parser.parse_args()



pins = [16]  # List of GPIO pins to monitor 
csvFields = ['Time', 'Pin', 'Event']

scriptPath = os.path.dirname(__file__)
hostname = os.uname().nodename
now = datetime.now().strftime("%Y%m%d_%H%M%S")

if args.session is None:
    session = now
else:
    session = args.session

saveDirectory = scriptPath + '/io/' + session + '/' + hostname

if os.path.exists(saveDirectory):
    warnings.warn("directory already exists for "+session+". Other recordings could already be in "+saveDirectory)
else:
    os.makedirs(saveDirectory)

saveFile = saveDirectory + '/' + now + '.csv'
print('SavingFile as '+saveFile)

# Create or open the CSV file and write the header 
with open(saveFile, "w", newline='') as csvfile: 
    writer = DictWriter(csvfile, fieldnames=csvFields) 
    writer.writeheader() 

def log_event(pin,event): 
    timeString = datetime.now().isoformat(sep='_', timespec='milliseconds')
    with open(saveFile, "a", newline='') as csvfile: 
        writer = DictWriter(csvfile, fieldnames=csvFields) 
        writer.writerow({'Time': timeString, 'Pin': pin, 'Event': event}) 

# Set up the GPIO pins and add event detection 
buttons = [Button(pin, bounce_time = 0.1) for pin in pins] 
for button in buttons: 
    button.when_released = lambda pin=button.pin.number: log_event(pin,'1') 
    button.when_pressed = lambda pin=button.pin.number: log_event(pin,'0') 

def endRecording(sig, frame):
    print('recordInput.py finished')
    sys.exit(0)

signal.signal(signal.SIGINT, endRecording)
signal.signal(signal.SIGTERM, endRecording)

print('waiting for a duration of '+str(args.duration) + ' seconds')
time.sleep(args.duration)
endRecording(0,None)
# try: 
#     print("Monitoring pins. Press Ctrl+C to exit.") 
#     while True: 
#         time.sleep(1) 
# except KeyboardInterrupt: 
#     print("Exiting...") 