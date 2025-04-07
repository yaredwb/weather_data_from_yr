import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
import time
import sys

# File path
file_path = 'temperature_vs_depth_results_oygard_model_concrete_cahnnel_1995-2025.csv'

print("Starting frost penetration analysis...")

# Create output directory for plots if it doesn't exist
output_dir = 'frost_analysis'
os.makedirs(output_dir, exist_ok=True)

start_time = time.time()

# Try different encodings until one works
print("Reading CSV file...")
encodings = ['latin1', 'cp1252', 'utf-8-sig', 'iso-8859-1']
df = None

for encoding in encodings:
    try:
        print(f"Trying {encoding} encoding...")
        # Read the entire file without filtering columns
        # Note: Using a different approach to read the file
        df = pd.read_csv(file_path, sep=';', encoding=encoding)
        print(f"Successfully read file with {encoding} encoding")
        print(f"File has {len(df.columns)} columns")
        break
    except Exception as e:
        print(f"Error with {encoding} encoding: {str(e)}")

# If all encodings failed
if df is None:
    raise ValueError("Could not read the file with any of the attempted encodings")

# Print the first few column names to help debugging
print("First 5 column names:", df.columns[:5].tolist())
print("First 5 rows of the first column:")
print(df.iloc[:5, 0])

# Rename distance column if needed
# Try to automatically detect distance column by checking first column
first_col = df.columns[0]
if first_col == '' or 'Unnamed' in first_col or 'distance' in first_col.lower():
    print(f"Renaming first column '{first_col}' to 'Distance (m)'")
    df = df.rename(columns={first_col: 'Distance (m)'})
else:
    print(f"First column name is '{first_col}', assuming this is the distance column")
    df = df.rename(columns={first_col: 'Distance (m)'})

# Get distance and temperature columns
distance_col = 'Distance (m)'
temp_columns = df.columns[1:].tolist()

# Convert data to numeric with better error handling
print("Converting data to numeric format...")
df = df.replace('', np.nan).replace(',', '.', regex=True)  # Replace commas with dots globally

# Convert distance column
try:
    df[distance_col] = pd.to_numeric(df[distance_col], errors='coerce')
    print(f"Distance column conversion complete. NaN count: {df[distance_col].isna().sum()}/{len(df)}")
    print(f"Distance sample values: {df[distance_col].dropna().head(3).tolist()}")
except Exception as e:
    print(f"Error converting distance column: {str(e)}")

# Convert temperature columns
for col in temp_columns[:10]:  # Process first 10 columns to save time
    try:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    except Exception as e:
        print(f"Error with column {col}: {str(e)}")

# Check for NaN values and drop if necessary
if df[distance_col].isna().all():
    print("WARNING: All distance values are NaN. Check the file format!")
else:
    # Drop rows with NaN in distance column
    orig_len = len(df)
    df = df.dropna(subset=[distance_col])
    print(f"Dropped {orig_len - len(df)} rows with NaN distance values")

print(f"Distance range: {df[distance_col].min():.2f}m to {df[distance_col].max():.2f}m")
print(f"Processing {len(temp_columns)} time points")

# Continue with the rest of the analysis...
# Display data summary
print("\nData Summary:")
print(f"Total time points: {len(temp_columns)}")
print(f"Total depth points: {len(df)}")
print(f"First few temperature values for first time point: {df[temp_columns[0]].dropna().head(3).tolist()}")
# Rename distance column if needed
if '' in df.columns:
    df = df.rename(columns={'': 'Distance (m)'})
elif 'Unnamed: 0' in df.columns:
    df = df.rename(columns={'Unnamed: 0': 'Distance (m)'})

# Get distance and temperature columns
distance_col = df.columns[0]
temp_columns = df.columns[1:].tolist()

# Convert data to numeric
df = df.replace('', np.nan)
df[distance_col] = pd.to_numeric(df[distance_col], errors='coerce')
for col in temp_columns:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

print(f"Distance range: {df[distance_col].min():.2f}m to {df[distance_col].max():.2f}m")
print(f"Processing {len(temp_columns)} time points")

# Extract days/years as numeric values
days = []
for col in temp_columns:
    try:
        col_str = str(col).strip()
        if 'days' in col_str:
            days.append(float(col_str.split('days')[0].strip()))
        elif 'yrs' in col_str:
            years = float(col_str.split('yrs')[0].strip().replace(',', '.'))
            days.append(years * 365)
        else:
            days.append(float(col_str))
    except:
        days.append(len(days) + 1)

# Calculate frost penetration depth for each time point
print("Calculating frost penetration depths...")
frost_depths = []
frost_dates = []

# Convert days to actual dates (assuming simulation starts on Jan 1, 1995)
from datetime import datetime, timedelta
start_date = datetime(1995, 1, 1)
dates = [start_date + timedelta(days=int(d)) for d in days]

