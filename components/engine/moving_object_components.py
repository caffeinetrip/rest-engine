from rest.utils.cms import CMSComponentDefinition
from typing import List


class PrevPos(CMSComponentDefinition):
    x: int
    y: int

class Speed(CMSComponentDefinition):
    x: float
    y: float

class Acceleration(CMSComponentDefinition):
    x: float
    y: float

class Size(CMSComponentDefinition):
    width: int
    height: int

class MaxSpeed(CMSComponentDefinition):
    x: float
    y: float

class Friction(CMSComponentDefinition):
    x: float
    y: float

class DeltaMove(CMSComponentDefinition):
    x: float
    y: float

class PrevMove(CMSComponentDefinition):
    x: float
    y: float

class Rebound(CMSComponentDefinition):
    value: float

class AutoMirror(CMSComponentDefinition):
    value: float

class CollisionList(CMSComponentDefinition):
    value: List

class Collisions(CMSComponentDefinition):
    up: bool
    down: bool
    right: bool
    left: bool

class PassThrough(CMSComponentDefinition):
    value: float

class NoCollide(CMSComponentDefinition):
    value: bool

class WalkableOnly(CMSComponentDefinition):
    value: bool

class CollisionOffsets(CMSComponentDefinition):
    left: int
    top: int
    right: int
    bottom: int

class Direction(CMSComponentDefinition):
    value: str

class Moving(CMSComponentDefinition):
    value: bool

class MoveX(CMSComponentDefinition):
    value: float

class MoveY(CMSComponentDefinition):
    value: float

class MovingProcessor(CMSComponentDefinition):
    value: bool
