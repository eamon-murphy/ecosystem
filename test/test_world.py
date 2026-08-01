from models.blob import Blob
from models.food import Food
from models.genome import Genome
from simulation.world import World


def make_blob() -> Blob:
    genome = Genome(
        speed=1.0,
        vision=10.0,
        metabolism=0.1,
        reproduction=10.0,
        mutation_rate=0.05,
    )

    return Blob(
        x=5.0,
        y=5.0,
        energy=30.0,
        age=0,
        genome=genome,
    )


def test_world_starts_with_empty_lists() -> None:
    world = World(width=100, height=100)

    assert world.blobs == []
    assert world.food == []


def test_world_instances_do_not_share_lists() -> None:
    first_world = World(width=100, height=100)
    second_world = World(width=100, height=100)

    first_world.blobs.append(make_blob())
    first_world.food.append(Food(x=1, y=1, energy=10))

    assert len(first_world.blobs) == 1
    assert len(first_world.food) == 1

    assert second_world.blobs == []
    assert second_world.food == []


def test_world_accepts_initial_entities() -> None:
    blob = make_blob()
    food = Food(x=10, y=20, energy=10)

    world = World(
        width=100,
        height=100,
        blobs=[blob],
        food=[food],
    )

    assert world.blobs == [blob]
    assert world.food == [food]