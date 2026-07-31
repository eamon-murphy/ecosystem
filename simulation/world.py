from dataclasses import dataclass, field

from models.blob import Blob

@dataclass
class World:
    width: float
    height: float
    blobs: list[Blob] = field(default_factory=list)