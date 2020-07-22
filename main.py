import pandas as pd
import requests
#import piexif - Do not need PIEXIF
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account
from googlemaps import client
import googlemaps
import gmplot
import os
import io
import json
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
# PIL = Python Image Library
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

#Main function, does not need to be modified anymore!
#Creates disasters.csv file
#Pulls exif/GPS data from pictures.
FOLDER = '/Documents/Uploads' #Ideally will allow us to identify which folder uploads go to.
N_ADDRESS = 4
# Initialize CSV
initial_columns = ['GPSLongitude', 'GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'DateTimeOriginal', 'PhotoName']
new_columns = ['GPSLongitude', 'GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef']
disasters = pd.DataFrame(columns = initial_columns) # Create dataframe
disasters2 = disasters.to_csv('disasters.csv', mode = 'a', header = True, index = False) # Save dataframe to disasters.csv

# Function to get exif data. Takes in user_input from CMD / server.py
def get_exif_data(user_input):

    exif = Image.open(user_input)._getexif() # Opening file and get exif information

    # Error handling if exif data exists
    if exif is not None:
        for key, value in exif.items():
            name = TAGS.get(key, key)
            exif[name] = exif.pop(key)
    else:
        return print("No GPS/Location Data Exists!")

    # Iphone
    if 'GPSInfo' in exif: #Exif/GPS data is lost when an image is uploaded to Slack, we NEED RAW data.
        for key in exif['GPSInfo'].keys():
            name = GPSTAGS.get(key, key) #GPSTAGS from PIL
            exif['GPSInfo'][name] = exif['GPSInfo'].pop(key)
        exif_df = pd.DataFrame.from_dict(exif['GPSInfo'], orient='index') # Save to DataFrame from Dictionary
        exif_df = exif_df.T[new_columns]
        exif_datetime = pd.DataFrame.from_dict(exif, orient='index') # Isolate DateTimeOriginal from original exif dictionary
        exif_df['DateTimeOriginal'] = exif_datetime.T['DateTimeOriginal'] # Add new column to exif_df with DateTimeOriginal
        exif_df["PhotoName"] = user_input[7:]
        exif_df # Important?
        disasters.append(exif_df) # Adding exif_df to Disasters scaffolding DataFrame
        return exif_df.to_csv('disasters.csv', mode='a', header=False, index=False) # Save to disasters.csv

    # Android
    if 34853 in exif: #Exif data from Android phones
        for key in exif[34853].keys():
            name = GPSTAGS.get(key, key)
            exif[34853][name] = exif[34853].pop(key)

        exif_df_android = pd.DataFrame.from_dict(exif[34853], orient='index')
        exif_df_android = exif_df_android.T[new_columns]
        exif_df_android['DateTimeOriginal'] = exif['DateTimeOriginal']
        exif_df_android["PhotoName"] = user_input[7:]
        exif_df_android
        disasters.append(exif_df_android)
        return exif_df_android.to_csv('disasters.csv', mode='a', header=False, index=False)

#Modifies GPS Lat/Long to minutes/seconds and returns one long string of coordinates.
#These coordinates are passed into GoogleMapPlotter to produce an HTML page with an exact
#Google Map!

def map_search(x):
    zoom = 12 # Google maps api feature. Indicates the radius of our view distance in miles. Modifialbe
    exif_df = pd.read_csv('disasters.csv') # Load in disasters.csv
    x = x[7:] # Removing 'Assets/' from user_input (Assets/trial.jpg)
    y = exif_df[exif_df['PhotoName'] == x].index.tolist()[0] # Returns index value for photo names in exif_df.

    # String manipulation to pull latitude numbers to proper format for Google Maps API
    lat_deg = int(exif_df["GPSLatitude"][y].replace("(",",").replace(")","").split(",")[2])
    lat_min = int(exif_df["GPSLatitude"][y].replace("(",",").replace(")","").split(",")[5])
    lat_sec = int(exif_df["GPSLatitude"][y].replace("(",",").replace(")","").split(",")[8])/100
    if exif_df["GPSLatitudeRef"][y] == "S":
        lat_numbers = str(round(float(-1*(lat_deg + (lat_min/60) + (lat_sec/3600))),7))
    else:
        lat_numbers = str(round(float(lat_deg + (lat_min/60) + (lat_sec/3600)),7))

    # String manipulation to pull longitude numbers to proper format for Google Maps API
    long_deg = int(exif_df["GPSLongitude"][y].replace("(",",").replace(")","").split(",")[2])
    long_min = int(exif_df["GPSLongitude"][y].replace("(",",").replace(")","").split(",")[5])
    long_sec = int(exif_df["GPSLongitude"][y].replace("(",",").replace(")","").split(",")[8])/100
    if exif_df["GPSLongitudeRef"][y] == "W":
        long_numbers = str(round(float(-1*(long_deg + (long_min/60) + (long_sec/3600))),7))
    else:
        long_numbers = str(round(float(long_deg + (long_min/60) + (long_sec/3600)),7))

    # Google Maps API code. Generates .HTML file with google maps location with 'zoom' view.
    gmap=gmplot.GoogleMapPlotter(lat_numbers, long_numbers, zoom)
    gmap.apikey = '#Insert Google Streetview/Google Maps API key'
    gmap.draw("../PyDisaster/PyDisaster.html" )
    return print ("Check the map!")

# For inputs / flask app
if __name__ == '__main__':
    print('you did it!')
