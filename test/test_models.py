from models.blob import Blob
from models.food import Food
from models.genome import Genome


def make_genome() -> Genome:
    return Genome(
        speed=1.0,
        vision=10.0,
        metabolism=0.1,
        reproduction=20.0,
        mutation_rate=0.05,
    )


def test_genome_stores_traits() -> None:
    genome = make_genome()

    assert genome.speed == 1.0
    assert genome.vision == 10.0
    assert genome.metabolism == 0.1
    assert genome.reproduction == 20.0
    assert genome.mutation_rate == 0.05


def test_blob_stores_organism_state() -> None:
    genome = make_genome()

    blob = Blob(
        x=5.0,
        y=8.0,
        energy=30.0,
        age=2,
        genome=genome,
    )

    assert blob.x == 5.0
    assert blob.y == 8.0
    assert blob.energy == 30.0
    assert blob.age == 2
    assert blob.genome is genome


def test_food_stores_position_and_energy() -> None:
    food = Food(
        x=3.0,
        y=4.0,
        energy=10.0,
    )

    assert food.x == 3.0
    assert food.y == 4.0
    assert food.energy == 10.0