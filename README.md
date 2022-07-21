# weather_data_from_yr
Get weather data for a specific location from yr.no using their API. A batch scipt may be added to run this script at a regular interval. The script will then download the data, process it to make changes and remove duplicates and save the data. A batch file to run the script would look like this:
```
python get_weather_forecast.py 
```
The url and the file names in the script should be changed to match the location and the data you want to download.
