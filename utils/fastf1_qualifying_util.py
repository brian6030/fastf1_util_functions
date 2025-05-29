import matplotlib.pyplot as plt

def plot_telemetry(session, driver_abbrs):
    """
    Plot telemetry data (Speed, Throttle, Brake, Gear, RPM, DRS) for given drivers in a session.

    Args:
        session: fastf1.Session object (loaded)
        driver_abbrs: list of driver abbreviations, e.g. ['NOR', 'PIA', 'VER']
    """
    telemetry = []
    for driver in driver_abbrs:
        lap = session.laps.pick_drivers(driver).pick_fastest()
        telemetry.append(lap.get_telemetry())

    fig, axes = plt.subplots(6, 1, figsize=(12, 12), sharex=True)

    # You can customize colors or use a default set here
    default_colors = ['orange', 'red', 'blue', 'green', 'purple', 'brown']
    driver_colors = {d: default_colors[i % len(default_colors)] for i, d in enumerate(driver_abbrs)}

    for driver_data, driver_name in zip(telemetry, driver_abbrs):
        axes[0].plot(driver_data['Distance'], driver_data['Speed'], label=f"{driver_name} Speed (km/h)", color=driver_colors[driver_name])
        axes[1].plot(driver_data['Distance'], driver_data['Throttle'], label=f"{driver_name} Throttle (%)", color=driver_colors[driver_name])
        axes[2].plot(driver_data['Distance'], driver_data['Brake'], label=f"{driver_name} Brake", color=driver_colors[driver_name])
        axes[3].plot(driver_data['Distance'], driver_data['nGear'], label=f"{driver_name} Gear", color=driver_colors[driver_name])
        axes[4].plot(driver_data['Distance'], driver_data['RPM'], label=f"{driver_name} RPM", color=driver_colors[driver_name])
        axes[5].plot(driver_data['Distance'], driver_data['DRS'], label=f"{driver_name} DRS (1=Active, 0=Off)", color=driver_colors[driver_name])

    for ax in axes:
        ax.legend()
        ax.grid()

    axes[0].set_ylabel("Speed (km/h)")
    axes[1].set_ylabel("Throttle (%)")
    axes[2].set_ylabel("Brake")
    axes[3].set_ylabel("Gear")
    axes[4].set_ylabel("RPM")
    axes[5].set_ylabel("DRS")
    axes[5].set_xlabel("Distance (m)")

    plt.suptitle(f"Q3 Top Drivers Fastest Lap Telemetry Data ({session.event['EventName']} {session.event.year})")
    plt.show()
