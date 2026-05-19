import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. Import the data from "fcc-forum-pageviews.csv" and set index to 'date'
# Parse dates explicitly so Pandas treats the index as a DatetimeIndex
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_index=False)
df.set_index('date', inplace=True)

# 2. Clean data by filtering out top 2.5% and bottom 2.5% of the dataset
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Copy data frame for safety
    df_line = df.copy()

    # Draw line plot using Matplotlib
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)

    # Set exact titles and labels required by the tests
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return the figure
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy data frame and prepare data for a monthly grouped bar chart
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Group by year and month, calculate the mean, and pivot the structure
    df_pivot = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # The order of columns matters! Reorder them chronologically
    months_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_pivot = df_pivot.reindex(columns=months_order)

    # Draw the grouped bar plot
    fig = df_pivot.plot(kind='bar', figsize=(10, 8)).get_figure()
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', labels=months_order)

    # Save image and return the figure
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this chunk is often provided in the boilerplate)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw side-by-side box plots using Seaborn
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Left plot: Year-wise Trend
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Right plot: Month-wise Seasonality
    # Enforce standard chronological ordering for shortened months
    months_short_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=months_short_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return the figure
    fig.savefig('box_plot.png')
    return fig
