import pygame
import math
from rest import G
from rest.utils.cms import CMSEntity
from components.engine.object_base_components import *
from copy import copy

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
            'outline': Outline(color=None),
            'shadow': Shadow(),
            'shadow_anim': ShadowAnimationState()
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

        shadow_anim = self.get_component('shadow_anim')
        shadow_anim.current_radius = self.get_component('shadow').radius
        shadow_anim.target_radius = shadow_anim.current_radius

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
        pos = self.get_component('position')
        offset = self.get_component('offset_coords')
        specs = self.get_component('specs').data
        img_dims = self.render_image.get_size()

        center_shift = (img_dims[0] // 2, img_dims[1] // 2) if specs.get('centered', False) else (0, 0)
        render_x = int(pos.x + offset.x - center_shift[0] - camera_offset[0])
        render_y = int(pos.y + offset.y - center_shift[1] - camera_offset[1])
        return (render_x, render_y)

    def tick(self, delta):
        if self.source_type == 'sequences':
            self.sequence.update(delta)
            self.get_component('source_image').image = self.sequence.img

        shadow_anim = self.get_component('shadow_anim')
        state_value = self.get_component('state').value
        mirror = self.get_component('mirror')

        shadow_anim.target_radius = self.get_component('shadow').radius
        shadow_anim.target_x_off = 0.0
        shadow_anim.target_y_off = 0.0
        
        if 'rotate' in state_value:
            shadow_anim.target_radius -= 1
        
        if 'top' in state_value:
            shadow_anim.target_y_off -= 0.05
        elif 'down' in state_value:
            shadow_anim.target_y_off += 0.05
        elif 'right' in state_value:
            shadow_anim.target_x_off += 0.15 if not mirror.flip_x else -0.15

        shadow_anim.current_radius += (shadow_anim.target_radius - shadow_anim.current_radius) * shadow_anim.lerp_speed * delta
        shadow_anim.current_x_off += (shadow_anim.target_x_off - shadow_anim.current_x_off) * shadow_anim.lerp_speed * delta
        shadow_anim.current_y_off += (shadow_anim.target_y_off - shadow_anim.current_y_off) * shadow_anim.lerp_speed * delta

        if 'idle' in state_value and self.sequence:
            sequence_duration = 0.85
            shadow_anim.pulse_frequency = 1.0 / sequence_duration if sequence_duration > 0 else 1.6
            shadow_anim.pulse_phase += 2 * math.pi * shadow_anim.pulse_frequency * delta

    def draw(self, surface, camera_offset=(0, 0)):
        if self.get_component('show').visible:
            surface.blit(self.render_image, self.draw_position(camera_offset))

    def renderz(self, camera_offset=(0, 0), group='game'):
        if not self.get_component('show').visible:
            return
        
        pos = self.draw_position(camera_offset)
        shadow = self.get_component('shadow')
        shadow_anim = self.get_component('shadow_anim')

        if shadow.enabled:
            effective_radius = shadow_anim.current_radius
            if 'idle' in self.get_component('state').value:
                effective_radius += shadow_anim.pulse_amplitude * math.sin(shadow_anim.pulse_phase)
            shadow_surface = pygame.Surface((effective_radius * 2, effective_radius * 2), pygame.SRCALPHA)
            
            pygame.draw.ellipse(
                shadow_surface,
                shadow.color + (shadow.alpha,),
                (0, 0, effective_radius * 2, effective_radius)
            )
            resize = self.get_component('resize')
            adjusted_offset_x = (shadow.offset_x + shadow_anim.current_x_off) * resize.scale_x
            adjusted_offset_y = (shadow.offset_y + shadow_anim.current_y_off) * resize.scale_y
            radius_diff = effective_radius - shadow_anim.current_radius
            shadow_pos = (
                int(pos[0] + adjusted_offset_x - radius_diff),
                int(pos[1] + adjusted_offset_y - radius_diff)
            )
            
            G.window.blit(
                shadow_surface,
                shadow_pos,
                z=self.get_component('z').val - 0.0001,
            )

        outline = self.get_component('outline')
        if outline.color:
            outline = pygame.mask.from_surface(self.render_image).to_surface(
                setcolor=outline.color, unsetcolor=(0, 0, 0, 0))
            outline.set_alpha(self.get_component('transparency').alpha)
            for shift in ADJACENT_DIRS:
                G.window.blit(outline, (pos[0] + shift[0], pos[1] + shift[1]),
                              z=self.get_component('z').val - 0.000001)
                
        G.window.blit(self.render_image, pos, z=self.get_component('z').val)
