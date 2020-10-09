import pandas as pd
import numpy as np
import json
import streamlit as st
import requests
################################Preprocessing Data#######################################
f = open('Preprocessing_.json',)
data = json.load(f)
dest_dict=data['dest_dict']
tailnum_dict=data['tailnum_dict']
mode_dict=data['mode_dict']
carrier = ['AA', 'AS', 'B6', 'DL', 'EV', 'F9', 'FL', 'HA', 'MQ', 'OO', 'UA', 'US', 'VX', 'WN', 'YV']
origin = ['JFK', 'LGA']
f_type=['Fixed wing multi engine','Fixed wing single engine','Rotorcraft']
engine = ['Reciprocating', 'Turbo-fan', 'Turbo-jet', 'Turbo-prop', 'Turbo-shaft']
manufacturer = ['BOEING', 'EMBRAER', 'AIRBUS', 'AIRBUS INDUSTRIE', 'BOMBARDIER INC',
                'MCDONNELL DOUGLAS AIRCRAFT CO', 'MCDONNELL DOUGLAS', 'CANADAIR',
                'MCDONNELL DOUGLAS CORPORATION', 'CESSNA', 'GULFSTREAM AEROSPACE',
                'CIRRUS DESIGN CORP', 'ROBINSON HELICOPTER CO', 'PIPER']

def One_Hot_Encoding(text="EWR",list1=[]):
    demo=[]
    # print(text,type(text))
    for i in list1:
        if i==text:
            demo.append(1)
        else:
            demo.append(0)
    return demo
def Mean_Encoding(text,dict1):
    # print("Mean_Encoding",text)
    return dict1[text]
def Get_Weather(lat,lon):
    if lat!=None and lon!=None:
        d=requests.get("https://weather.api.here.com/weather/1.0/report.json?product=observation&latitude="+str(lat)+"&longitude="+str(lon)+
                       "&oneobservation=true&app_id=devportal-demo-20180625&app_code=9v2BkviRwi9Ot26kp2IysQ")
        # st.write(d.json())
        data=d.json()
        key=['temperature','dewPoint','humidity','windDirection','windSpeed','precipitation24H','barometerPressure','visibility']
        info={}
        for i in key:
            if data["observations"]["location"][0]["observation"][0][i]!="*":
                info[i]=float(data["observations"]["location"][0]["observation"][0][i])
            else:
                info[i] =0.0
        return  info
    else:
        return {"Invalid input":[lat,lon]}
def Preprocessing_df(data,Source_location,Dest_loc_info):
    print("Preprocessing")
    Source_Weather=Get_Weather(Source_location["lat"],Source_location["lon"])

    main_dict={
        "month":"",
        "day":"",

        'flight':"",
        'tailnum':"",

        'dest':"",
        'air_time':"",
        'distance':"",
        'hour':"",
        'minute':"",

        'lat_x':"",
        'lon_x':"",
        'alt_x':"",

        'lat_y':"",
        'lon_y':"",
        'alt_y':"",

        'year_y':"",

        'model':"",
        'engines':'',
        'seats':'',

        'temp':'',
        'dewp':'',
        'humid':'',
        'wind_dir':'',
        'wind_speed':'',
        'precip':'',
        'pressure':'',
        'visib':'',

        'AA':'',
        'AS':'',
        'B6':'',
        'DL':'',
        'EV':'',
        'F9':'',
        'FL':'',
        'HA':'',
        'MQ':'',
        'OO':'',
        'UA':'',
        'US':'',
        'VX':'',
        'WN':'',
        'YV':'',

        'JFK':'',
        'LGA':'',

        'Fixed wing single engine':'',
        'Rotorcraft':'',

        'Reciprocating':'',
        'Turbo-fan':'',
        'Turbo-jet':'',
        'Turbo-prop':'',
        'Turbo-shaft':'',

        'BOEING':'',
        'EMBRAER':'',
        'AIRBUS':'',
        'AIRBUS INDUSTRIE':'',
        'BOMBARDIER INC':'',
        'MCDONNELL DOUGLAS AIRCRAFT CO':'',
        'MCDONNELL DOUGLAS':'',
        'CANADAIR':'',
        'MCDONNELL DOUGLAS CORPORATION':'',
        'CESSNA':'',
        'GULFSTREAM AEROSPACE':'',
        'CIRRUS DESIGN CORP':'',
        'ROBINSON HELICOPTER CO':'',
        'PIPER':''
    }
    data=data.to_dict(orient='records')[0]

    for key in main_dict.keys():
        # print(key)
        if key=="dest":
            main_dict[key]= Mean_Encoding(data[key], dest_dict)
        elif key=="model":
            main_dict[key]= Mean_Encoding(data[key], mode_dict)
        elif key == "tailnum":
            main_dict[key] = Mean_Encoding(data[key], tailnum_dict)
        elif key=="temp":
            main_dict[key] = Source_Weather["temperature"] #['temperature','dewPoint','humidity','windDirection','precipitation24H','barometerPressure','visibility']
        elif key=="dewp":
            main_dict[key] = Source_Weather["dewPoint"]
        elif key=="humid":
            main_dict[key] = Source_Weather["humidity"]
        elif key=="wind_dir":
            main_dict[key] = Source_Weather["windDirection"]
        elif key == "wind_speed":
            main_dict[key] = Source_Weather["windSpeed"]
        elif key=="precip":
            main_dict[key] = Source_Weather["precipitation24H"]
        elif key == "pressure":
            main_dict[key] = Source_Weather["barometerPressure"]
        elif key == "visib":
            main_dict[key] = Source_Weather["visibility"]
        elif key=="lat_x":
            main_dict[key]=Source_location["lat"]
        elif key=="lon_x":
            main_dict[key]=Source_location["lon"]
        elif key=="alt_x":
            main_dict[key]=Source_location["alt"]
        elif key=="lat_y":
            main_dict[key]=Dest_loc_info["lat"]
        elif key=="lon_y":
            main_dict[key]=Dest_loc_info["lon"]
        elif key=="alt_y":
            main_dict[key]=Dest_loc_info["alt"]
        elif(key in carrier):
            if key==data["carrier"]:
                main_dict[key] = 1
            else:
                main_dict[key] = 0
        elif (key in origin):
            if key == data["origin"]:
                main_dict[key] = 1
            else:
                main_dict[key] = 0
        elif (key in engine):
            if key == data["engine"]:
                main_dict[key] = 1
            else:
                main_dict[key] = 0
        elif (key in f_type):
            if key == data["type"]:
                main_dict[key] = 1
            else:
                main_dict[key] = 0
        elif (key in manufacturer):
            if key == data["manufacturer"]:
                main_dict[key] = 1
            else:
                main_dict[key] = 0
        else:
            if key in data.keys():
                main_dict[key]=data[key]
    # st.write(main_dict)
    return main_dict


