import hashlib
import requests
import sys
from pathlib import Path
import os
def tk_get_file_path():
    try:
        import tkinter as tk
        from tkinter import filedialog
    except:
        print("Error: tkinter is not installed/available. Please install and try again")
        sys.exit()
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    try:
        with open(file_path, 'r') as f:
            pass
    except:
        print("Cancelled")
        sys.exit()
    return file_path

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

def download(file_path):
    hash1 = str(get_hash(file_path))
    url = 'http://api.thesubdb.com/?action=download&hash='+ hash1 +'&language=en'
    header = { "user-agent": "SubDB/1.0 (Subtitle; https://github.com/avjt28/Subtitle.git)" }
    req = requests.get(url, headers=header)
    if req.status_code == 200:
        data = req.content
        filename = Path(file_path).with_suffix('.srt')
        with open(filename, 'wb') as f:
            f.write(data)
        f.close()
        print("Subtitle Downloaded Successfully")
    elif req.status_code == 400:
        print('Error:400  =  the request was malformed')
    elif req.status_code == 404:
        print('Error:404  =  the subtitle doesnt exist on the server')
    else:
        print('Unknown Error')

file_path = tk_get_file_path()
download(file_path)
