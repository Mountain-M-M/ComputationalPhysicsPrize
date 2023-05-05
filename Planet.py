from LatitudeBelt import LatitudeBelt


class Planet:

  def __init__(self):
    self.radius = 6.4e6
    self.num_belts = 100
    self.mass = 5.98e24
    self.water_proportion = 0.71
    self.initial_temperature = -20
    self.latitude_belts = [LatitudeBelt(i, (273 + self.initial_temperature), self.radius, self.num_belts) for i in range(self.num_belts)]
    self.albedo_of_water = 0.07
    self.albedo_of_snow = 0.65
    self.albedo_of_land = 0.153
    self.obliquity = 0.41
    self.emissivity = 0.95