from rest.utils.cms import CMSComponentDefinition
from dataclasses import dataclass
import pygame
from typing import Tuple, Dict

# engine components (doesn't delete)

# entity
# --------------------------------------------------------------------------------------------------------------------

@dataclass
class Position(CMSComponentDefinition):
    x: int
    y: int
    z: int = 0

@dataclass
class Opacity(CMSComponentDefinition):
    value: int = 255
    
@dataclass
class Scale(CMSComponentDefinition):
    width: int
    height: int
    
@dataclass
class Rotation(CMSComponentDefinition):
    angle: int
    
@dataclass
class Flip(CMSComponentDefinition):
    horizontal: bool
    vertical: bool
    
@dataclass
class Visible(CMSComponentDefinition):
    value: bool

@dataclass
class Action(CMSComponentDefinition):
    state: str
    
@dataclass
class Center(CMSComponentDefinition):
    x_val: int
    y_val: int

@dataclass
class Rect(CMSComponentDefinition):
    rect: pygame.Rect
    
@dataclass
class LocalOffset(CMSComponentDefinition):
    x_val: int
    y_val: int
    
# tracks if image is scaled or rotated (affects rendering position)
@dataclass
class Tweaked(CMSComponentDefinition):
    value: bool

@dataclass
class Outline(CMSComponentDefinition):
    color: Tuple[int,int,int] | None

# @dataclass
# class Config(CMSComponentDefinition):

    
# @dataclass
# class Assets(CMSComponentDefinition):

    
# @dataclass
# class Animations(CMSComponentDefinition):
    
    
# @dataclass
# class Source(CMSComponentDefinition):

    
# @dataclass
# class Img(CMSComponentDefinition):

    
# @dataclass
# class RawImg(CMSComponentDefinition):

# physics entity
# --------------------------------------------------------------------------------------------------------------------
@dataclass
class Velocity(CMSComponentDefinition):
    x_val: int
    y_val: int
    
@dataclass
class Acceleration(CMSComponentDefinition):
    x_val: int
    y_val: int

@dataclass
class VelocityCaps(CMSComponentDefinition):
    x_val: int
    y_val: int
    
@dataclass
class Bounce(CMSComponentDefinition):
    val: int

# Assets
# -------------------------------------------------------------------------------------------------------------

@dataclass 
class Path(CMSComponentDefinition):
    path: str | None

@dataclass
class Spritesheets(CMSComponentDefinition):
    value: Dict[str, dict]

@dataclass 
class Images(CMSComponentDefinition):
    value: Dict

# other components
# -------------------------------------------------------------------------------------------------------------
@dataclass
class Health(CMSComponentDefinition):
    hp: int

@dataclass
class Energy(CMSComponentDefinition):
    value: int
    
@dataclass
class TestBehavior(CMSComponentDefinition):
    value: bool