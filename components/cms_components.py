from rest.utils.cms import CMSComponentDefinition
from dataclasses import dataclass
import pygame
from typing import Tuple, Dict, List, Any

# engine components (doesn't delete)

@dataclass
class Animations(CMSComponentDefinition):
    value: Dict[str, Any]
    current: Any = None

@dataclass
class Config(CMSComponentDefinition):
    size: List[int]
    offset: List[int]
    centered: bool

@dataclass
class CameraComponent(CMSComponentDefinition):
    size: Tuple[int, int]
    pos: List[float]
    slowness: float
    tilemap: Any = None
    int_pos: Tuple[int, int] = (0, 0)
    rect: pygame.Rect | None = None
    target_pos: Tuple[float, float] | None = None

@dataclass
class Tilemap(CMSComponentDefinition):
    tile_size: Tuple[int, int]
    dimensions: Tuple[int, int]
    grid_tiles: Dict[Tuple[int, int], Dict[int, Any]]


# other components
# -------------------------------------------------------------------------------------------------------------
class Health(CMSComponentDefinition):
    hp: int

class Energy(CMSComponentDefinition):
    value: int
    
class TestBehavior(CMSComponentDefinition):
    value: bool