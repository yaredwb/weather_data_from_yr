import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Simulation results files
simulation_results_files = [
    'temperature_vs_depth_results_profile_x=5.0_oygard_model_concrete_channel_1995-2025.csv',
    'temperature_vs_depth_results_profile_x=4.8_oygard_model_concrete_channel_1995-2025.csv',
    'temperature_vs_depth_results_profile_x=4.4_oygard_model_concrete_channel_1995-2025.csv',
]

# Read the simulation results
dataframes = []
for file in simulation_results_files:
    df = pd.read_csv(file, sep=';', encoding='latin1', skiprows=2, header=None, decimal=',')
    # Set column names, first column depth, second column T(°C) Day 1, third column T(°C) Day 2, etc.
    # Assuming the first column is depth and the rest are temperature values
    df.columns = ['Depth (m)'] + [f'Temperature Day {i+1}' for i in range(df.shape[1]-1)]    
    dataframes.append(df)


# Determine the frost penetration depth for each simulation result, for each day
frost_penetration_depths = []
for df in dataframes:
    frost_depths = []
    for col in df.columns[1:]:
        temperatures = df[col].values
        depths = df['Depth (m)'].values
        
        # Check if there's any frost at all
        if np.min(temperatures) >= 0:
            # No frost
            frost_depth = np.nan
        elif np.max(temperatures) < 0:
            # Everything is frozen
            frost_depth = max(depths)
        else:
            # Find the deepest point where temperature is <= 0°C
            frozen_indices = np.where(temperatures <= 0)[0]
            if len(frozen_indices) > 0:
                max_frozen_index = frozen_indices[-1]
                
                # If this is the last point, use it as frost depth
                if max_frozen_index == len(temperatures) - 1:
                    frost_depth = depths[max_frozen_index]
                else:
                    # Interpolate between the last frozen point and the first non-frozen point
                    t1 = temperatures[max_frozen_index]
                    t2 = temperatures[max_frozen_index + 1]
                    d1 = depths[max_frozen_index]
                    d2 = depths[max_frozen_index + 1]
                    
                    # Linear interpolation
                    frost_depth = d1 + (0 - t1) * (d2 - d1) / (t2 - t1)
            else:
                frost_depth = np.nan
                
        frost_depths.append(frost_depth)
    frost_penetration_depths.append(frost_depths)

# Location of top of water pipe (defined early for the frost depth check)
depth_water_pipe = 0.47  # in meters

# Find days when frost depth exceeds water pipe depth
print("\nDays when frost depth exceeds water pipe depth ({}m):".format(depth_water_pipe))
for i, frost_depths in enumerate(frost_penetration_depths):
    critical_days = []
    for day, depth in enumerate(frost_depths, start=1):
        if depth is not None and depth > depth_water_pipe:
            critical_days.append(day)
    
    profile_name = f"Profile {i+1}"
    if critical_days:
        print(f"{profile_name}: Days {', '.join(map(str, critical_days))} (total: {len(critical_days)} days)")
    else:
        print(f"{profile_name}: No days with frost depth exceeding water pipe depth")

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

# Location of top of water pipe
depth_water_pipe = 0.47  # in meters

# Create figure with subplots - make it longer horizontally
fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
fig.tight_layout(pad=3.0)

# Norwegian text for labels
x_label = 'Dag'
y_label = 'Frostdybde (m)'
water_pipe_label = 'Vannrør'
profile_label = 'Profil'

# Plot each profile in its own subplot
for i, frost_depths in enumerate(frost_penetration_depths):
    ax = axes[i]
    
    # Plot frost depth
    ax.plot(range(len(frost_depths)), frost_depths, color='blue', linewidth=2)
    
    # Add water pipe depth as horizontal dashed line
    ax.axhline(y=depth_water_pipe, color='red', linestyle='--', linewidth=1.5, 
               label=water_pipe_label)
    
    # Add labels and legend
    if i == 2:  # Only add x-label to bottom plot
        ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_title(f'{profile_label} {i+1}', fontsize=14)
    
    # Invert y-axis so deeper points are shown lower
    ax.invert_yaxis()
    
    # Add legend
    ax.legend(loc='best')
    
    # Improve appearance for publication quality
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.tick_params(axis='both', which='major', labelsize=10)
    
    # Set y-limits to be consistent across subplots
    ax.set_ylim(bottom=1.0, top=0)  # Adjust these values based on your data range

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(hspace=0.3)  # Add space between subplots

# Save as high-resolution image for publication
plt.savefig('frost_depth_profiles.png', dpi=300, bbox_inches='tight')

plt.show()

