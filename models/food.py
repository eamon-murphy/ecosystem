from dataclasses import dataclass
from models.organism import Organism

@dataclass
class Food(Organism):
    energy: float