import pygame
from rest.utils.cms import CMSEntity
from components.cms_components import Position, Action, Opacity, Scale, Rotation, Flip, Visible, Tweaked, Outline, Center, Rect, LocalOffset

class BasicObject(CMSEntity):
    def __init__(self, entity_id, pos, z=0):
        super().__init__(entity_id)
        
        self.components = {
            'pos': Position(list(pos)[0], list(pos)[1], z),
            # 'config': None,
            # 'assets': None,
            # 'source': None,
            # 'animation': None,
            # 'size': None,
            'opacity': Opacity(255),
            'scale': Scale(1, 1),
            'rotation': Rotation(0),
            'flip': Flip(False, False),
            'visible': Visible(True),
            'tweaked': Tweaked(False),
            'outline': Outline(None),
            # 'rect': Rect(),
            # 'center': Center(),
            # 'local_offset': LocalOffset()
            # 'img': None,
            # 'raw_img': None
        }