import random
from simulation.world import World
from models.food import Food
import math


class Simulation:
    def __init__(self, world: World):
        self.world = world
        self.tick = 0

    def step(self) -> None:
        for blob in self.world.blobs:

            self.move_blobs()

            for food in self.world.food:
                if int(blob.x) == int(food.x) and int(blob.y) == int(food.y):
                     blob.energy += food.energy
                     self.world.food.remove(food)

            blob.energy -= 10
            blob.age += 1
            if blob.energy <= 0:
                 blob.age = -1

        self.tick += 1

        if self.tick % 5 == 0: # Disperse food every 5 ticks
                    self.disperse_food()

    def disperse_food(self) -> None:
        food = Food (
            x=random.uniform(0, self.world.width),
            y=random.uniform(0, self.world.height),
            energy=10 # For now all food is 10 energy
        )

        self.world.food.append(food)

    def move_blobs(self) -> None:
        for blob in self.world.blobs:

            target_food = None
            closest_distance = float("inf")
            # Find the closest food that is within vision
            for food in self.world.food:

                dx = food.x - blob.x
                dy = food.y - blob.y
                distance = math.hypot(dx, dy)


                if distance > blob.genome.vision:
                     continue

                elif distance < closest_distance:
                     closest_distance = distance
                     target_food = food

            # If we found food within vision,
            # move towards it.
            if target_food is not None:

                dx = target_food.x - blob.x
                dy = target_food.y - blob.y

                distance = math.hypot(dx, dy)

                # Avoid dividing by zero if the blob is already on the food
                if distance > 0:
                    direction_x = dx / distance
                    direction_y = dy / distance

                    blob.x += direction_x * blob.genome.speed
                    blob.y += direction_y * blob.genome.speed

            else:
                # Move randomly within the range allowed by the blobs speed
                blob.x += random.uniform(-blob.genome.speed, blob.genome.speed)
                blob.y += random.uniform(-blob.genome.speed, blob.genome.speed)
                # Keeps the blob within the limits of the world
                blob.x = max(0, min(self.world.width, blob.x)) 
                blob.y = max(0, min(self.world.height, blob.y))

    