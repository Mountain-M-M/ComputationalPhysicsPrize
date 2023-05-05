# Importing matplotlib for graphs + classes from other files

from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
import numpy as np

from Planet import Planet
from Sun import Sun

sun = Sun()
planet = Planet()

# Lists for graphs (x -> time, y -> temperature, z -> index)

x = []
y = []
z = []

y_2d = []  # This is the y-axis list for when a 2d graph is generated

values = ["5.148e18", "700", "280", "6.4e6", "0.71", "-20", "0.41", "0.95", "3.8e26", "1.5e11", "5"]

def main_program(values):

    # Constants

    STEFAN = 5.670e-8
    MASS_OF_ATMOSPHERE = float(values[0])
    HEAT_CAPACITY_OF_AIR = float(values[1])
    CO2_CONC = float(values[2])

    planet.radius = float(values[3])
    planet.water_proportion = float(values[4])
    planet.initial_temperature = float(values[5])
    planet.obliquity = float(values[6])
    planet.emissivity = float(values[7])

    sun.luminosity = float(values[8])
    sun.distance_from_planet = float(values[9])


    for i in range(planet.num_belts):  # Creating values for z axis (index of latitude belt)
        z.append(i)

    t = 0
    dt = 24 * 60 * 60

    # Time loop

    count = 0  # number of time steps that have passed

    while t < (dt * 365 * int(values[10])):  # Determines how long the simulation will run for
        change_in_temperatures = []  # This list will hold all the changes in temperature for each time step.

        for i in range(planet.num_belts):
            planet.latitude_belts[i].perceived_area = planet.latitude_belts[i].calculate_perceived_area(planet.radius,
                                                                                                        planet.num_belts,
                                                                                                        count,
                                                                                                        planet.obliquity)

            energy_absorbed = planet.latitude_belts[i].calculate_energy_absorbed(sun.luminosity, sun.distance_from_planet,
                                                                                 dt, 0, CO2_CONC)

            energy_transferred = planet.latitude_belts[i].calculate_energy_transferred(planet.latitude_belts, dt)

            energy_absorbed += energy_transferred

            energy_emitted = planet.latitude_belts[i].calculate_energy_emitted(STEFAN, dt, planet.emissivity)

            change_in_temperature = planet.latitude_belts[i].calculate_temperature_change(energy_absorbed, energy_emitted,
                                                                                          MASS_OF_ATMOSPHERE,
                                                                                          HEAT_CAPACITY_OF_AIR,
                                                                                          planet.num_belts)

            change_in_temperatures.append(change_in_temperature)

            planet.latitude_belts[i].albedo = planet.latitude_belts[i].calculate_albedo(planet.water_proportion,
                                                                                        planet.albedo_of_snow,
                                                                                        planet.albedo_of_land,
                                                                                        planet.albedo_of_water)

        for i in range(planet.num_belts):  # Adding on the temperatures
            planet.latitude_belts[i].temperature += change_in_temperatures[i]

        CO2_CONC = CO2_CONC * 1  # This is how much CO2 to add/multiply each time step

        total = 0  # This is a temporary variable for calculating the average temperature

        for belt in planet.latitude_belts:
            total += belt.temperature

        y_2d.append(total / planet.num_belts - 273)

        x.append(t / (24 * 60 * 60))

        holder = []  # Temporary variable for adding values to the y-axis
        for belt in planet.latitude_belts:
            holder.append(belt.temperature - 273)
        y.append(holder)

        count += 1  # Incrementing the number of time steps that have passed
        t += dt  # Incrementing time


# 3D graph creation

def graph_3d(x, y, z):

    y = np.array(y)
    norm = Normalize(vmin=y.min(), vmax=y.max())
    x_grid, z_grid = np.meshgrid(x, z)
    y = y.T

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(X=x_grid, Y=z_grid, Z=y, cmap='coolwarm', norm=norm)

    ax.set_xlabel('Time / days')
    ax.set_ylabel('Latitude Belt Index')
    ax.set_zlabel('Temperature / Degrees Celsius')

    plt.show()

# 2D graph creation

def graph_2d(x, y):

    plt.plot(x, y)
    plt.xlabel('Time / Days')
    plt.ylabel('Temperature / Degrees Celsius')

    plt.show()


def get_values():
    variables = ["Mass of atmosphere", "Heat capacity of air", "CO2 concentration", "Radius of planet", "Water proportion", "Initial temperature", "Obliquity", "Emissivity", "Luminosity of sun", "Distance between planet and earth", "Years"]
    finished = False
    while not finished:
        for i in range(len(variables)):
            print("{}) {}: {}".format(i+1, variables[i], values[i]))

        choice = input("Enter value to edit: ")
        print("**Note that 2.3x10^3 == 2.3e3 in Python**")
        values[int(choice)-1] = input("Enter new value: ")
        choice = input("Edit another value? (y/n): ")
        if choice == "n":
            finished = True

finished = False

while not finished:
    print("1) Edit Values")
    print("2) 2D Graph")
    print("3) 3D Graph")
    print("4) Quit")

    choice = input("Enter an option: ")

    if choice == "1":
        get_values()
    elif choice == "2":
        main_program(values)
        try:
            graph_2d(x, y_2d)
        except:
            print("Error with creating graph. Please restart program")
            print("This error can occur if values caused program to crash or sometimes the graph fails to load on the second loop of the program")
    elif choice == "3":
        main_program(values)
        try:
            graph_3d(x, y, z)
        except:
            print("Error with creating graph. Please restart program")
            print("This error can occur if values caused program to crash or sometimes the graph fails to load on the second loop of the program")

    elif choice == "4":
        print("Quitting...")
        finished = True
