from .object_base import Object
from rest import G
from rest.utils.cms import CMSEntity
from components.engine.moving_object_components import *
from rest.utils.game_math import get_state_in_diapasone
import pygame

WALKABLE_TILES = ['walk_zone']

def apply_friction(value, amount):
    if abs(value) < amount:
        return 0
    return value - amount if value > 0 else value + amount

class MovingObject(CMSEntity):
    def __init__(self, entity_id, position=(0, 0), moving=True, z=0):
        super().__init__(entity_id)
        self.entity_id = entity_id
        self.object = Object(entity_id, position, z)
        
        self.components = self._initialize_components()
        if moving:
            self._register_input()

    def _initialize_components(self):
        return {
            'object': self.object,
            'prev_pos': PrevPos(x=0, y=0),
            'speed': Speed(x=0.0, y=0.0),
            'acceleration': Acceleration(x=0.0, y=0.0),
            'size': Size(width=16, height=16),
            'max_speed': MaxSpeed(x=70.0, y=70.0),
            'friction': Friction(x=0.0, y=0.0),
            'delta_move': DeltaMove(x=0.0, y=0.0),
            'prev_move': PrevMove(x=0.0, y=0.0),
            'rebound': Rebound(value=0.0),
            'auto_mirror': AutoMirror(value=0.0),
            'target_mirror': TargetMirror(value=False),
            'collision_list': CollisionList(value=[]),
            'collisions': Collisions(up=False, down=False, right=False, left=False),
            'pass_through': PassThrough(value=0.0),
            'no_collide': NoCollide(value=False),
            'walkable_only': WalkableOnly(value=True),
            'collision_offsets': CollisionOffsets(left=5, top=0, right=-8, bottom=-5),
            'direction': Direction(value='down'),
            'target_direction': TargetDirection(value='down'),
            'moving': Moving(value=False),
            'move_x': MoveX(value=0.0),
            'move_y': MoveY(value=0.0),
            'moving_processor': MovingProcessor(value=True),
            'last_vertical_state': LastVerticalState(state=None),
            'degrees': Degrees(value=0),
            'rotate_speed': RotationSpeed(value=18),
            'target_degrees': TargetDegrees(value=0)
        }

    @property
    def rebound_factors(self):
        rebound = self.get_component('rebound').value
        return tuple(rebound) if isinstance(rebound, (list, tuple)) else (rebound, rebound)

    @property
    def center(self):
        return self.rect.center

    @property
    def rect(self):
        pos = self.get_component('prev_pos')
        size = self.get_component('size')
        return pygame.Rect(pos.x, pos.y, size.width, size.height)

    def check_walkable_collision(self, new_position, level_map):
        if not self.get_component('walkable_only').value:
            return True
        
        world_width = level_map.dimensions[0] * level_map.tile_size[0]
        world_height = level_map.dimensions[1] * level_map.tile_size[1]
        offsets = self.get_component('collision_offsets')
        size = self.get_component('size')

        if (new_position[0] - offsets.left < 0 or
                new_position[0] + size.width + offsets.right > world_width or
                new_position[1] - offsets.top < 0 or
                new_position[1] + size.height + offsets.bottom > world_height):
            return False

        corners = [
            (new_position[0] - offsets.left, new_position[1] - offsets.top),
            (new_position[0] + size.width + offsets.right, new_position[1] - offsets.top),
            (new_position[0] - offsets.left, new_position[1] + size.height + offsets.bottom),
            (new_position[0] + size.width + offsets.right, new_position[1] + size.height + offsets.bottom),
            (new_position[0] + size.width // 2, new_position[1] + size.height // 2)
        ]

        for x, y in corners:
            
            grid_x, grid_y = int(x // level_map.tile_size[0]), int(y // level_map.tile_size[1])
            if (grid_x, grid_y) not in level_map.grid_tiles:
                return False
            
            if not any(tile.group in WALKABLE_TILES for tile in level_map.grid_tiles[(grid_x, grid_y)].values()):
                return False
            
        return True

    def _register_input(self):
        key_configs = [
            {'keys': [pygame.K_LEFT, pygame.K_a], 'x': -1, 'y': 0, 'direction': 'right', 'mirror': True},
            {'keys': [pygame.K_RIGHT, pygame.K_d], 'x': 1, 'y': 0, 'direction': 'right', 'mirror': False},
            {'keys': [pygame.K_UP, pygame.K_w], 'x': 0, 'y': -1, 'direction': 'top', 'mirror': False},
            {'keys': [pygame.K_DOWN, pygame.K_s], 'x': 0, 'y': 1, 'direction': 'down', 'mirror': False},
        ]

        for config in key_configs:
            
            event_data = {
                'x': config['x'], 'y': config['y'], 'direction': config['direction'],
                'mirror': config['mirror'], 'max_speed': [70, 70]
            }
            
            G.input.add_key_event('holding', config['keys'], 'move', event_data, self)
            G.input.add_key_event('released', config['keys'], 'move', {**event_data, 'x': 0, 'y': 0}, self)

    def behavior_update(self):
        self.get_component('move_x').value = 0
        self.get_component('move_y').value = 0

    def physics_update(self, level_map):
        delta = G.window.dt
        self.behavior_update()
        
        if self.get_component('degrees').value >= 360:
            self.get_component('degrees').value = 0
        
        if self.get_component('move_x').value != 0 and self.get_component('move_y').value != 0:
            self.get_component('max_speed').x, self.get_component('max_speed').y = (33, 33)

        delta_move = self.get_component('delta_move')
        auto_mirror = self.get_component('auto_mirror').value
        
        if delta_move.x * -auto_mirror > 0:
            self.get_component('object').get_component('mirror').flip_x = True
            
        elif delta_move.x * auto_mirror > 0:
            self.get_component('object').get_component('mirror').flip_x = False

        delta_move.x += self.get_component('speed').x * delta
        delta_move.y += self.get_component('speed').y * delta
        self.move_with_physics(delta_move, level_map)
        
        if 'rotate' in self.get_component('object').get_component('state').value:
            if G.input.holded_keys_count == 0:
                x = get_state_in_diapasone(self.get_component('degrees').value)
                self.get_component('object').set_state(x)
                self.get_component('direction').value = x.removeprefix('idle/')

        self.get_component('prev_move').x = delta_move.x / delta
        self.get_component('prev_move').y = delta_move.y / delta
        self.get_component('speed').x += self.get_component('acceleration').x * delta
        self.get_component('speed').y += self.get_component('acceleration').y * delta
        self.get_component('speed').x = apply_friction(self.get_component('speed').x, self.get_component('friction').x * delta)
        self.get_component('speed').y = apply_friction(self.get_component('speed').y, self.get_component('friction').y * delta)
        self.get_component('speed').x = max(-self.get_component('max_speed').x, min(self.get_component('max_speed').x, self.get_component('speed').x))
        self.get_component('speed').y = max(-self.get_component('max_speed').y, min(self.get_component('max_speed').y, self.get_component('speed').y))
        
        delta_move.x = delta_move.y = 0
        
        self.get_component('pass_through').value = max(0, self.get_component('pass_through').value - delta)

    def apply_impulse(self, vector):
        delta_move = self.get_component('delta_move')
        delta_move.x += vector[0] * G.window.dt
        delta_move.y += vector[1] * G.window.dt

    def move_with_physics(self, movement, level_map):
        collision_list = self.get_component('collision_list')
        prev_pos = self.get_component('prev_pos')
        collisions = self.get_component('collisions')
        obj_pos = self.get_component('object').get_component('position')

        collision_list.value = []
        prev_pos.x, prev_pos.y = obj_pos.x, obj_pos.y
        collisions.up = collisions.down = collisions.right = collisions.left = False

        if self.get_component('walkable_only').value:
            if movement.y != 0:
                test_pos_y = [obj_pos.x, obj_pos.y + movement.y]
                
                if self.check_walkable_collision(test_pos_y, level_map):
                    obj_pos.y += movement.y
                    
                else:
                    collisions.down = movement.y > 0
                    collisions.up = movement.y < 0
                    self.get_component('speed').y = 0
                    
            if movement.x != 0:
                
                test_pos_x = [obj_pos.x + movement.x, obj_pos.y]
                if self.check_walkable_collision(test_pos_x, level_map):
                    obj_pos.x += movement.x
                    
                else:
                    collisions.right = movement.x > 0
                    collisions.left = movement.x < 0
                    self.get_component('speed').x = 0
        else:
            
            obj_pos.y += movement.y
            tiles = level_map.nearby_grid_physics(self.center)
            self.handle_collisions((0, movement.y), tiles)
            
            obj_pos.x += movement.x
            tiles = level_map.nearby_grid_physics(self.center)
            self.handle_collisions((movement.x, 0), tiles)
