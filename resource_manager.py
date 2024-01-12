# resource_manager.py
import traceback


class ResourceManager:
    def __init__(self):
        self.resources = {
            'population': 100,
            'currency': 1000,
            'minerals': 100,
            'energy': 100,
            'food': 500,
            'researchPoints': 0,
        }
        self.not_enough_food_logged = False
        self.no_food_counter = 0

    def is_population_extinct(self):
        """Check if the population has reached zero."""
        return self.resources['population'] <= 0

    def spend_resource(self, resource, amount):
        """ Spend a specified amount of a resource if available. """
        if self.resources[resource] >= amount:
            self.resources[resource] -= amount
            return True
        return False

    def earn_resource(self, resource, amount):
        """ Add a specified amount to a resource. """
        self.resources[resource] += amount

    def update_resources(self, buildingManager, population, log_event, update_labels):
        try:
            # Use the passed parameters instead of self
            generated_minerals = buildingManager.total_resource_production()
            generated_energy = buildingManager.total_energy_production()

            # Add generated energy and minerals to the total resources
            self.earn_resource('energy', generated_energy)
            self.earn_resource('minerals', generated_minerals)

            # Define power consumption rates for miners and farms
            power_consumption_per_miner = 1
            power_consumption_per_farm = 1

            # Calculate total power consumption for miners and farms
            total_power_consumption = (power_consumption_per_miner * len(buildingManager.extractors) +
                                       power_consumption_per_farm * len(buildingManager.farms))

            # Deduct energy for all miners and farms
            if self.resources['energy'] >= total_power_consumption:
                self.spend_resource('energy', total_power_consumption)
                food_produced = buildingManager.total_food_production()
                self.earn_resource('food', food_produced)
            else:
                log_event("Not enough energy for miners and farms to operate.")

            # Handle food consumption by the population
            food_consumed = population.consume_food()
            if self.resources['food'] >= food_consumed:
                self.spend_resource('food', food_consumed)
                population.grow()
            else:
                population.shrink()
                log_event("Population has shrunk due to lack of food.")

            # Update UI labels using the passed function
            update_labels()

        except Exception as e:
            # Detailed logging for the error
            error_message = f"Error during resource update: {str(e)}"
            print(error_message)
            traceback.print_exc()
            log_event(error_message)  # Log the error using the passed function
