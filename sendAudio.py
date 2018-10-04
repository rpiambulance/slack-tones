#!/usr/bin/python

import glob
import os
import requests
from auth_audio import *

list_of_files = glob.glob('audio/*.mp3')
latest_file = max(list_of_files, key=os.path.getctime)

audiofile = {'file': open(latest_file, 'rb')}

payload = {"token":slack_token,"channels":channels}

r = requests.post(url, params=payload, files=audiofile)
