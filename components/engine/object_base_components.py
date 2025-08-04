from rest.utils.cms import CMSComponentDefinition
from typing import  Dict, Any, Optional, Tuple

import pygame

class Position(CMSComponentDefinition):
    x: int
    y: int

class Depth(CMSComponentDefinition):
    val: int

class Specs(CMSComponentDefinition):
    data: Dict[str, Any]

class Resources(CMSComponentDefinition):
    data: Dict[str, Any]

class Sequences(CMSComponentDefinition):
    data: Dict[str, Any]

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

class Highlight(CMSComponentDefinition):
    color: Optional[Tuple[int, int, int]]

class Center(CMSComponentDefinition):
    x: int
    y: int
    
class Hitbox(CMSComponentDefinition):
    rect: pygame.Rect

class OffsetCoords(CMSComponentDefinition):
    x: int
    y: int

class SourceImage(CMSComponentDefinition):
    image: Optional[pygame.Surface]

class RenderImage(CMSComponentDefinition):
    image: pygame.Surface