import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry













def single_classification(single_path):
    
    """
    This function take a single path of a photo, then do reshape to fit the models, and do classification
    Input is a path of a certain photo
    Output is a tuple which contains subtype(for being send to a correct sub-model), 
                                     info(a string having all info of a clothes), 
                                     res(a list having all info of a clothes)
    """
    
    # Our model only applies to dataframes. 
    # Therefore, in order to enable the model to predict a single picture, 
    # we turn this picture into a dataframe with only one row.
    train_images = np.zeros((1,80,60,3))
  
    path = single_path#/content/images   
    img = cv2.imread(path)
    
    #reshape img to apply the model
    if img.shape != (80,60,3):
        img = image.load_img(path, target_size=(80,60,3))

    train_images[0] = img

    
    result2 = sub_list[np.argmax(sub_model.predict(train_images))]
    
    # According to the results of the first model, branch to three other models
    if result2=="top":
        res = single_helper(train_images,top_model,top_list)
    elif result2=="bottom":
        res = single_helper(train_images,bottom_model,bottom_list)
    elif result2=="foot":
        res = single_helper(train_images,foot_model,foot_list)
    res.append(single_path)
    res_str = f"{res[0]}, {res[1]}, {color_classification(single_path)}, {res[3]}, {res[4]}, {single_path}" 
    
    return (result2,res_str,res)




def find_combo_by_top(top_color_group, combotype):
    """
    This function recommend color base on a seed color by a given angle in a colorwheel.
    Input is a color (from 12+3 colorwheel) and a angle: moderate_combo == 90
                                                         similar_combo == 60
                                                         close_combo == 30
                                                         same_combo == 0
    output is a list of two color
    """
    
    co = int(combotype/30)
    
    
    #if top color is multi
    if top_color_group == 15: #if top color is multi
        bottom_color_group = random.choice([12,13,14])
        if bottom_color_group==12: #if bottom color is black
            shoes_color_group = 13 #then set shoes to be white
            
        elif bottom_color_group==13:                      #if bottom color is white
            shoes_color_group = random.choice([12,13,14]) #then set shoes to be black or white or grey
            
        else:                      #if bottom color is grey
            shoes_color_group = random.choice([12,13])    #then set shoes to be black or white
    
    
    #if top color is mono
    elif top_color_group == 12 or top_color_group == 13 or top_color_group == 14:
        if top_color_group == 12:
            bottom_color_group = random.choice([12,13])
            if bottom_color_group==12:
                shoes_color_group = 13
            else:
                shoes_color_group=random.choice([12,13])
        elif top_color_group == 13:
            bottom_color_group = random.choice([12,13])
            if bottom_color_group==12:
                shoes_color_group = 13
            else:
                shoes_color_group=12
        else:
            bottom_color_group=random.choice([12,13])
            shoes_color_group=random.choice([12,13])  
    else: 
        bottom_color_group = random.choice([top_color_group-co, top_color_group+co])
        if bottom_color_group==top_color_group-co:
            shoes_color_group = top_color_group+co
        else:
            shoes_color_group = top_color_group-co
            
        #In fact, we can simplify this part of the code
        if bottom_color_group == 12:
            bottom_color_group = 0
        if bottom_color_group == 13:
            bottom_color_group = 1
        if bottom_color_group == 14:
            bottom_color_group = 2 
        if bottom_color_group == 15:
            bottom_color_group = 3
        if bottom_color_group == 16:
            bottom_color_group = 4
        if bottom_color_group == 17:
            bottom_color_group = 5
            
        if shoes_color_group == 12:
            shoes_color_group = 0
        if shoes_color_group == 13:
            shoes_color_group = 1
        if shoes_color_group == 14:
            shoes_color_group = 2
        if shoes_color_group == 15:
            shoes_color_group = 3
        if shoes_color_group == 16:
            shoes_color_group = 4
        if shoes_color_group == 17:
            shoes_color_group = 5
        
        if bottom_color_group == -1:
            bottom_color_group = 11
        if bottom_color_group == -2:
            bottom_color_group = 10
        if bottom_color_group == -3:
            bottom_color_group = 9 
        if bottom_color_group == -4:
            bottom_color_group = 8
        if bottom_color_group == -5:
            bottom_color_group = 7
        if bottom_color_group == -6:
            bottom_color_group = 6
            
        if shoes_color_group == -1:
            shoes_color_group = 11
        if shoes_color_group == -2:
            shoes_color_group = 10
        if shoes_color_group == -3:
            shoes_color_group = 9
        if shoes_color_group == -4:
            shoes_color_group = 8
        if shoes_color_group == -5:
            shoes_color_group = 7
        if shoes_color_group == -6:
            shoes_color_group = 6
            
    return (bottom_color_group , shoes_color_group)




