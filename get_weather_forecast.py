import os
import csv
import requests
import pandas as pd
from matplotlib import rcParams
import xml.etree.ElementTree as et

class WeatherData:
  def __init__(self, url, xml_filename, csv_filename):
    '''
    Initializes object with url and necessary filenames
    '''
    self.url = url
    self.xml_filename = xml_filename
    self.csv_filename = csv_filename

  def requestDataFromYr(self):
    """
    Requests and saves weather forecast data from yr.no
    """
    global my_dir
    path = os.path.abspath(__file__)
    my_dir = os.path.dirname(path)

    # Grab latest forecast from yr.no and save xml file
    weather_data = requests.get(self.url, allow_redirects=True)
    file = open(os.path.join(my_dir, self.xml_filename), 'wb')
    file.write(weather_data.content)

  def parseXMLFileAndWriteToCSV(self):
    '''
    Parses the forecast xml file, extracts the dates and weather
    forecasts (precipitation and temperature) and writes the extracted
    data to a csv file
    '''
    # Read root XML data
    tree = et.parse(os.path.join(my_dir, self.xml_filename))
    root = tree.getroot()

    # Get forecast child
    forecast = root.find('forecast').find('tabular')

    # Check if the csv file exists - If not, create one in writing mode
    # If yes, initiate the csv writer in appending mode
    if not os.path.exists(os.path.join(my_dir, self.csv_filename)):
      f = open(os.path.join(my_dir, self.csv_filename), 'w', newline='')
      csvwriter = csv.writer(f)
      col_names = ['From', 'To', 'Min Precip. (mm)', 'Avg Precip. (mm)',
                   'Max Precip. (mm)', 'Temp. (C)']
      csvwriter.writerow(col_names)
    else:
      f = open(os.path.join(my_dir, self.csv_filename), 'a', newline='')
      csvwriter = csv.writer(f)

    # Extract data from the forecast child
    for element in forecast.findall('time'):
      data = []
      start_time = element.get('from')
      end_time   = element.get('to')
      prcp       = element.find('precipitation')
      min_prcp   = prcp.get('minvalue')
      avg_prcp   = prcp.get('value')
      max_prcp   = prcp.get('maxvalue')
      temp       = element.find('temperature').get('value')
      if min_prcp == None or max_prcp == None:
        min_prcp, max_prcp = 0, 0
      # Append data to create new row
      data.append(start_time)
      data.append(end_time)
      data.append(min_prcp)
      data.append(avg_prcp)
      data.append(max_prcp)
      data.append(temp)
      # Write a new row to csv file
      csvwriter.writerow(data)

    f.close()

    # Get forecast update time
    global update_time
    update_time = root.find('meta').find('lastupdate').text
    update_time = update_time.replace(':','.')
    upd_xml_filename = self.xml_filename[:-4] + '_' + update_time + '.xml'

    # Rename forecast xml file with update time, pass if forecast not updated
    try:
      os.rename(os.path.join(my_dir, self.xml_filename),
                os.path.join(my_dir, upd_xml_filename))
    except FileExistsError:
      pass

  def updateForecasts(self):
    '''
    Drops old yr forecast data and keeps the updated ones
    '''
    # Load csv file with duplicate data
    raw_data = pd.read_csv(os.path.join(my_dir, self.csv_filename))
    # Clean data by keeping only latest forecasts
    clean_data = raw_data.drop_duplicates(subset=['From', 'To'], keep='last')
    # Write clean data to new csv file
    clean_file = self.csv_filename[:-4] + '_Clean.csv'
    clean_data.to_csv(os.path.join(my_dir, clean_file), index=False)

  def plotWeatherData(self):
    '''
    Plots a histogram from the accumulated precipitation data, the precipitation
    versus time and the temperature vs time for the latest forecast
    '''
    # Load csv data for plotting
    data_file = self.csv_filename[:-4] + '_Clean.csv'
    data = pd.read_csv(os.path.join(my_dir, data_file))

    # Separate precipitation and temperature data
    prcp = data[['From', 'Min Precip. (mm)', 'Avg Precip. (mm)',
                 'Max Precip. (mm)']]
    temp = data[['From', 'Temp. (C)']]

    # Set chart parameters
    rcParams.update({'figure.autolayout': True})
    rcParams['font.family'] = 'Times New Roman'
    rcParams.update({'font.size': 11})

    # Plot histogram from precipitation data
    ax0 = prcp.plot.hist(bins=20)   # bins=10 by default
    ax0.legend(['Minimum', 'Average', 'Maximum'])
    ax0.set_xlabel('Hourly Precipitation [mm]')

    # Plot precipitation data for the latest 48 hour forecast
    prcp_latest = prcp.tail(48)
    ax1 = prcp_latest.plot.bar(x='From', figsize=(15,5))
    ax1.legend(['Minimum', 'Average', 'Maximum'])
    ax1.set_ylabel('Precipitation [mm]')
    ax1.axes.get_xaxis().get_label().set_visible(False)

    # Plot temperature data for the latest 48 hour forecast
    temp_latest = temp.tail(48)
    ax2 = temp_latest.plot.bar(x='From', figsize=(15,5))
    ax2.get_legend().remove()
    ax2.set_ylabel('Temperature [C]')
    ax2.axes.get_xaxis().get_label().set_visible(False)

    # Plot names
    fig1 = 'Histogram_' + update_time + '.png'
    fig2 = 'Latest_Prcp_Forecast_' + update_time + '.png'
    fig3 = 'Latest_Temp_Forecast_' + update_time + '.png'

    # Save updated plots
    ax0.get_figure().savefig(os.path.join(my_dir, fig1))
    ax1.get_figure().savefig(os.path.join(my_dir, fig2))
    ax2.get_figure().savefig(os.path.join(my_dir, fig3))

if __name__ == "__main__":
  url = 'https://www.yr.no/place/Norway/Tr%C3%B8ndelag/Stj%C3%B8rdal/Flornes/forecast_hour_by_hour.xml'
  xml_filename = 'Flornes_Hourly_Forecast.xml'
  csv_filename = 'Flornes_Hourly_Data.csv'
  go = WeatherData(url, xml_filename, csv_filename)
  go.requestDataFromYr()
  go.parseXMLFileAndWriteToCSV()
  go.updateForecasts()
  go.plotWeatherData()