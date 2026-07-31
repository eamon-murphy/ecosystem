from dataclasses import dataclass
from models.genome import Genome
from models.organism import Organism


@dataclass
class Blob(Organism):
    energy: float
    age: int
    genome: Genome

