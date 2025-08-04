import pygame
from rest import G
from rest.utils.cms import CMSEntity
from components.engine.object_base_components import *

ADJACENT_DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Object(CMSEntity):
    def __init__(self, entity_id, position=(0, 0), z=0):
        super().__init__(entity_id)
        self.entity_id = entity_id
        asset_data = G.asset_library[entity_id]
        if not asset_data:
            raise ValueError(f"No asset data found for {entity_id}")

        specs = asset_data.specs
        size = specs.get('size', [16, 16])
        self.components = {
            'position': Position(x=position[0], y=position[1]),
            'z': Z(val=z),
            'specs': Specs(data=specs),
            'resources': Resources(data=asset_data.resources),
            'sequences': Sequences(data=asset_data.sequences),
            'state': State(value=specs.get('initial', 'idle/down')),
            'dimensions': Dimensions(width=size[0], height=size[1]),
            'transparency': Transparency(alpha=255),
            'resize': Resize(scale_x=1.0, scale_y=1.0),
            'angle': Angle(degrees=0.0),
            'mirror': Mirror(flip_x=False, flip_y=False),
            'show': Show(visible=True),
            'modified': Modified(changed=False),
            'outline': Outline(color=None)
        }

        sequences = self.get_component('sequences').data
        state = self.get_component('state').value
        self.source_type = 'sequences'
        self.sequence = sequences[state].copy() if state in sequences else sequences[list(sequences.keys())[0]].copy() if sequences else None
        if not self.sequence:
            raise ValueError(f"No sequences found for {entity_id}")

        self.add_component('hitbox', Hitbox(rect=self.hitbox))
        self.add_component('center', Center(x=self.center[0], y=self.center[1]))
        self.add_component('offset_coords', OffsetCoords(x=self.offset_coords[0], y=self.offset_coords[1]))
        self.add_component('source_image', SourceImage(image=self.source_image))
        self.add_component('render_image', RenderImage(image=self.render_image))

    @property
    def center(self):
        return self.get_component('hitbox').rect.center

    @property
    def hitbox(self):
        pos = self.get_component('position')
        dims = self.get_component('dimensions')
        return pygame.Rect(pos.x, pos.y, dims.width, dims.height)

    @property
    def offset_coords(self):
        specs = self.get_component('specs').data
        state = self.get_component('state').value
        res_offset = specs[self.source_type][state]['offset']
        obj_offset = specs['offset']
        return res_offset[0] + obj_offset[0], res_offset[1] + obj_offset[1]

    @property
    def source_image(self):
        return self.sequence.img if self.source_type == 'sequences' else None

    @property
    def render_image(self):
        src_img = self.get_component('source_image').image
        if not src_img:
            dims = self.get_component('dimensions')
            placeholder = pygame.Surface((dims.width, dims.height))
            placeholder.fill((255, 0, 255))
            return placeholder

        img = src_img
        orig_size = img.get_size()
        resize = self.get_component('resize')
        if resize.scale_x != 1.0 or resize.scale_y != 1.0:
            img = pygame.transform.scale(img, (int(resize.scale_x * orig_size[0]), int(resize.scale_y * orig_size[1])))
            self.get_component('modified').changed = True

        mirror = self.get_component('mirror')
        if mirror.flip_x or mirror.flip_y:
            img = pygame.transform.flip(img, mirror.flip_x, mirror.flip_y)

        angle = self.get_component('angle')
        if angle.degrees:
            img = pygame.transform.rotate(img, angle.degrees)
            self.get_component('modified').changed = True

        transparency = self.get_component('transparency')
        if transparency.alpha != 255:
            if img == src_img:
                img = img.copy()
                
            img.set_alpha(transparency.alpha)

        return img

    def set_state(self, state, override=False):
        if not override and self.get_component('state').value == state:
            return
        
        self.get_component('state').value = state
        sequences = self.get_component('sequences').data
        self.source_type = 'sequences' if state in sequences else 'images'
        
        if self.source_type == 'sequences':
            self.sequence = sequences[state].copy()
            self.get_component('source_image').image = self.sequence.img

    def draw_position(self, camera_offset=(0, 0)):
        img_dims = self.render_image.get_size()
        pos = self.get_component('position')
        offset = self.get_component('offset_coords')
        specs = self.get_component('specs').data
        modified = self.get_component('modified').changed

        if not modified or specs['centered']:
            
            center_shift = (img_dims[0] // 2, img_dims[1] // 2) if specs['centered'] else (0, 0)
            
            return (pos.x - camera_offset[0] + offset.x - center_shift[0],
                    pos.y - camera_offset[1] + offset.y - center_shift[1])
        
        raw_dims = self.get_component('source_image').image.get_size()
        size_delta = (img_dims[0] - raw_dims[0], img_dims[1] - raw_dims[1])
        auto_shift = (-size_delta[0] // 2, -size_delta[1] // 2)
        
        return (pos.x - camera_offset[0] + offset.x + auto_shift[0],
                pos.y - camera_offset[1] + offset.y + auto_shift[1])

    def tick(self, delta):
        if self.source_type == 'sequences':
            self.sequence.update(delta)
            self.get_component('source_image').image = self.sequence.img

    def draw(self, surface, camera_offset=(0, 0)):
        if self.get_component('show').visible:
            surface.blit(self.render_image, self.draw_position(camera_offset))

    def renderz(self, camera_offset=(0, 0), group='game'):
        if not self.get_component('show').visible:
            return
        
        pos = self.draw_position(camera_offset)
        outline = self.get_component('outline')
        
        if outline.color:
            
            outline = pygame.mask.from_surface(self.render_image).to_surface(
                setcolor=outline.color, unsetcolor=(0, 0, 0, 0))
            
            outline.set_alpha(self.get_component('transparency').alpha)
            
            for shift in ADJACENT_DIRS:
                G.window.blit(outline, (pos[0] + shift[0], pos[1] + shift[1]),
                               z=self.get_component('z').val - 0.000001)
                
        G.window.blit(self.render_image, pos, z=self.get_component('z').val)
