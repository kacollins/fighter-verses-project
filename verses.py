from bs4 import BeautifulSoup
import urllib
from urllib.request import Request, urlopen
import json
from tkinter import *
from tkinter import ttk
from io import BytesIO
from PIL import Image, ImageTk
import re
import os
os.add_dll_directory(r"C:\Program Files (x86)\VideoLAN\VLC")
import vlc

song_url = ""
medium_image_url = ""

def get_soup(site):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def get_search_url():
    site = "https://fighterverses.com/"
    soup = get_soup(site)
    title = soup.title.string
    title = title.replace('Fighter Verses - ', '')
    title = title.replace('\r\n\t', '')
    url = "http://theversesproject.com/search?q=" + urllib.parse.quote(title)
    return url

def get_verse_url():
    site = get_search_url()
    soup = get_soup(site)
    verse_div = soup.find("div", "verse")
    song_data = json.loads(verse_div.find("button").attrs['data-songs'])[0]
    return "http://theversesproject.com" + song_data['verse_url']

def get_song_url():
    song_div = soup.find("div", "song")
    song_data = json.loads(song_div.find("button").attrs['data-songs'])[0]
    return song_data['mp3']

def get_image_url():
    image_div = soup.find("div", "background")    
    return image_div.attrs['data-url']

def update_image_url(width):
    image_url = medium_image_url
    m = re.match("http://s3.amazonaws.com/versesproject/verses/\d*/(\d*)", medium_image_url)
    number = int(m.group(1))

    if width > 1280:
        image_url = medium_image_url
    elif width > 1000:
        image_url = medium_image_url.replace('_medium', '_small')
    elif width > 680:
        image_url = medium_image_url.replace(str(number), str(number + 1)).replace('_desktop_medium', '_ipad_original')
    else:
        image_url = medium_image_url.replace(str(number), str(number + 2)).replace('_desktop_medium', '_iphone_original')

    print(width, image_url)
    return image_url
    
def play_mp3():
    p = vlc.MediaPlayer(song_url)
    p.play()

def show_image(image_url, width, height):
    u = urllib.request.urlopen(image_url)
    raw_data = u.read()
    u.close()

    image_data = Image.open(BytesIO(raw_data))
    resized = image_data.resize((width, height))
    root.image = ImageTk.PhotoImage(resized)

    label.configure(image=root.image)

def resize_image(event):
    image_url = update_image_url(event.width)
    show_image(image_url, event.width, event.height)

root = Tk()
root.state('zoomed')
root.bind('<Configure>', resize_image)

image = PhotoImage(file = 'verses-bg.png')
label = Label(image=image)
label.pack(fill=BOTH, expand=YES)

site = get_verse_url()
soup = get_soup(site)

song_url = get_song_url()
play_mp3() 

button = ttk.Button(root, text='Play Again')
button.pack()
button.config(command=play_mp3)

medium_image_url = get_image_url()
show_image(medium_image_url, 1025, 577)

root.mainloop()

