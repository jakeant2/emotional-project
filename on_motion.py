import pygame
import pygame.camera
import time
from datetime import datetime
import requests
import json
from json.decoder import JSONDecodeError
import tkinter as tk
import os

class Timer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-zoomed', True)
        self.configure(background='dark blue')
        self.label1 = tk.Label(self, text='Get Ready!', font='Times 56', width=80, bg='white', fg='black')
        self.label1.pack()
        self.label = tk.Label(self, text="", font='Times 300', fg='white', bg='dark blue')
        self.label.pack()
        self.remaining = 0
        self.countdown(5)

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining
        if self.remaining <= 0:
            self.destroy()
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

if __name__ == "__main__":
    app=Timer()
    app.mainloop()  


now = datetime.now()
date_time = now.strftime('%m-%d-%Y_%H:%M')

def Photo():
    pygame.camera.init()
    #pygame.camera.list_camera() #Camera detected or not
    cam = pygame.camera.Camera("/dev/video0",(640,480))
    cam.start()
    img = cam.get_image()
    global image_name
    image_name = 'image_' + date_time + '.jpg'
    pygame.image.save(img, image_name)
    time.sleep(1)
Photo()

def Analyze():
    image = os.path.join('/home/pi/Documents/', image_name)
    files = {
         'files': (image, open(image, 'rb')),
    }
    response = requests.post('https://api.emotuit.com/upload', files=files)
    try:
        global name
        name = date_time + "_result.json"
        file = open(name, 'wb')
        global data
        data = response.content
        write = file.write(data)
        pretty_json = json.loads(data)
        print(pretty_json)
    except JSONDecodeError:
        oops = tk.Tk()
        window_width = oops.winfo_reqwidth()
        window_height = oops.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        position_right = int(window_width/2)
        position_down = int(window_height/2)
        # Positions the window in the center of the page.
        oops.geometry("+{}+{}".format(position_right, position_down))
        main = tk.Label(oops, text='Oops!', font='Verdana 80 bold').pack()
        detail = tk.Label(oops, text='Your Photo could not be analyzed', font='Verdana 60').pack()
        oops.after(5000, oops.destroy)
        oops.mainloop()


Analyze()



def ResultUI():
    json_data = open(name, 'r')
    contents = json_data.read()
    try:    
        json_contents = json.loads(contents)

        #age = json_contents['age']
        #anger = json_contents['angry']
        #disgust = json_contents['disgust']
        #fear = json_contents['fear']
        #gender = json_contents['gender']
        #happy = json_contents['happy']
        #neutral = json_contents['neutral']
        #sadness = json_contents['sad']
        #surprise = json_contents['surprise']
        data_labels = ['Age', 'Anger', 'Disgust', 'Fear', 'Gender', 'Happiness', 'Neutral', 'Sadness', 'Surprise']
        #json_results = [age, anger, disgust, fear, gender, happy, neutral, sadness, surprise]

        top = tk.Tk()
        
        window_width = top.winfo_reqwidth()
        window_height = top.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        position_right = int(top.winfo_screenwidth()/2 - window_width/2)
        position_down = int(top.winfo_screenheight()/2 - window_height/2)
         
        # Positions the window in the center of the page.
        top.geometry("+{}+{}".format(position_right, position_down))

        title = tk.Label(top, text='Your Results:', font='Verdana 70 bold').grid(row=0, columnspan=2, sticky='NSEW')
        r = 1
        for d in data_labels:
            tk.Label(top, text=d, font='Fixedsys 45 bold', bg='white').grid(row=r, column=0, sticky='EW')
            r = r + 1
        q = 1
        #for j in json_results: # this needs to be made active when json results are fixed
        for j in json_contents: # this needs to be deleted when json results are fixed
            tk.Label(top, text=j, font='Fixedsys 45 italic', bg='white').grid(row=q, column=1, sticky='EW')
            q = q +1
        top.after(9000, top.destroy)
        top.mainloop()
        
    except JSONDecodeError:
        print('\nOopsie Daisies!')
ResultUI()

