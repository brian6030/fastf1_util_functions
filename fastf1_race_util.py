import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_laptimes_boxplot(data, x, y, hue, order, palette, figsize=(15, 10), xlabel=None, title=None):
    """
    Plot a boxplot of lap times.

    Parameters:
    - data: DataFrame containing the data to plot
    - x: str, the column name for the x-axis (categorical data)
    - y: str, the column name for the y-axis (numeric data)
    - hue: str, the column name for the hue (categorical data for color encoding)
    - order: list, the order of categories for the x-axis
    - palette: dict or list, the colors to use for the different categories
    - figsize: tuple, the size of the figure (default: (15, 10))
    - xlabel: str, the label for the x-axis (default: None)
    - title: str, the title of the plot (default: None)

    Returns:
    - None: Displays the plot.
    """

    fig, ax = plt.subplots(figsize=figsize)
    sns.boxplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        order=order,
        palette=palette,
        whiskerprops=dict(color="white"),
        boxprops=dict(edgecolor="white"),
        medianprops=dict(color="grey"),
        capprops=dict(color="white"),
    )

    plt.grid(visible=False)

    if xlabel:
        ax.set(xlabel=xlabel)
    else:
        ax.set(xlabel=None)

    if title:
        plt.title(title)

    plt.tight_layout()
    plt.show()


def plot_lap_time_distributions(driver_laps, finishing_order, driver_colors, compound_colors, title=None, marker_size = 4, figsize=(10, 5)):
    """
    Utility function to plot lap time distributions for each driver.
    
    Parameters:
    - driver_laps: DataFrame containing the lap data for drivers
    - finishing_order: list, the order of drivers to display on the x-axis
    - driver_colors: dict, mapping of driver abbreviations to colors
    - compound_colors: dict, mapping of tire compounds to colors
    - title: str, the title of the plot (default: None)
    - marker_size: float, size of the markers (default: 4)
    - figsize: tuple, the size of the figure (default: (10, 5))
    
    Returns:
    - None: Displays the plot.
    """
    # Convert LapTime to seconds if not already done
    if "LapTime (s)" not in driver_laps.columns:
        driver_laps["LapTime (s)"] = driver_laps["LapTime"].dt.total_seconds()

    # Create the figure
    fig, ax = plt.subplots(figsize=figsize)

    # Violin plot
    sns.violinplot(data=driver_laps,
                   x="Driver",
                   y="LapTime (s)",
                   hue="Driver",
                   inner=None,
                   density_norm="area",
                   order=finishing_order,
                   palette=driver_colors
                   )

    # Swarm plot
    sns.swarmplot(data=driver_laps,
                  x="Driver",
                  y="LapTime (s)",
                  order=finishing_order,
                  hue="Compound",
                  palette=compound_colors,
                  hue_order=["SOFT", "MEDIUM", "HARD"],
                  linewidth=0,
                  size=marker_size,
                  )

    # Customize labels and title
    ax.set_xlabel("Driver")
    ax.set_ylabel("Lap Time (s)")
    if title:
        plt.suptitle(title)
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    plt.show()


