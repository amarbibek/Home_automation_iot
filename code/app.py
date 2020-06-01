from flask import Flask, render_template
from flask_ask import Ask, statement, question
import RPi.GPIO as GPIO 

#init GPIO
GPIO.setwarnings(False)
ledPin = 11 #+ve pin
GPIO.setmode(GPIO.BOARD)    
GPIO.setup(ledPin, GPIO.OUT)   
GPIO.output(ledPin, GPIO.LOW) 
 
app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def launch():
    welcome_text = render_template('welcome_text')
    return question(welcome_text)

@ask.intent('AMAZON.FallbackIntent')
def fallback():
    reprompt_text = render_template('command_reprompt')
    return question(reprompt_text)

@ask.intent('OnOffIntent')
def control(OnOff):
    command = OnOff
    if command is None: 
        reprompt_text = render_template('command_reprompt')
        return question(reprompt_text)
    elif command == "on" or command == "off":
        if command == "off": 
            GPIO.output(ledPin, GPIO.LOW)
        else: 
            GPIO.output(ledPin, GPIO.HIGH)
        response_text = render_template('command', onOffCommand=command)
        return statement(response_text).simple_card('Command', response_text)
    else: 
        reprompt_text = render_template('command_reprompt')
        return question(reprompt_text)

if __name__ == '__main__':
    app.run(debug=True)
