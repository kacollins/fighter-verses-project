from bs4 import BeautifulSoup
import urllib
from urllib.request import Request, urlopen
import json
import tkinter
from tkinter import ttk
from io import BytesIO
from PIL import Image, ImageTk
import os
os.add_dll_directory(r"C:\Program Files (x86)\VideoLAN\VLC")
import vlc

song_url = ""
image_url = ""

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

def play_mp3():
    p = vlc.MediaPlayer(song_url)
    p.play()

def show_image():
    u = urllib.request.urlopen(image_url)
    raw_data = u.read()
    u.close()

    image_data = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(image_data)

    label = tkinter.Label(image=image)
    label.pack()
    root.mainloop()

root = tkinter.Tk()
root.state('zoomed')

site = get_verse_url()
soup = get_soup(site)

song_url = get_song_url()
play_mp3() 

button = ttk.Button(root, text='Play Again')
button.pack()
button.config(command=play_mp3)

image_url = get_image_url()
show_image()
