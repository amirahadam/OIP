import os
import json
import re
from pathlib import Path
import requests
from sense_hat import SenseHat
from picamera import PiCamera
from tkinter import *

# tkinter GUI
root = Tk()
root.geometry("800x480")
root.title("NGT")
root.resizable(width = FALSE, height = FALSE)
label = Label()

# Sense HAT connection
sense = SenseHat()
sense.clear()

AFTER = None

# Cleaning state GUI
def cleaning():
    root.configure(background="deep sky blue") # set the colour to the next colour generated
    label.configure(text = "Cleaning in progress",
        fg = "snow",
        bg = "deep sky blue",
        font = "Helvetica 24 bold italic")
    label.pack()
    label.place(x=400, y=240, anchor="center")
    root.after(5000, drying) # run drying function after 5000ms

# Drying state GUI
def drying():
    root.configure(background="gold") # set the colour to the next colour generated
    label.configure(text = "Drying in progress",
        fg = "snow",
        bg = "gold",
        font = "Helvetica 24 bold italic")
    label.pack()
    label.place(x=400, y=240, anchor="center")
    root.after(1000,measureHumidity) # run measureHumidity function after 1000ms

# Ready state GUI
def ready():
    root.configure(background="green4") # set the colour to the next colour generated
    label.configure(text = "Syringes are ready",
        fg = "snow",
        bg = "green4",
        font = "Helvetica 24 bold italic")
    label.pack()
    label.place(x=400, y=240, anchor="center")

# Measure Humidity function
def measureHumidity():    
    # humidity = 39 # static data for testing
    humidity = round(sense.get_humidity())
    AFTER = root.after(1000, measureHumidity)
    print(humidity)
    if humidity == 39:
        print("Normal Humidity")
        root.after_cancel(AFTER) # stop measuring when humidity level is 39
        root.after(1000,CV) # run cv function after 1000ms
    return humidity

def CV():
    camera = PiCamera() # camera connection
    camera.capture('/home/pi/Desktop/OIP/image.jpg') #capture image
    file_paths = [
        os.path.join(Path().absolute(),'image.jpg'),
    ]
    # Slick AI API
    project_id = '119e1b41-4840-4972-9f86-beee7f9ca3ef'
    code = """curl --silent --request POST \
        --url https://app.slickk.ai/api/project/entryPoint \
        --header 'Accept: */*' \
        --header 'Accept-Language: en-US,en;q=0.5' \
        --header 'Connection: keep-alive' \
        --header 'Content-Type: multipart/form-data' \
        --form "projectId={1}" \
        {0}""".format(
        ' '.join(["--form data=@{0}".format(path) for path in file_paths]),
        project_id
        )
    # now we can execute this code
    results = os.popen(code).read()
    # the above returns a string, and it includes progress information, so let's remove that first
    results = re.sub(r'{"progress":\d+,"max":\d+}', "", results)
    # now we need to process it using the json library and load it into our program.
    results = json.loads(results)
    
    # results = [] # static data for testing
    if len(results) > 0:
        print([result["text"] for result in results])
        # for r in results:
        #     print(r) # static data for testing
    else:  # includes simplejson.decoder.JSONDecodeError
        # ValueError = If model does detect water droplets, syringe is dry
        print('Dry')
        root.after(1000,ready) # display Ready GUI
        # telegram feature
        bot_token = '1911295001:AAEMJNTZpKP5N22g5L4aM74KpcBoP8mwoY4'
        bot_chatID = '-424596188'
        send_text = 'https://api.telegram.org/bot'+ bot_token + '/sendMessage?chat_id='+ bot_chatID + '/&parse_mode=MarkdownV2&text=' + "Syringes are dry and ready for next use"
        response = requests.get(send_text)
        response.json()
    
# start of process
cleaning()

root.mainloop()
