from rest.utils.cms import CMSComponentDefinition
from typing import Optional, Tuple, Dict
import pygame

class Position(CMSComponentDefinition):
    x: float
    y: float

class Velocity(CMSComponentDefinition):
    x: float
    y: float

class Z(CMSComponentDefinition):
    val: float

class Specs(CMSComponentDefinition):
    data: Dict

class Resources(CMSComponentDefinition):
    data: Dict

class Sequences(CMSComponentDefinition):
    data: Dict

class State(CMSComponentDefinition):
    value: str

class Dimensions(CMSComponentDefinition):
    width: int
    height: int

class Transparency(CMSComponentDefinition):
    alpha: int

class Resize(CMSComponentDefinition):
    scale_x: float
    scale_y: float

class Angle(CMSComponentDefinition):
    degrees: float

class Mirror(CMSComponentDefinition):
    flip_x: bool
    flip_y: bool

class Show(CMSComponentDefinition):
    visible: bool

class Modified(CMSComponentDefinition):
    changed: bool

class Outline(CMSComponentDefinition):
    color: Optional[Tuple[int, int, int]]

class Advance(CMSComponentDefinition):
    value: float

class DecayRate(CMSComponentDefinition):
    value: float

class Colors(CMSComponentDefinition):
    data: Optional[Dict[Tuple[int, int, int], Tuple[int, int, int]]]

class Behavior(CMSComponentDefinition):
    value: Optional[str]

class Hitbox(CMSComponentDefinition):
    rect: pygame.Rect

class Center(CMSComponentDefinition):
    x: float
    y: float

class OffsetCoords(CMSComponentDefinition):
    x: float
    y: float

class SourceImage(CMSComponentDefinition):
    image: Optional[pygame.Surface]

class RenderImage(CMSComponentDefinition):
    image: pygame.Surface