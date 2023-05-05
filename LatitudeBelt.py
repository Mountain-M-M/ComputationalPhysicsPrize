import math


class LatitudeBelt:

    def __init__(self, index, temperature, radius, num_belts):
        self.index = index
        self.albedo = 0
        self.temperature = temperature
        self.perceived_area = 0
        self.actual_area = self.calculate_actual_area(radius, num_belts)
        self.snow = self.check_if_snow()

    def check_if_snow(self):
        if self.temperature < 263:
            return True
        else:
            return False

    def calculate_perceived_area(self, radius, num_belts, number_of_time_steps, obliquity):
        n = self.index
        N = num_belts
        Po = obliquity * math.pi / 180 * math.sin(2 * math.pi * number_of_time_steps / 365)
        theta = math.pi / N
        r = radius

        return r ** 2 * (math.sin(2 * n * theta - Po) + -1 *
                         math.sin(2 * n * theta + 2 * theta + Po)) / 2 + (r ** 2 * theta)

    def calculate_actual_area(self, radius, num_belts):
        n = self.index
        theta = math.pi / num_belts
        r = radius
        return 2 * math.pi * r ** 2 * (math.cos(theta * n) - math.cos(theta *
                                                                      (n + 1)))

    def calculate_energy_absorbed(self, luminosity, distance_from_sun, dt,
                                  obliquity, co2_conc):
        D = distance_from_sun
        L = luminosity
        pA = self.perceived_area
        aA = self.actual_area
        a = self.albedo
        o = obliquity

        return (math.cos(o) * pA * (1 - a) * L / (4 * math.pi * D ** 2) + (
                150 + (5.35 * math.log(co2_conc / 270))) * aA) * dt

    def calculate_energy_transferred(self, latitude_belts, dt):

        n = self.index
        Tc = latitude_belts[n].temperature
        Aac = self.actual_area

        try:
            Tn1 = latitude_belts[self.index - 1].temperature
            Aan1 = latitude_belts[n - 1].actual_area
        except:
            Tn1 = Tc
            Aan1 = 0

        try:
            Tn2 = latitude_belts[self.index + 1].temperature
            Aan2 = latitude_belts[n + 1].actual_area
        except:
            Tn2 = Tc
            Aan2 = 0

        return (2.3 * (Aac + Aan1) * (-Tc + Tn1) + (2.3 * (Aan2 + Aac) * (Tn2 - Tc))) * dt

    def calculate_energy_emitted(self, stefan, dt, emissivity):
        s = stefan
        aA = self.actual_area
        T = self.temperature
        e = emissivity

        return s * e * aA * T ** 4 * dt

    def calculate_stable_temperature(self, dt, energy_absorbed, stefan):
        Qin = energy_absorbed
        s = stefan
        aA = self.actual_area

        return (Qin / (aA * s * dt)) ** 0.25

    def calculate_temperature_change(self, energy_absorbed, energy_emitted,
                                     mass_of_atmosphere, heat_capacity_of_air,
                                     num_belts):
        Qin = energy_absorbed
        Qout = energy_emitted
        m = mass_of_atmosphere
        N = num_belts
        c = heat_capacity_of_air
        return (19 / 70) * (Qin - Qout) / ((m / N) * c)

    def calculate_albedo(self, water_proportion, albedo_of_snow, albedo_of_land,
                         albedo_of_water):
        w = water_proportion
        s = self.check_if_snow()
        Al = albedo_of_land
        Aw = albedo_of_water
        As = albedo_of_snow

        if s:
            return As
        else:
            return (Al * (1 - w) + Aw * (1 + w)) * 2
