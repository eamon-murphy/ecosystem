from dataclasses import dataclass, field

from models.blob import Blob
from models.food import Food

@dataclass
class World:
    width: float
    height: float
    blobs: list[Blob] = field(default_factory=list)
    food: list[Food] = field(default_factory=list)