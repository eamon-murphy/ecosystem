import random
from simulation.world import World


class Simulation:
    def __init__(self, world: World):
        self.world = world
        self.tick = 0

    def step(self) -> None:
        for blob in self.world.blobs:
            # Move randomly within the range allowed by the blobs speed
            blob.x += random.uniform(-blob.genome.speed, blob.genome.speed)
            blob.y += random.uniform(-blob.genome.speed, blob.genome.speed)

            ## Keeps the blob within the limits of the world
            blob.x = max(0, min(self.world.width, blob.x))  
            blob.y = max(0, min(self.world.height, blob.y))

            blob.age += 1

        self.tick += 1