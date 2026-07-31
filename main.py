from models.blob import Blob
from models.genome import Genome
from simulation.simulation import Simulation
from simulation.world import World


genome = Genome(
    speed=1.0,
    vision=10.0,
    metabolism=1.0,
    reproduction=100.0,
    mutation_rate=0.05,
)

kevin = Blob(
    x=50,
    y=50,
    energy=100,
    age=0,
    genome=genome,
)

world = World(
    width=100,
    height=100,
    blobs=[kevin],
)

simulation = Simulation(world)

for _ in range(10):
    simulation.step()

    for kevin in world.blobs:
        print(
            f"Tick {simulation.tick}: "
            f"({kevin.x:.2f}, {kevin.y:.2f}) "
            f"age={kevin.age}"
        )