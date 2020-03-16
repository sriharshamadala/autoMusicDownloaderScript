#!/usr/bin/env python

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# For calling instantMusic
from subprocess import call, check_call
from subprocess import Popen

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def open_downloaded_songs_list(filename):
    """
    Returns the file object of the downloaded songs list.
    If file doesn't exist, creates one.
    """
    open(filename, "a").close()
    fp = open(filename, "r")
    return fp

def call_instant_music(song, destDir):
    """
    Makes a system call to instantmusic to download the given song.
    """
    print(50*"=")
    print("Trying to download {}".format(song))
    print(50*"=")
    try:
        retVal = call(["instantmusic", "-p", "-s", "{}".format(song)], cwd="./"+destDir)
    except ValueError:
        print("Invalid choice.") 
    return retVal

def main():
    service = build('sheets', 'v4', credentials=get_credentials())
    
    # Insert your spread sheet ID and the desired data range.
    spreadsheetId = '<sheed_id_here>'
    rangeName = 'Sheet1!A:N'

    result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        header = values[0]
        for colIndex in range(9):
            # Create a separate directory for each category
            destDir = "{}".format(header[colIndex])
            filename = "Downloaded Songs List.txt"
            try:
                check_call(["mkdir", destDir])
            except:
                print("Directory already exists.")

            for row in values[1:]:
                if (len(row) >= colIndex+1):
                    song = row[colIndex].strip()
                    if song:
                        fp = open_downloaded_songs_list(destDir+"/"+filename)
                        downloadedSongs = fp.readlines()
                        fp.close()
                        songExists = False
                        for dlSong in downloadedSongs:
                            dlSong = dlSong.strip()
                            # TODO: Need fuzzy search here.
                            if (dlSong.find(song) == 0):
                                songExists = True
                                break
                        if not songExists:
                            retVal = call_instant_music(song, destDir)
                            if (retVal==0):
                                try:
                                    fp = open(destDir+"/"+filename, "a")
                                except:
                                    print("Unable to open "+destDir+"/"+filename)
                                    return
                                fp.write(song)
                                fp.close()
                        else:
                            print("Skipping. The song already exists locally.")


if __name__ == '__main__':
    main()

