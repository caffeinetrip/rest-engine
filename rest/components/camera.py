import pygame
from rest import G
from rest.utils.cms import CMSEntity
from typing import Tuple
from rest.utils.gfx import smooth_approach
from rest.utils.cms import CMSComponentDefinition
from typing import List, Tuple, Any

class CameraComponent(CMSComponentDefinition):
    size: Tuple[int, int]
    pos: List[float]
    slowness: float
    tilemap: Any = None
    int_pos: Tuple[int, int] = (0, 0)
    rect: pygame.Rect | None = None
    target_pos: Tuple[float, float] | None = None

class Camera(CMSEntity):
    def __init__(self, entity_id, size: Tuple[int, int], pos=(0, 0), slowness=1, tilemap=None):
        super().__init__(entity_id)

        self.components = {
            'camera': CameraComponent(size=size, pos=list(pos), slowness=slowness, tilemap=tilemap)
        }
        self.target_entity = None

    @property
    def offset(self):
        return self.components['camera'].int_pos

    def set_target(self, target):
        self.target_entity = target
        self.components['camera'].target_pos = None

    def update(self, dt):
        target = self.target_entity
        if self.target_entity:
            target = (
                self.target_entity.components['center'].x_val - self.components['camera'].size[0] // 2,
                self.target_entity.components['center'].y_val - self.components['camera'].size[1] // 2
            )
        if target:
            if self.components['camera'].tilemap:
                map_width = self.components['camera'].tilemap.dimensions[0] * self.components['camera'].tilemap.tile_size[0]
                map_height = self.components['camera'].tilemap.dimensions[1] * self.components['camera'].tilemap.tile_size[1]
                target = (
                    max(0, min(target[0], map_width - self.components['camera'].size[0])),
                    max(0, min(target[1], map_height - self.components['camera'].size[1]))
                )
            self.components['camera'].pos[0] = smooth_approach(self.components['camera'].pos[0], target[0], dt, slowness=self.components['camera'].slowness)
            self.components['camera'].pos[1] = smooth_approach(self.components['camera'].pos[1], target[1], dt, slowness=self.components['camera'].slowness)
        self.components['camera'].int_pos = (int(self.components['camera'].pos[0]), int(self.components['camera'].pos[1]))
        self.components['camera'].rect = pygame.Rect(
            self.components['camera'].pos[0] - 20, self.components['camera'].pos[1] - 20,
            self.components['camera'].size[0] + 40, self.components['camera'].size[1] + 40
        )
