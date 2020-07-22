import getpass
import json
import os
import smtplib
import ssl
import urllib.request


from datetime import datetime, timedelta

import numpy as np
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates



#%%
#email = os.environ["EMAIL"] if "EMAIL" in os.environ else input("Email: ")
#password = os.environ["PASSWORD"] if "PASSWORD" in os.environ else getpass.getpass()

lat = 22.3193
long = 114.1694

with urllib.request.urlopen("https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=%f&lon=%f" %(lat, long)) as fp:
    forecast = json.load(fp)
    
    # Adjust for timezones
    now = datetime.now()
    day = now.strftime("%d/%m/%Y")
    servertime = datetime.strptime(forecast["properties"]["timeseries"][0]["time"],"%Y-%m-%dT%H:%M:%SZ")
    tzdelta = now - servertime

    # Select features
    precip_list = []
    dt_list = []
    cloud_list = []

    for i in range(24):
        precipitation = forecast["properties"]["timeseries"][i]["data"]["next_1_hours"]["details"]["precipitation_amount"]
        precip_list.append(precipitation)
        
        cloud = forecast["properties"]["timeseries"][i]["data"]["instant"]["details"]["cloud_area_fraction"]
        cloud_list.append(cloud)
        
        date = datetime.strptime(forecast["properties"]["timeseries"][i]["time"],"%Y-%m-%dT%H:%M:%SZ") + tzdelta
        dt_list.append(date)
#%%
        
    d = {'Time': dt_list, 'Precipitation': precip_list, 'Cloud_coverage': cloud_list}
    df = pd.DataFrame(d)
    df.index.name = 'Time'
    
    plt.style.use('ggplot')
    ax = df.plot(title = 'Precipitation and cloud cover in the next 24 hours', x='Time', secondary_y='Cloud_coverage', figsize=(9,6))
    ax.set_xlabel('Time')
    ax.set_ylabel('Precipitation (mm)')
    ax.right_ax.set_ylabel('Cloud coverage (%)')
    
#    ax.grid()
    plt.show()

    if precipitation > 0:
#        print(precipitation)
        msg = f"Subject: Don't forget your umbrella!\n\n{precipitation}mm of precipitation is forecast."
        context = ssl.create_default_context()
#        with smtplib.SMTP_SSL("smtp.gmail.com", context=context) as server:
#            server.login(email, password)
#            server.sendmail(email, email, msg)

        