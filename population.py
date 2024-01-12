# population.py

class Population:
    def __init__(self, initial_size, growth_rate):
        self.size = initial_size
        self.growth_rate = growth_rate

    def grow(self):
        # Increase the population size by the growth rate, only if there's enough food
        self.size += self.size * self.growth_rate
        self.size = int(self.size)  # Ensure the population size is an integer

    def shrink(self):
        # Decrease the population size by the shrink rate due to lack of food
        # Ensure that the population does not go below a certain threshold, for example, 1
        if self.size > 1:
            self.size -= 1  # Adjust the shrink amount or rate as needed
        self.size = max(self.size, 1)  # Prevent population from going below 1

    def consume_food(self):
        # Food consumption rate is 10 food per 100 population
        food_consumption_rate = 0.1  # 10 food for 100 population
        return int(food_consumption_rate * self.size)
