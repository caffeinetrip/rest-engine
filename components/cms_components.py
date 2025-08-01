from rest.utils.cms import CMSComponentDefinition
from dataclasses import dataclass
import pygame
from typing import Tuple, Dict, List, Any

# engine components (doesn't delete)

# entity
# --------------------------------------------------------------------------------------------------------------------

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


class Position(CMSComponentDefinition):
    x: int
    y: int
    z: int = 0

class Opacity(CMSComponentDefinition):
    value: int = 255
    
class Scale(CMSComponentDefinition):
    width: int
    height: int
    
class Rotation(CMSComponentDefinition):
    angle: int
    
class Flip(CMSComponentDefinition):
    horizontal: bool
    vertical: bool
    
class Visible(CMSComponentDefinition):
    value: bool

class Action(CMSComponentDefinition):
    state: str
    
class Center(CMSComponentDefinition):
    x_val: int
    y_val: int

class Rect(CMSComponentDefinition):
    rect: pygame.Rect
    
class LocalOffset(CMSComponentDefinition):
    x_val: int
    y_val: int
    
# tracks if image is scaled or rotated (affects rendering position)
class Tweaked(CMSComponentDefinition):
    value: bool

class Outline(CMSComponentDefinition):
    color: Tuple[int,int,int] | None


# physics entity
# --------------------------------------------------------------------------------------------------------------------
class Velocity(CMSComponentDefinition):
    x_val: int
    y_val: int
    
class Acceleration(CMSComponentDefinition):
    x_val: int
    y_val: int

class VelocityCaps(CMSComponentDefinition):
    x_val: int
    y_val: int
    
class Bounce(CMSComponentDefinition):
    val: int
    

# Assets
# -------------------------------------------------------------------------------------------------------------
 
class Path(CMSComponentDefinition):
    path: str | None

class Spritesheets(CMSComponentDefinition):
    value: Dict
 
class Images(CMSComponentDefinition):
    value: Dict

# other components
# -------------------------------------------------------------------------------------------------------------
class Health(CMSComponentDefinition):
    hp: int

class Energy(CMSComponentDefinition):
    value: int
    
class TestBehavior(CMSComponentDefinition):
    value: bool