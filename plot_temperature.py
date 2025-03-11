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
df = pd.read_csv('Øygarden_temperature_2015_2025.csv', sep=';', decimal=',')

# Create date range starting from January 1, 2015
start_date = datetime(2015, 1, 1)
df['date'] = [start_date + timedelta(days=i-1) for i in df['date']]

# Extract month and year for seasonal analysis
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Calculate seasonal colors
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

df['season'] = df['month'].apply(get_season)

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
        label='Daily Temperature')

# Add trend line
ax.plot(df['date'], df['smooth_trend'], 
        linewidth=2.5, 
        color='#d62728', 
        alpha=0.8,
        label='Temperature Trend')

# Calculate and plot annual average temperatures
yearly_avg = df.groupby('year')['temperature'].mean()
years = [datetime(year, 1, 1) for year in yearly_avg.index]
ax.plot(years, yearly_avg.values, 'o-', 
        linewidth=2, 
        color='#2ca02c',
        markersize=6,
        markerfacecolor='white',
        markeredgewidth=2,
        label='Annual Average')

# Add mean temperature reference line
mean_temp = df['temperature'].mean()
ax.axhline(y=mean_temp, color='gray', linestyle='-', alpha=0.5, linewidth=1)
ax.text(df['date'].iloc[-500], mean_temp+0.5, 
        f'Mean: {mean_temp:.1f}°C', 
        fontsize=9, color='dimgray')

# Format x-axis with cleaner date labels
years = YearLocator()
months = MonthLocator(bymonth=[1, 7])  # January and July
year_fmt = DateFormatter('%Y')

ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(year_fmt)
ax.xaxis.set_minor_locator(months)

# Customize the plot
ax.set_xlabel('Year', fontsize=12, fontweight='bold', labelpad=10)
ax.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_title('Temperature Variation in Øygarden (2015-2025)', 
             fontsize=14, fontweight='bold', pad=20)

# Format axis appearance
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xticks(rotation=0)  # Horizontal year labels look better

# Add some padding
plt.margins(x=0.01)

# Add legend with better positioning
legend = ax.legend(loc='upper right', frameon=True, framealpha=0.9, fontsize=10)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_edgecolor('lightgray')

# Add descriptive text about data
plt.figtext(0.02, 0.02, 'Data source: yr.no/Øygarden (2015-2025)', 
            fontsize=8, color='gray', ha='left')

# Add seasonal highlights (subtle background shading)
for season, color in [('Winter', '#e1f5fe'), ('Summer', '#fffde7')]:
    season_data = df[df['season'] == season]
    if not season_data.empty:
        for year in season_data['year'].unique():
            year_data = season_data[season_data['year'] == year]
            if len(year_data) > 0:
                ax.axvspan(year_data['date'].min(), year_data['date'].max(), 
                          alpha=0.2, color=color, zorder=0)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('temperature_plot_publication.png', dpi=300, bbox_inches='tight')
plt.show()