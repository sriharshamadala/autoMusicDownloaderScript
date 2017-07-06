# AutoMusicDownloaderScript
My friends and I maintain a collaborative playlist on google sheets. It seems like a strange choice given there are plenty of other feature-rich options like Youtube or Spotify, but we wanted a one-stop, rarely-changing platform to store this information. Spotify does not have music in genres like Classical Telugu songs and in Youtube, videos get taken down. This also gives each of us the freedom to choose our music source.

In this project we write a simple script using the google sheets API and [instantmusic](https://github.com/yask123/Instant-Music-Downloader) to download the songs from our playlist. Please read the legal section before proceeding.

## Requirements
Python 3 or Python 2 (needs minor modifications in the script provided) and Pip.

Linux or Windows (portability of the script is not verified, minor modifications may be needed)

## Install InstantMusic
Use pip or pip3 to install InstantMusic depending on your choice of python versions.
```bash
$ sudo pip install instantmusic
$ sudo pip3 install instantmusic
```
For more details [read these instructions](https://github.com/yask123/Instant-Music-Downloader).

## Google Sheets API
Follow [these instructions](https://developers.google.com/sheets/api/quickstart/python) to create a basic python script to get your data from the google sheets. **Make sure you modify the "spreadsheetId" and the "rangeName" parameters.**

For my application each column is a separate genre. Main features of this script are:
* Download the songs corresponding to a genre into a separate directory.
* Maintain a list of downloaded songs so that any incremental changes in the playlist only prompt us to download the new songs.

## Remarks
* Sometimes the download fails when using InstantMusic. [This is because youtube-dl needs to be updated frequently](http://askubuntu.com/questions/598200/youdtube-dl-failed-to-extract-signature).
* If you do not want the download prompts and let the script run until it downloads all the songs in your playlist, simply call instantmusic with "-p" flag.

## Legality
From a [basic search](http://www.pcadvisor.co.uk/how-to/internet/is-it-legal-download-youtube-videos-3420353/), it is clear that downloading youtube videos (which is where instantmusic is extracting the music from) is illegal. Hence use it at your own risk.
