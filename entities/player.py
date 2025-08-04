import pygame
from rest.objects.moving_object import MovingObject
from rest.utils.cms import CMSEntity
from rest import G

class PlayerEntity(CMSEntity):
    def __init__(self, position):
        super().__init__(entity_id='player')

        self.components = {
            'object': MovingObject(self.entity_id, position)
        }
