'''

Polarisation Switching Flask application

Developed by Peter Goodhall 2M0SQL
Complete project details: https://github.com/magicbug/polarisation-switch

'''

import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   4 : {'name' : 'GPIO 4', 'state' : GPIO.LOW},
   22 : {'name' : 'GPIO 22', 'state' : GPIO.LOW},
   6 : {'name' : 'GPIO 4', 'state' : GPIO.LOW},
   26 : {'name' : 'GPIO 22', 'state' : GPIO.LOW},
   }

vartwo = ''
message = ''

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
   global vartwo 
   global message
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

@app.route("/phase/2m/<changephase>")
def changephase(changephase):
   global vartwo 
   global message

   deviceName = changephase

   if changephase== "rhcp":
      # Set the pin high:
      GPIO.output(4, GPIO.HIGH)
      GPIO.output(22, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "rhcp"

   if changephase == "lhcp":
      # Set the pin high:
      GPIO.output(4, GPIO.HIGH)
      GPIO.output(22, GPIO.LOW)
      # Save the status message to be passed into the template:
      message = "lhcp"

   if changephase == "v":
      GPIO.output(4, GPIO.LOW)
      GPIO.output(22, GPIO.LOW)
      message = "v"

   if changephase == "h":
      GPIO.output(4, GPIO.LOW)
      GPIO.output(22, GPIO.HIGH)
      message = "h"

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins,
      'message' : message,
      'vartwo': vartwo
   }

   return render_template('main.html', **templateData)

@app.route("/70cm/<phase>")
def phase(phase):
   global vartwo 
   global message

   deviceName = phase

   if phase== "rhcp":
      # Set the pin high:
      GPIO.output(6, GPIO.HIGH)
      GPIO.output(26, GPIO.HIGH)
      # Save the status message to be passed into the template:
      vartwo = "rhcp"

   if phase == "lhcp":
      # Set the pin high:
      GPIO.output(6, GPIO.HIGH)
      GPIO.output(26, GPIO.LOW)
      # Save the status message to be passed into the template:
      vartwo = "lhcp"

   if phase == "v":
      GPIO.output(6, GPIO.LOW)
      GPIO.output(26, GPIO.LOW)
      vartwo = "v"

   if phase == "h":
      GPIO.output(6, GPIO.LOW)
      GPIO.output(26, GPIO.HIGH)
      vartwo = "h"

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins,
      'message' : message,
      'vartwo': vartwo
   }

   return render_template('main.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
   global vartwo 
   global message

   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('main.html', **templateData)

@app.route("/api/status")
def api():
 return "Running"

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)