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

def get_soup(site):
    print("url", site)
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
    print("iphone", iphone_url)
    root.iphone_image = get_image(iphone_url)

    ipad_url = image_div.find("a", "ipad")['href']
    print("ipad", ipad_url)
    root.ipad_image = get_image(ipad_url)

    small_url = desktop_button.find_all("a")[0]['href']
    print("small", small_url)
    root.small_image = get_image(small_url)

    medium_url = desktop_button.find_all("a")[1]['href']
    print("medium", medium_url)
    root.medium_image = get_image(medium_url)

    large_url = desktop_button.find_all("a")[1]['href']
    print("large", large_url)
    root.large_image = get_image(large_url)

def get_image(image_url):
    u = urllib.request.urlopen(image_url)
    raw_data = u.read()
    u.close()

    image_data = Image.open(BytesIO(raw_data))
    return ImageTk.PhotoImage(image_data)
    
def play_mp3():
    p = vlc.MediaPlayer(song_url)
    p.play()

def resize_image(event):
    show_image(event.width, event.height)

def show_image(width, height):
    if width >= 2100:
        label.configure(image=root.large_image)
        print(width, "large")
    elif width >= 1600:
        label.configure(image=root.medium_image)
        print(width, "medium")
    elif width >= 1000:
        label.configure(image=root.small_image)
        print(width, "small")
    elif width >= 680:
        label.configure(image=root.ipad_image)
        print(width, "ipad")
    else:
        label.configure(image=root.iphone_image)
        print(width, "iphone")

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

get_images()
show_image(root.winfo_width(), root.winfo_height())

root.mainloop()

