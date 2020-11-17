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
window_width, window_height = 0, 0

def get_soup(site):
    print(site)
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

def get_images():
    image_div = soup.find("div", "wallpaper")
    desktop_button = image_div.find("button", "desktop")

    iphone_url = image_div.find("a", "iphone")['href']
    root.iphone_image_data = get_image_data(iphone_url)

    ipad_url = image_div.find("a", "ipad")['href']
    root.ipad_image_data = get_image_data(ipad_url)

    small_url = desktop_button.find_all("a")[0]['href']
    root.small_image_data = get_image_data(small_url)

    medium_url = desktop_button.find_all("a")[1]['href']
    root.medium_image_data = get_image_data(medium_url)

    large_url = desktop_button.find_all("a")[1]['href']
    root.large_image_data = get_image_data(large_url)

def get_image_data(image_url):
    u = urllib.request.urlopen(image_url)
    raw_data = u.read()
    u.close()

    return Image.open(BytesIO(raw_data))

def play_mp3():
    p = vlc.MediaPlayer(song_url)
    p.play()

def resize_image(event):
    global window_width, window_height
    if window_width != event.width and window_height != event.height:
        window_width, window_height = event.width, event.height
        show_image(event.width, event.height)

def show_image(width, height):
    if width >= 100 and height >= 100:
        new_width = width - 20
        new_height = height - 40

        if width > 2133:
            size = "large"
            image_data = root.large_image_data
            original_width = 2133
            original_height = 1200
        elif width > 1600:
            size = "medium"
            image_data = root.medium_image_data
            original_width = 1600
            original_height = 900
        elif width > 1067:
            size = "small"
            image_data = root.small_image_data
            original_width = 1067
            original_height = 600
        elif width > 640:
            size = "ipad"
            image_data = root.ipad_image_data
            original_width = 1536
            original_height = 2048
        else:
            size = "iphone"
            image_data = root.iphone_image_data
            original_width = 640
            original_height = 1136

        if new_height < original_height:
            new_width = int(new_height * original_width / original_height)

        if new_width > width:
            new_width = width

        print("window", width, height, size)
        print("resize", new_width, new_height)

        if new_width >= 20 and new_height >= 20:
            resized = image_data.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(resized)
            label.config(image = photo)
            label.image = photo

root = Tk()
root.state('zoomed')
root.bind('<Configure>', resize_image)

button = ttk.Button(root, text='Play Again')
button.pack()
button.config(command=play_mp3)

image = PhotoImage(file = 'verses-bg.png')
label = Label(image=image, width = root.winfo_width(), height = root.winfo_height())
label.pack(fill=BOTH, expand=YES)

site = get_verse_url()
soup = get_soup(site)

song_url = get_song_url()
play_mp3() 

get_images()
show_image(root.winfo_width(), root.winfo_height())

root.mainloop()