for i, col in enumerate(temp_columns):
    column_temps = df[col].values
    column_depths = df[distance_col].values
    
    # Find where temperature crosses 0°C
    has_frost = np.any(column_temps <= 0)
    
    if has_frost:
        # Find the deepest point where temp is at or below 0°C
        # Interpolate to get more precise depth
        for d_idx in range(len(column_depths)-1):
            if column_temps[d_idx] <= 0 and column_temps[d_idx+1] > 0:
                # Linear interpolation to find zero-crossing
                depth_range = column_depths[d_idx+1] - column_depths[d_idx]
                temp_range = column_temps[d_idx+1] - column_temps[d_idx]
                zero_depth = column_depths[d_idx] + (0 - column_temps[d_idx]) * depth_range / temp_range
                frost_depths.append(zero_depth)
                frost_dates.append(dates[i])
                break
        else:
            # If the loop completes without finding a crossing or the deepest point is below 0
            if column_temps[-1] <= 0:
                frost_depths.append(column_depths[-1])  # Maximum depth in our data
                frost_dates.append(dates[i])

# Convert to numpy arrays for easier manipulation
frost_depths = np.array(frost_depths)
frost_dates = np.array(frost_dates)

if len(frost_depths) > 0:
    # Create a publication-quality frost penetration depth plot
    print("Generating frost penetration plot...")
    plt.figure(figsize=(12, 8))
    
    # Create colormap based on seasons
    months = np.array([d.month for d in frost_dates])
    
    # Define colors for seasons: winter (blue), spring (green), summer (yellow), fall (orange)
    season_colors = plt.cm.viridis(np.linspace(0, 1, 12))
    
    # Plot frost depth over time with seasonal coloring
    sc = plt.scatter(frost_dates, frost_depths, c=months, cmap='viridis', 
                    alpha=0.7, s=30, edgecolor='none')
    
    # Add trend line
    from scipy.signal import savgol_filter
    if len(frost_depths) > 10:
        try:
            smooth_depths = savgol_filter(frost_depths, min(21, len(frost_depths) // 3 * 2 + 1), 3)
            plt.plot(frost_dates, smooth_depths, color='#FF5733', lw=2, alpha=0.8)
        except:
            pass
    
    # Styling
    plt.gca().invert_yaxis()  # Invert y-axis to show depth going down
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.title('Frost Penetration Depth over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Depth (m)', fontsize=14)
    
    # Add colorbar for months
    cbar = plt.colorbar(sc, label='Month of Year')
    cbar.set_ticks([1, 3, 6, 9, 12])
    cbar.set_ticklabels(['Jan', 'Mar', 'Jun', 'Sep', 'Dec'])
    
    # Add statistics annotation
    max_frost = frost_depths.max()
    avg_frost = frost_depths.mean()
    textstr = f"Maximum frost depth: {max_frost:.2f} m\nAverage frost depth: {avg_frost:.2f} m"
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.annotate(textstr, xy=(0.03, 0.05), xycoords='axes fraction', fontsize=12,
                verticalalignment='bottom', bbox=props)
    
    # Format the plot for publication
    plt.tight_layout()
    
    # Save high-resolution plot
    frost_plot_path = os.path.join(output_dir, 'frost_penetration_depth.png')
    plt.savefig(frost_plot_path, dpi=300, bbox_inches='tight')
    print(f"Frost penetration plot saved to {frost_plot_path}")
    
    # Generate additional plot with yearly patterns
    plt.figure(figsize=(12, 8))
    
    # Extract year and day of year for seasonal pattern visualization
    years = np.array([d.year for d in frost_dates])
    days_of_year = np.array([d.timetuple().tm_yday for d in frost_dates])
    
    unique_years = np.unique(years)
    cmap = plt.get_cmap('viridis', len(unique_years))
    
    # Plot frost depth by day of year, colored by year
    for i, year in enumerate(sorted(unique_years)):
        mask = years == year
        plt.scatter(days_of_year[mask], frost_depths[mask], color=cmap(i), 
           label=str(year), alpha=0.7, s=30, edgecolor='none')
    
    # Styling
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.title('Seasonal Frost Penetration Patterns by Year', fontsize=16, fontweight='bold')
    plt.xlabel('Day of Year', fontsize=14)
    plt.ylabel('Depth (m)', fontsize=14)
    
    # Add month indicators on x-axis
    month_starts = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    plt.xticks(month_starts, month_names)
    
    # Add legend for years
    plt.legend(title='Year', loc='best', framealpha=0.7)
    
    plt.tight_layout()
    seasonal_plot_path = os.path.join(output_dir, 'seasonal_frost_patterns.png')
    plt.savefig(seasonal_plot_path, dpi=300, bbox_inches='tight')
    print(f"Seasonal frost pattern plot saved to {seasonal_plot_path}")
    
    # Calculate and print frost statistics
    print("\nFrost Penetration Statistics:")
    print(f"Maximum frost depth: {max_frost:.2f} m")
    print(f"Average frost depth: {avg_frost:.2f} m")
    print(f"Number of days with frost penetration: {len(frost_depths)}")
    
    if len(unique_years) > 1:
        print("\nYearly Maximum Frost Depths:")
        for year in sorted(unique_years):
            year_mask = years == year
            if np.any(year_mask):
                year_max = frost_depths[year_mask].max()
                print(f"  {year}: {year_max:.2f} m")
else:
    print("No frost penetration detected in the data.")

end_time = time.time()
print(f"Analysis completed in {end_time - start_time:.2f} seconds")
