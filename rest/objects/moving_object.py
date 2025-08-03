from .object_base import Object
from rest import G
import pygame

WALKABLE_TILES = [
    'walk_zone',
]

def apply_friction(value, amount):
    if abs(value) < amount:
        return 0
    elif value > 0:
        return value - amount
    else:
        return value + amount

class MovingObject(Object):
    def __init__(self, position, moving=True, depth=0):
        super().__init__(position, depth=depth)
        self.prev_pos = (0, 0)
        self.speed = [0, 0]
        self.acceleration = [0, 0]
        self.size = [16, 16]
        self.max_speed = [70, 70]
        self.friction = [0, 0]
        self.delta_move = [0, 0]
        self.prev_move = [0, 0]
        self.rebound = 0
        self.auto_mirror = 0
        self.collision_list = []
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.pass_through = 0
        self.no_collide = False
        self.walkable_only = True
        self.collision_offsets = [5, 0, -8, -5]
        self.direction = 'down'
        self.moving = False
        self.mirror = [False, False]
        self.move_x = 0
        self.move_y = 0
        self.moving_proccesor = moving
        
        if moving:
            self.register_input()
        
        self.initialize()

    @property
    def rebound_factors(self):
        if type(self.rebound) not in {list, tuple}:
            return self.rebound, self.rebound
        return tuple(self.rebound)

    @property
    def center(self):
        return self.rect.center

    @property
    def rect(self):
        return pygame.Rect(*self.prev_pos, *self.size)

    def initialize(self):
        pass

    def check_walkable_collision(self, new_position, level_map):
        if not self.walkable_only:
            return True
        world_width = level_map.dimensions[0] * level_map.tile_size[0]
        world_height = level_map.dimensions[1] * level_map.tile_size[1]
        left_offset, top_offset, right_offset, bottom_offset = self.collision_offsets
        if (new_position[0] - left_offset < 0 or
                new_position[0] + self.size[0] + right_offset > world_width):
            return False
        if (new_position[1] - top_offset < 0 or
                new_position[1] + self.size[1] + bottom_offset > world_height):
            return False
        corners = [
            (new_position[0] - left_offset, new_position[1] - top_offset),
            (new_position[0] + self.size[0] + right_offset, new_position[1] - top_offset),
            (new_position[0] - left_offset, new_position[1] + self.size[1] + bottom_offset),
            (new_position[0] + self.size[0] + right_offset, new_position[1] + self.size[1] + bottom_offset)
        ]
        center = (new_position[0] + self.size[0] // 2, new_position[1] + self.size[1] // 2)
        corners.append(center)
        for corner in corners:
            grid_x = int(corner[0] // level_map.tile_size[0])
            grid_y = int(corner[1] // level_map.tile_size[1])
            if (grid_x, grid_y) in level_map.grid_tiles:
                found_walkable = False
                for layer, tile in level_map.grid_tiles[(grid_x, grid_y)].items():
                    if tile.group in WALKABLE_TILES:
                        found_walkable = True
                        break
                if not found_walkable:
                    return False
            else:
                return False
        return True

    def register_input(self):
        key_configs = [
            {'keys': [pygame.K_LEFT, pygame.K_a], 'x': -1, 'y': 0, 'direction': 'right', 'mirror': True},
            {'keys': [pygame.K_RIGHT, pygame.K_d], 'x': 1, 'y': 0, 'direction': 'right', 'mirror': False},
            {'keys': [pygame.K_UP, pygame.K_w], 'x': 0, 'y': -1, 'direction': 'top', 'mirror': False},
            {'keys': [pygame.K_DOWN, pygame.K_s], 'x': 0, 'y': 1, 'direction': 'down', 'mirror': False},
        ]

        for config in key_configs:

            G.input.add_key_event('holding', config['keys'], 'move', {
                'x': config['x'], 'y': config['y'], 'direction': config['direction'],
                'mirror': config['mirror'], 'max_speed': [70, 70]
            }, self)

            G.input.add_key_event('released', config['keys'], 'move', {
                'x': 0, 'y': 0, 'direction': config['direction'],
                'mirror': config['mirror'], 'max_speed': [70, 70]
            }, self)

    def behavior_update(self):
        
        self.move_x = 0
        self.move_y = 0


    def physics_update(self, level_map):
        delta = G.window.dt
        self.behavior_update()
        if self.delta_move[0] * -self.auto_mirror > 0:
            self.mirror[0] = True
        if self.delta_move[0] * self.auto_mirror > 0:
            self.mirror[0] = False
        self.delta_move[0] += self.speed[0] * delta
        self.delta_move[1] += self.speed[1] * delta
        self.move_with_physics(self.delta_move, level_map)
        self.prev_move = (self.delta_move[0] / delta, self.delta_move[1] / delta)
        self.speed[0] += self.acceleration[0] * delta
        self.speed[1] += self.acceleration[1] * delta
        self.speed[0] = apply_friction(self.speed[0], self.friction[0] * delta)
        self.speed[1] = apply_friction(self.speed[1], self.friction[1] * delta)
        self.speed[0] = max(-self.max_speed[0], min(self.max_speed[0], self.speed[0]))
        self.speed[1] = max(-self.max_speed[1], min(self.max_speed[1], self.speed[1]))
        self.delta_move = [0, 0]
        self.pass_through = max(0, self.pass_through - delta)

    def apply_impulse(self, vector):
        self.delta_move[0] += vector[0] * G.window.dt
        self.delta_move[1] += vector[1] * G.window.dt

    def move_with_physics(self, movement, level_map):
        self.collision_list = []
        self.prev_pos = tuple(self.position)
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        if self.walkable_only:
            if movement[1] != 0:
                test_pos_y = [self.position[0], self.position[1] + movement[1]]
                if self.check_walkable_collision(test_pos_y, level_map):
                    self.position[1] += movement[1]
                else:
                    self.collisions['down' if movement[1] > 0 else 'up'] = True
                    self.speed[1] = 0
            if movement[0] != 0:
                test_pos_x = [self.position[0] + movement[0], self.position[1]]
                if self.check_walkable_collision(test_pos_x, level_map):
                    self.position[0] += movement[0]
                else:
                    self.collisions['right' if movement[0] > 0 else 'left'] = True
                    self.speed[0] = 0
        else:
            self.position[1] += movement[1]
            tiles = level_map.nearby_grid_physics(self.center)
            self.handle_collisions((0, movement[1]), tiles)
            self.position[0] += movement[0]
            tiles = level_map.nearby_grid_physics(self.center)
            self.handle_collisions((movement[0], 0), tiles)
