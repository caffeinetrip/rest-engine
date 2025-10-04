from rest.utils.cms import CMSComponentDefinition
from typing import Optional, Tuple, List
import pygame

class Shadow(CMSComponentDefinition):
    enabled: bool = True
    radius: float = 6.5
    offset_x: float = 1.9
    offset_y: int = 12
    alpha: int = 20
    color: tuple = (0, 0, 0)

class ShadowAnimationState(CMSComponentDefinition):
    current_radius: float = 6.5
    current_x_off: float = 0.0
    current_y_off: float = 0.0
    target_radius: float = 6.5
    target_x_off: float = 0.0
    target_y_off: float = 0.0
    lerp_speed: float = 15.0
    pulse_phase: float = 0
    pulse_amplitude: float = 0.005
    pulse_frequency: float = 1.0
    
class Position(CMSComponentDefinition):
    x: int
    y: int

class Z(CMSComponentDefinition):
    val: int

class Specs(CMSComponentDefinition):
    data: dict

class Resources(CMSComponentDefinition):
    data: dict

class Sequences(CMSComponentDefinition):
    data: dict

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
    
class DrawPosition(CMSComponentDefinition):
    x: int
    y: int