def plot_driver_positions(lap_data, driver_colors, title="Race Position Changes", figsize=(8.0, 4.9)):
    """
    Plots the race position changes for each driver in a session.

    Parameters:
    - lap_data: DataFrame containing the lap data for drivers, expected to have columns 'Driver', 'LapNumber', and 'Position'
    - driver_colors: dict, mapping of driver identifiers to colors
    - title: str, the title of the plot (default: "Race Position Changes")
    - figsize: tuple, the size of the figure (default: (8.0, 4.9))
    """
    fig, ax = plt.subplots(figsize=figsize)

    drivers = lap_data['Driver'].unique()
    for driver in drivers:
        drv_laps = lap_data[lap_data['Driver'] == driver]
        
        if drv_laps.empty:
            continue  # Skip if no lap data for driver

        color = driver_colors.get(driver, 'black')  # Use black as default if no color is specified

        ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=driver, color=color)

    ax.set_ylim([20.5, 0.5])  # Adjust as necessary for the number of drivers
    ax.set_yticks([1, 5, 10, 15, 20])
    ax.set_xlabel('Lap')
    ax.set_ylabel('Position')

    handles, labels = ax.get_legend_handles_labels()
    if labels:
        ax.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_tyre_strategy(drivers, stints, driver_colors, compound_colors, title="Tyre Strategy", figsize=(10, 5)):
    """
    Plots the tyre strategies for each driver in a session.
    
    Parameters:
    - drivers: list of drivers
    - stints: DataFrame containing the stint data for drivers
    - driver_colors: dict, mapping of driver identifiers to colors
    - compound_colors: dict, mapping of compound names to colors
    - title: str, the title of the plot (default: "Tyre Strategy")
    - figsize: tuple, the dimensions of the figure (default: (10, 5))
    """
    
    fig, ax = plt.subplots(figsize=figsize)

    for driver in drivers:
        driver_stints = stints.loc[stints["Driver"] == driver]

        previous_stint_end = 0  # Reset the stint end marker for each driver

        for idx, row in driver_stints.iterrows():
            ax.barh(
                y=driver,
                width=row["StintLength"],
                left=previous_stint_end,
                color=compound_colors.get(row["Compound"], 'gray'),  # Default to gray if no color is found
                edgecolor="black",
                fill=True
            )
            previous_stint_end += row["StintLength"]

    plt.title(title)
    plt.xlabel("Lap Number")

    ax.xaxis.grid(True)  # Enable the grid for x-axis
    ax.yaxis.grid(False)  # Disable the grid for y-axis
    # invert the y-axis so drivers that finish higher are closer to the top
    ax.invert_yaxis()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.show()


def prepare_driver_laps(session, drivers, stints):
    """
    Prepares a DataFrame with lap times and stint information for each driver.
    
    Parameters:
    - session: FastF1 session object containing the race data
    - drivers: list of driver codes
    - stints: DataFrame containing stint information for drivers
    
    Returns:
    - DataFrame with combined lap times and stint information for all drivers
    """
    driver_laps_list = []
    for driver in drivers:
        driver_laps = session.laps.pick_drivers(driver).pick_quicklaps().reset_index(drop=True)
        driver_laps['Driver'] = driver  # Add a column for the driver code

        # Get stint information for the driver
        driver_stints = stints.loc[stints["Driver"] == driver]
        stint_lengths = driver_stints["StintLength"].tolist()

        # Assign stint number to each lap based on stint length
        start_lap = 1
        for stint_number, stint_length in enumerate(stint_lengths, start=1):
            end_lap = start_lap + stint_length - 1
            driver_laps.loc[(driver_laps['LapNumber'] >= start_lap) & (driver_laps['LapNumber'] <= end_lap), 'Stint'] = stint_number
            start_lap = end_lap + 1  # Next stint starts after the last lap of the current stint

        driver_laps_list.append(driver_laps)

    # Concatenate all dataframes in the list
    return pd.concat(driver_laps_list, ignore_index=True)
    
    
def plot_driver_laps(session, drivers, stints, title='Lap time comparison of each stint'):
    """
    Plots the lap times for drivers across their stints.
    
    Parameters:
    - all_driver_laps: DataFrame containing lap times, driver identifiers, and stint numbers
    
    Returns:
    - None: Displays the plot.
    """
    all_driver_laps = prepare_driver_laps(session, drivers, stints)

    fig, ax = plt.subplots(figsize=(14, 10))
    sns.lineplot(data=all_driver_laps,
                 x="LapNumber",
                 y="LapTime",
                 ax=ax,
                 hue="Driver",  # Use the driver code as the hue
                 style="Stint",  # Use the stint number for style (which includes color)
                 palette="tab10",  # You can use any color palette you prefer
                 linewidth=2)  # Set the line width

    ax.set_title(title)
    ax.set_ylabel('Lap Time (s)')
    ax.invert_yaxis()  # Typically, lower lap times are better, so invert the axis

    # Improve legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, title='Driver and Stint', loc='upper right')

    plt.show()
