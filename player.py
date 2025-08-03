import pygame
from rest.objects.moving_object import MovingObject
from rest import G

class PlayerEntity(MovingObject):
    def __init__(self, position):
        self.kind = 'player'
        super().__init__(position)
        self.walkable_only = True