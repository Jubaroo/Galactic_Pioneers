# building_manager.py

class BuildingManager:
    def __init__(self):
        self.extractors = []
        self.power_plants = []
        self.farms = []

    def add_extractor(self, extractor):
        self.extractors.append(extractor)

    def add_power_plant(self, plant):
        self.power_plants.append(plant)

    def total_resource_production(self):
        return sum(extractor.produce() for extractor in self.extractors)

    def total_energy_production(self):
        return sum(plant.generate_energy() for plant in self.power_plants)

    def add_farm(self, farm):
        self.farms.append(farm)

    def total_food_production(self):
        return sum(farm.produce_food() for farm in self.farms)


class ResourceExtractor:
    def __init__(self, resource_type, generation_rate):
        self.resource_type = resource_type
        self.generation_rate = generation_rate

    def produce(self):
        return self.generation_rate


class PowerPlant:
    def __init__(self, energy_output):
        self.energy_output = energy_output

    def generate_energy(self):
        return self.energy_output


class Farm:
    def __init__(self, food_production):
        self.food_production = food_production

    def produce_food(self):
        return self.food_production
