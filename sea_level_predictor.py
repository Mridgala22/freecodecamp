import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # 1. Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # 2. Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], color='blue', alpha=0.5, label='Actual Data')

    # 3. Create first line of best fit (Entire dataset: 1880 - 2050)
    # Get the slope and intercept
    res_all = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    
    # Generate an array of years from 1880 all the way to 2050 for the prediction
    years_all = pd.Series([i for i in range(1880, 2051)])
    
    # Calculate predicted y values using the linear equation: y = mx + c
    sea_levels_all = res_all.slope * years_all + res_all.intercept
    plt.plot(years_all, sea_levels_all, color='red', label='Best Fit Line (1880-2050)')

    # 4. Create second line of best fit (Recent dataset: 2000 - 2050)
    # Filter out data before the year 2000
    df_recent = df[df['Year'] >= 2000]
    
    # Get the slope and intercept for the recent data subset
    res_recent = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
    
    # Generate an array of years from 2000 to 2050
    years_recent = pd.Series([i for i in range(2000, 2051)])
    
    # Calculate predicted y values for the recent trend line
    sea_levels_recent = res_recent.slope * years_recent + res_recent.intercept
    plt.plot(years_recent, sea_levels_recent, color='green', label='Best Fit Line (2000-2050)')

    # 5. Add labels, title, and legend
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    plt.legend()
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()
