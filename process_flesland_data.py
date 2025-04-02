import pandas as pd
import csv
import os

# Define input and output file paths
input_file = "G:/My Drive/GitHub Repos/weather_data_from_yr/Flesland_middeltemperatur_døgn_fra_1995.csv"
output_file = "G:/My Drive/GitHub Repos/weather_data_from_yr/flesland_daily_average_temperature_from_1995.csv"

# Read the input file and write to the output file
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    # Create CSV readers and writers
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')
    
    # Skip the header row in the input file
    next(reader)
    
    # Write the header row to the output file
    writer.writerow(['date', 'temperature'])
    
    # Process each row of data
    day_count = 1
    for row in reader:
        # Skip empty rows or rows that appear to be comments or metadata
        if not row or (len(row) > 0 and (row[0].strip().startswith('//') or 'Data er gyldig' in row[0])):
            continue
        
        if len(row) >= 4:  # Ensure we have enough columns
            temperature = row[3]  # Get the temperature value (already with comma as decimal)
            
            # Write the new row to the output file
            writer.writerow([day_count, temperature])
            day_count += 1

print(f"Processing complete. Created {output_file} with {day_count-1} days of temperature data.")