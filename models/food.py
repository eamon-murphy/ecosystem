from dataclasses import dataclass
from models import Organism

@dataclass
class Food(Organism):
    energy: float