from unittest.mock import patch

import pytest

from models.blob import Blob
from models.food import Food
from models.genome import Genome
from simulation.simulation import Simulation
from simulation.world import World


def make_blob(
    *,
    x: float = 5.0,
    y: float = 5.0,
    speed: float = 1.0,
    vision: float = 10.0,
    energy: float = 20.0,
    age: int = 0,
) -> Blob:
    genome = Genome(
        speed=speed,
        vision=vision,
        metabolism=0.1,
        reproduction=20.0,
        mutation_rate=0.05,
    )

    return Blob(
        x=x,
        y=y,
        energy=energy,
        age=age,
        genome=genome,
    )


def test_step_advances_tick() -> None:
    world = World(width=100, height=100)
    simulation = Simulation(world)

    simulation.step()

    assert simulation.tick == 1


def test_step_increases_blob_age() -> None:
    blob = make_blob(speed=0)
    world = World(width=100, height=100, blobs=[blob])
    simulation = Simulation(world)

    simulation.step()

    assert blob.age == 1


def test_blob_moves_towards_visible_food() -> None:
    blob = make_blob(
        x=0,
        y=0,
        speed=2,
        vision=20,
    )

    closest_food = Food(x=6, y=8, energy=10)
    farther_food = Food(x=12, y=0, energy=10)

    world = World(
        width=100,
        height=100,
        blobs=[blob],
        food=[farther_food, closest_food],
    )

    simulation = Simulation(world)
    simulation.move_blobs()

    # Direction from (0, 0) to (6, 8) is (0.6, 0.8).
    # At speed 2, movement should be (1.2, 1.6).
    assert blob.x == pytest.approx(1.2)
    assert blob.y == pytest.approx(1.6)


def test_blob_ignores_food_outside_vision() -> None:
    blob = make_blob(
        x=10,
        y=10,
        speed=1,
        vision=2,
    )

    food = Food(x=20, y=20, energy=10)

    world = World(
        width=100,
        height=100,
        blobs=[blob],
        food=[food],
    )

    simulation = Simulation(world)

    # No food is visible, so random wandering is used.
    with patch(
        "simulation.simulation.random.uniform",
        side_effect=[0.5, -0.25],
    ):
        simulation.move_blobs()

    assert blob.x == pytest.approx(10.5)
    assert blob.y == pytest.approx(9.75)


def test_blob_does_not_move_further_than_speed_towards_food() -> None:
    blob = make_blob(
        x=0,
        y=0,
        speed=3,
        vision=100,
    )

    food = Food(x=30, y=40, energy=10)

    world = World(
        width=100,
        height=100,
        blobs=[blob],
        food=[food],
    )

    simulation = Simulation(world)
    simulation.move_blobs()

    distance_moved = (blob.x**2 + blob.y**2) ** 0.5

    assert distance_moved == pytest.approx(3.0)


def test_blob_does_not_crash_when_already_on_food() -> None:
    blob = make_blob(x=5, y=5)
    food = Food(x=5, y=5, energy=10)

    world = World(
        width=100,
        height=100,
        blobs=[blob],
        food=[food],
    )

    simulation = Simulation(world)

    simulation.move_blobs()

    assert blob.x == 5
    assert blob.y == 5


def test_random_movement_is_clamped_to_world_bounds() -> None:
    blob = make_blob(
        x=9.5,
        y=0.5,
        speed=10,
        vision=0,
    )

    world = World(
        width=10,
        height=10,
        blobs=[blob],
    )

    simulation = Simulation(world)

    with patch(
        "simulation.simulation.random.uniform",
        side_effect=[5, -5],
    ):
        simulation.move_blobs()

    assert blob.x == 10
    assert blob.y == 0


def test_disperse_food_adds_food_to_world() -> None:
    world = World(width=100, height=50)
    simulation = Simulation(world)

    with patch(
        "simulation.simulation.random.uniform",
        side_effect=[25.0, 40.0],
    ):
        simulation.disperse_food()

    assert len(world.food) == 1

    food = world.food[0]

    assert food.x == 25.0
    assert food.y == 40.0
    assert food.energy == 10


def test_food_is_dispersed_every_five_ticks() -> None:
    world = World(width=100, height=100)
    simulation = Simulation(world)

    with patch.object(simulation, "disperse_food") as disperse_food:
        for _ in range(4):
            simulation.step()

        disperse_food.assert_not_called()

        simulation.step()

        disperse_food.assert_called_once()


def test_blob_eats_food_in_same_tile() -> None:
    blob = make_blob(
        x=1.1,
        y=3.8,
        speed=0,
        energy=20,
    )

    food = Food(
        x=1.9,
        y=3.1,
        energy=10,
    )

    world = World(
        width=100,
        height=100,
        blobs=[blob],
        food=[food],
    )

    simulation = Simulation(world)
    simulation.step()

    assert blob.energy == 20
    assert food not in world.food


def test_blob_does_not_eat_food_in_different_tile() -> None:
    blob = make_blob(
        x=1.9,
        y=3.8,
        speed=0,
        energy=20,
    )

    food = Food(
        x=2.0,
        y=3.1,
        energy=10,
    )

    world = World(
        width=100,
        height=100,
        blobs=[blob],
        food=[food],
    )

    simulation = Simulation(world)
    simulation.step()

    assert blob.energy == 10
    assert food in world.food