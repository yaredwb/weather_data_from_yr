import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
from scipy import signal

# Set style for publication-ready plot
# Use a valid style from matplotlib
plt.style.use('default')  # Start with default style
sns.set_theme(style="ticks")  # Modern seaborn style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['figure.figsize'] = [12, 7]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7
plt.rcParams['grid.color'] = '#cccccc'

# Read the data and convert semicolon separator and comma decimal
# df = pd.read_csv('Øygarden_temperature_2015_2025.csv', sep=';', decimal=',')
df = pd.read_csv('flesland_daily_average_temperature_from_1995.csv', sep=';', decimal=',')

# Create date range starting from January 1, 2015
start_date = datetime(1995, 1, 1)
df['date'] = [start_date + timedelta(days=i-1) for i in df['date']]

# Extract month and year for seasonal analysis
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Calculate moving average (365-day window) for trend
window_size = 365
df['trend'] = df['temperature'].rolling(window=window_size, center=True).mean()

# Apply Savitzky-Golay filter for smoother trend visualization
try:
    from scipy.signal import savgol_filter
    df['smooth_trend'] = savgol_filter(df['temperature'], 
                                       window_length=window_size, 
                                       polyorder=3)
except:
    # Fallback if savgol_filter is not available
    df['smooth_trend'] = df['trend']

# Create figure and axes with better proportions
fig, ax = plt.subplots(figsize=(12, 7))

# Plot temperature data with enhanced aesthetics
ax.plot(df['date'], df['temperature'], 
        linewidth=0.8, 
        color='#1f77b4', 
        alpha=0.7,
        label='Daglig temperatur')

# Add trend line
ax.plot(df['date'], df['smooth_trend'], 
        linewidth=2.5, 
        color='#d62728', 
        alpha=0.8,
        label='Temperaturtrend')

# Calculate and plot annual average temperatures
yearly_avg = df.groupby('year')['temperature'].mean()
years = [datetime(year, 1, 1) for year in yearly_avg.index]
ax.plot(years, yearly_avg.values, 'o-', 
        linewidth=2, 
        color='#2ca02c',
        markersize=6,
        markerfacecolor='white',
        markeredgewidth=2,
        label='Årlig gjennomsnitt')

# Format x-axis with cleaner date labels - show fewer years to avoid crowding
years = YearLocator(base=5)  # Show every 5 years instead of every year
months = MonthLocator(bymonth=[1])  # Only January
year_fmt = DateFormatter('%Y')

ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(year_fmt)
ax.xaxis.set_minor_locator(months)

# Customize the plot with Norwegian text
ax.set_xlabel('År', fontsize=12, fontweight='bold', labelpad=10)
ax.set_ylabel('Temperatur (°C)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_title('Temperaturvariasjon i Flesland (1995-2024)', 
             fontsize=14, fontweight='bold', pad=20)

# Format axis appearance
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xticks(rotation=0)  # Horizontal year labels

# Add some padding
plt.margins(x=0.01)

# Add legend with better positioning
legend = ax.legend(loc='upper right', frameon=True, framealpha=0.9, fontsize=10)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_edgecolor('lightgray')

# Add descriptive text about data - updated source
plt.figtext(0.02, 0.02, 'Datakilde: MET', 
            fontsize=8, color='gray', ha='left')

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('temperatur_plot_flesland.png', dpi=300, bbox_inches='tight')
plt.show()