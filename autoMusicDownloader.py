#!/usr/bin/env python

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# For calling instantMusic
from subprocess import call, check_call
from subprocess import Popen

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.
    
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
    return credentials

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
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
            'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                discoveryServiceUrl=discoveryUrl)
    
    # Insert your spread sheet ID and the desired data range.
    spreadsheetId = 
    rangeName = 'Sheet1!A:I'

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

