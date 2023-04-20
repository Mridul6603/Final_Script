from tkinter import *
from tkinter import ttk
import inspect
import os
import ctypes
import apod_desktop
import apod_api
import requests
from apod_api import get_apod_info
from tkinter import messagebox
import image_lib
import tkinter as tk
import apod_api

# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the image cache
apod_desktop.init_apod_cache(script_dir)


# TODO: Create the GUI
root = Tk()
root.geometry('600x400')
root.title("Astronomy Picture of the Day Viewer")

# Set the window icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.APOS_Nasa_viewer')
icon_path = os.path.join(script_dir, 'image.ico')
root.iconbitmap(icon_path)
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)


#creating the frame
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

#adding the image to the frame
img_poke = PhotoImage(file=os.path.join(script_dir, 'nasa_image.png'))
lbl_poke = ttk.Label(frame, image=img_poke)
lbl_poke.grid(row = 0, column = 0, sticky = NSEW)

#add frames to window
frm_top_left = ttk.Frame(root)
frm_top_left.grid(row=10, column=10, columnspan=50)

#left side
frm_btm_left = ttk.LabelFrame(root, text = 'View Cached Image')
frm_btm_left.grid(row=1, column=0, padx= (10, 20), pady= (10, 20), sticky = SW)

lbl_name = ttk.Label(frm_btm_left, text='Select Image: ')
lbl_name.grid(row=10, column=5)

ent_name = ttk.Entry(frm_btm_left)
ent_name.grid(row=10, column=6)

#function for set as desktop
def desktop_handle():
    return
btn_hello = ttk.Button(frm_btm_left, text='Set as Desktop', command = desktop_handle)
btn_hello.grid(row = 10, column = 10, padx=10, pady=10)

#right side

frm_top_right = ttk.Frame(root)
frm_top_right.grid(row=10, column=50, columnspan=5)

frm_btm_right = ttk.LabelFrame(root, text = 'Get more images')
frm_btm_right.grid(row=1, column=1, padx= (10, 20), pady= (10, 20), sticky = SE)

lbl_name = ttk.Label(frm_btm_right, text='Select Date: ')
lbl_name.grid(row=10, column=15)

ent_name = ttk.Entry(frm_btm_right)
ent_name.grid(row=10, column=20)

#function for download handle
def download_handle():
    return

btn_hello = ttk.Button(frm_btm_right, text='Download Image', command = download_handle)
btn_hello.grid(row = 10, column = 25, padx=10, pady=10)


#add widgets to frames

root.mainloop()