import pygame
from rest.objects.object_base import MovingObject
from rest import G

class PlayerEntity(MovingObject):
    def __init__(self, position):
        self.kind = 'player'
        super().__init__(position)
        self.walkable_only = True
        self.speed = [0, 0]
        self.max_speed = [80, 80]
        self.size = [16, 16]
        self.direction = 'down'
        self.moving = False
        self.mirror = [False, False]
        self.move_x = 0
        self.move_y = 0
        self.prev_move = [0, 0]

        self.register_input()

    def register_input(self):
        G.input.add_key_event('holding', [pygame.K_LEFT, pygame.K_a], 'move', {
            'x': -1, 'y': 0, 'direction': 'right', 'mirror': True, 'max_speed': [80, 80]
        }, self)

        G.input.add_key_event('holding', [pygame.K_RIGHT, pygame.K_d], 'move', {
            'x': 1, 'y': 0, 'direction': 'right', 'mirror': False, 'max_speed': [80, 80]
        }, self)

        G.input.add_key_event('holding', [pygame.K_UP, pygame.K_w], 'move', {
            'x': 0, 'y': -1, 'direction': 'top', 'mirror': False, 'max_speed': [80, 80]
        }, self)

        G.input.add_key_event('holding', [pygame.K_DOWN, pygame.K_s], 'move', {
            'x': 0, 'y': 1, 'direction': 'down', 'mirror': False, 'max_speed': [80, 80]
        }, self)

    def behavior_update(self):

        self.move_x = 0
        self.move_y = 0

        pass