# planet.py

class Planet:
    def __init__(self, name, planet_type, resources):
        self.name = name
        self.planet_type = planet_type
        # Dictionary of resources
        self.resources = resources
