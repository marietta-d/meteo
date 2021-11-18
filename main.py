import mysql.connector # before we have to pip install mysql-connector-python at terminal
import matplotlib.pyplot as plt
import numpy as np
from decimal import *
from windrose import WindroseAxes

my_db = mysql.connector.connect(
    host="localhost",
    user="marietta",
    password="pythonis@BIGsnAK3",
    database="meteo"
    )
my_cursor = my_db.cursor()
command = """select open_weather_data.temperature, 
	geo_coordinate.latitude, 
	geo_coordinate.longitude,
	open_weather_data.wind_speed, 
	open_weather_data.wind_deg, 
	open_weather_data.interval_utc_timestamp as time
		from open_weather_data 
		inner join geo_coordinate on open_weather_data.geo_coordinate_id = geo_coordinate.id
		where geo_coordinate_id = 74
		order by interval_utc_timestamp DESC;"""
my_cursor.execute(command)

w_cache = np.empty(shape=(0,))
d_cache = np.empty(shape=(0,))

for x in my_cursor.fetchall():
    w_curr = float(x[3]) * 3.6
    d_curr = float(x[4])
    w_cache = np.concatenate((w_cache, [w_curr]))
    d_cache = np.concatenate((d_cache, [d_curr]))

plt.scatter(d_cache, w_cache)
plt.xlabel("Direction (deg)")
plt.ylabel("Wind speed (km/h)")
plt.show()

plt.hist(w_cache, bins=20)
plt.show()

ax = WindroseAxes.from_ax()
ax.bar(d_cache, w_cache, normed=True)
ax.set_legend()
plt.show()