# Since one of the factors in our clothes recommendation is the season,
# we extract the current real season and match it with all the clothes stored in the app.
# This means that we only recommend clothes that are suitable for the current season
'''from datetime import date
todays_date = date.today()
tomonth = todays_date.month
if tomonth in [3,4,5]:
    toseason = "Spring"
elif tomonth in [6,7,8]:
    toseason = "Summer"
elif tomonth in [9,10,11]:
    toseason = "Fall"
else:
    toseason = "Winter"'''
 

 
# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)
 
# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 42.3001,
    "longitude": -83.0165,
    "current": ["temperature_2m", "rain", "weather_code"],
    "hourly": ["temperature_2m", "relative_humidity_2m", "rain", "showers", "weather_code", "temperature_120m"],
    "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
    "forecast_days": 10,
    "models": "gem_seamless"
}
responses = openmeteo.weather_api(url, params=params)
 
# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
 
# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_rain = current.Variables(1).Value()
current_weather_code = current.Variables(2).Value()
 
print(f"Current time {current.Time()}")
print(f"Current temperature_2m {current_temperature_2m}")
print(f"Current rain {current_rain}")
print(f"Current weather_code {current_weather_code}")
 
# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_rain = hourly.Variables(2).ValuesAsNumpy()
hourly_showers = hourly.Variables(3).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(4).ValuesAsNumpy()
hourly_temperature_120m = hourly.Variables(5).ValuesAsNumpy()
 
hourly_data = {"date": pd.date_range(
    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
    freq=pd.Timedelta(seconds=hourly.Interval()),
    inclusive="left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["rain"] = hourly_rain
hourly_data["showers"] = hourly_showers
hourly_data["weather_code"] = hourly_weather_code
hourly_data["temperature_120m"] = hourly_temperature_120m
 
print("---------Hourly---------")
hourly_dataframe = pd.DataFrame(data=hourly_data)
pd.set_option('display.max_rows', None)
print(hourly_dataframe)
print("-------------------------")
 
# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
 
daily_data = {"date": pd.date_range(
    start=pd.to_datetime(daily.Time(), unit="s", utc=True),
    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
    freq=pd.Timedelta(seconds=daily.Interval()),
    inclusive="left"
)}
daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
 
daily_dataframe = pd.DataFrame(data=daily_data)
pd.set_option('display.max_rows', None)
print(daily_dataframe)
 
# Function to interpret weather codes
def interpret_weather_code(weather_code):
    if weather_code == 0:
        return "Clear sky"
    elif weather_code in [1, 2, 3]:
        return "Partly cloudy"
    elif weather_code in [45, 48]:
        return "Foggy"
    elif weather_code in [51, 53, 55]:
        return "Drizzle"
    elif weather_code in [56, 57]:
        return "Freezing drizzle"
    elif weather_code in [61, 63, 65]:
        return "Rainy"
    elif weather_code in [66, 67]:
        return "Freezing rain"
    elif weather_code in [71, 73, 75]:
        return "Snowfall"
    elif weather_code == 77:
        return "Snow grains"
    elif weather_code in [80, 81, 82]:
        return "Rain showers"
    elif weather_code in [85, 86]:
        return "Snow showers"
    elif weather_code == 95:
        return "Thunderstorm"
    elif weather_code in [96, 99]:
        return "Thunderstorm with hail"
    else:
        return "Unknown weather"
 
# Function to determine the season based on temperature and weather conditions
def determine_season(max_temp, weather_condition):
    if weather_condition == "Drizzle" and max_temp >= 25:
        return "Summer"
    elif weather_condition in ["Rainy", "Thunderstorm", "Rain showers"]:
        return "Fall"
    elif weather_condition == "Drizzle" and max_temp < 10:
        return "Winter"
    elif max_temp >= 25:
        return "Summer"
    elif 15 <= max_temp < 25:
        return "Spring"
    elif 5 <= max_temp < 15:
        return "Fall"
    else:
        return "Winter"
 
# Determine weather conditions for the next 10 days
for i in range(10):
    date = daily_dataframe['date'][i].strftime('%Y-%m-%d')
    max_temp = daily_temperature_2m_max[i]
    min_temp = daily_temperature_2m_min[i]
    weather_code = daily_weather_code[i]
    
    weather_condition = interpret_weather_code(weather_code)
    
    # Determine if it's cold
    if max_temp < 10:
        temp_condition = "Cold"
    elif max_temp >= 10 and max_temp < 20:
        temp_condition = "Cool"
    elif max_temp >= 20 and max_temp < 30:
        temp_condition = "Warm"
    else:
        temp_condition = "Hot"
    
    # Determine the season
    toseason = determine_season(max_temp, weather_condition)
    
    #`  print(f"{date}: {weather_condition}, Temperature: {temp_condition} (Max: {max_temp}°C, Min: {min_temp}°C), Season: {season}")