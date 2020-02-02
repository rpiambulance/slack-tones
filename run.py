import glob
import os
from datetime import datetime
from sys import argv

import requests
from dotenv import load_dotenv
from slack import WebClient

load_dotenv()

URL = os.getenv('URL')
VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
SLACK_TOKEN = os.getenv('SLACK_BOT_TOKEN')
CHANNEL = os.getenv('SLACK_CHANNEL')

d = datetime.now()


def uploadaudio():
    list_of_files = glob.glob('audio/*.mp3')
    latest_file = max(list_of_files, key=os.path.getctime)
    wc = WebClient(token=SLACK_TOKEN)
    wc.files_upload(
        channels=CHANNEL,
        file=latest_file
    )


if __name__ == "__main__":
    try:
        message = ""
        type_ = ""
        if len(argv) < 2 or argv[1].lower() == 'normal':
            type_ = 'normal'
            message = "TONES RECEIVED. Stand by for text message dispatch."
            if d.weekday() == 0 and d.hour == 18 and 0 <= d.minute <= 10:
                message = "TONES RECEIVED but likely to be the weekly pager test. Confirm a possible" \
                          " call using other means."
        elif argv[1].lower() == 'long':
            type_ = 'long'
            message = "LONGTONE (GROUP ALERT) RECEIVED. Stand by for further information."
            if d.weekday() == 5 and d.hour == 12 and 0 <= d.minute <= 10:
                message = "LONGTONE (GROUP ALERT) RECEIVED but likely to be the weekly all-call test. Confirm any" \
                          " possible message using other means."
        else:
            raise ValueError
        requests.post(url=URL, data={'message': message, "type": type_},
                      headers={"Authorization": f"BEARER {VERIFICATION_TOKEN}"})
        uploadaudio()
    except ValueError:
        print("Incorrect argument. Please use either 'normal' or 'long'")
