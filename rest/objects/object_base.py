import pygame
from rest import G

ADJACENT_DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Object:
   def __init__(self, position, depth=0):
       self.kind = getattr(self, 'kind', type)
       self.position = list(position)
       self.depth = depth

       asset_data = G.asset_library[self.kind]
       if asset_data is None:
           raise ValueError(f"No asset data found for kind '{self.kind}'")

       self.specs = asset_data.specs
       self.resources = asset_data.resources
       self.sequences = asset_data.sequences
       self.state = self.specs.get('initial', 'idle/down')

       if self.state in self.sequences:
           self.source_type = 'sequences'
           self.sequence = self.sequences[self.state].copy()
       else:
           if self.sequences:
               self.state = list(self.sequences.keys())[0]
               self.source_type = 'sequences'
               self.sequence = self.sequences[self.state].copy()
           else:
               raise ValueError(f"No sequences found for {self.kind}")

       self.dimensions = self.specs.get('size', [16, 16])
       self.transparency = 255
       self.resize = [1, 1]
       self.angle = 0
       self.mirror = [False, False]
       self.show = True
       self.modified = False
       self.highlight = None

   @property
   def center(self):
       return self.hitbox.center

   @property
   def hitbox(self):
       return pygame.Rect(*self.position, *self.dimensions)

   @property
   def offset_coords(self):
       res_offset = self.specs[self.source_type][self.state]['offset']
       obj_offset = self.specs['offset']
       return res_offset[0] + obj_offset[0], res_offset[1] + obj_offset[1]

   @property
   def source_image(self):
       if self.source_type == 'sequences':
           return self.sequence.img
       return None

   @property
   def render_image(self):
       src_img = self.source_image
       if src_img is None:
           placeholder = pygame.Surface(self.dimensions)
           placeholder.fill((255, 0, 255))
           return placeholder

       img = src_img
       orig_size = img.get_size()
       if self.resize != [1, 1]:
           img = pygame.transform.scale(img, (int(self.resize[0] * orig_size[0]),
                                              int(self.resize[1] * orig_size[1])))
           self.modified = True
       if any(self.mirror):
           img = pygame.transform.flip(img, self.mirror[0], self.mirror[1])
       if self.angle:
           img = pygame.transform.rotate(img, self.angle)
           self.modified = True
       if self.transparency != 255:
           if img == src_img:
               img = img.copy()
           img.set_alpha(self.transparency)
       return img

   def set_state(self, state, override=False):
       if not override and (self.state == state):
           return
       self.state = state
       self.source_type = 'sequences' if self.state in self.sequences else 'images'
       if self.source_type == 'sequences':
           self.sequence = self.sequences[self.state].copy()

   def draw_position(self, camera_offset=(0, 0)):
       img_dims = self.render_image.get_size()
       if (not self.modified) or self.specs['centered']:
           center_shift = (img_dims[0] // 2, img_dims[1] // 2) if self.specs['centered'] else (0, 0)
           return (self.position[0] - camera_offset[0] + self.offset_coords[0] - center_shift[0],
                   self.position[1] - camera_offset[1] + self.offset_coords[1] - center_shift[1])
       else:
           raw_dims = self.source_image.get_size()
           size_delta = (img_dims[0] - raw_dims[0], img_dims[1] - raw_dims[1])
           auto_shift = [-size_delta[0] // 2, -size_delta[1] // 2]
           return (self.position[0] - camera_offset[0] + self.offset_coords[0] + auto_shift[0],
                   self.position[1] - camera_offset[1] + self.offset_coords[1] + auto_shift[1])

   def tick(self, delta):
       if self.source_type == 'sequences':
           self.sequence.update(delta)

   def draw(self, surface, camera_offset=(0, 0)):
       if self.show:
           surface.blit(self.render_image, self.draw_position(camera_offset))

   def renderz(self, camera_offset=(0, 0), group='game'):
       if self.show:
           pos = self.draw_position(camera_offset)
           if self.highlight:
               outline = pygame.mask.from_surface(self.render_image).to_surface(setcolor=self.highlight,
                                                                                unsetcolor=(0, 0, 0, 0))
               outline.set_alpha(self.transparency)
               for shift in ADJACENT_DIRS:
                   G.renderer.blit(outline, (pos[0] + shift[0], pos[1] + shift[1]),
                                 z=self.depth - 0.000001)
           G.renderer.blit(self.render_image, pos, z=self.depth)


