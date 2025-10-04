import pygame
import time

class Window:
    def __init__(self, dimensions=(800, 600), display_size=(340, 220), caption='pygpen window', flags=0, fps_cap=60, frag_path=None, screens=['default']):
        self.dimensions = dimensions
        self.display_size = display_size
        
        self.caption = caption
        
        self.flags = flags | pygame.DOUBLEBUF | pygame.OPENGL
        
        self.fps_cap = fps_cap
        self.dt_cap = 1
        
        self.frag_path = frag_path
        
        self.background_color = (0, 0, 0)
        
        self.mgl = None
        
        self.start_time = time.time()
        self.time = self.start_time
        self.runtime = 0
        
        self.frames = 0
        self.frame_log = []
        self.last_frame = self.start_time
        
        self.dt = 0.1
        
        self.tremor = 0
        
        # Initialize render queue
        self.render_queue = {name: [] for name in screens}
        self.render_order = screens
        self.render_count = 0
        self.i = 0
        
        pygame.init()
        pygame.display.set_caption(caption)
        
        self.screen = pygame.display.set_mode(dimensions, self.flags)
        self.clock = pygame.time.Clock()
        self.render_object = None
        
        self.initialized_opengl = False
        self.surfaces = {name: pygame.Surface(display_size, pygame.SRCALPHA) for name in screens}

    def add_surfaces(self, surfs):
        self.surfaces.update({name: surf for name, surf in surfs.items() if name not in self.render_order})
        self.render_order.extend(name for name in surfs if name not in self.render_order)
    
        for name in surfs:
            if name not in self.render_queue:
                self.render_queue[name] = []

    def blit(self, surface, pos, z=0, group='default'):
        if group in self.surfaces:
            self.render_queue[group].append((z, self.i, surface, pos))
            self.i += 1

    def renderf(self, func, *args, **kwargs):
        z = kwargs.pop('z', 0)
        group = kwargs.pop('group', 'default')
        if group in self.surfaces:
            self.render_queue[group].append((z, self.i, func, args, kwargs))
            self.i += 1

    def draw_rect(self, rect, color=(255, 0, 0), group='default'):
        pygame.draw.rect(self.surfaces.get(group, self.surfaces['default']), color, rect)

    def initialize_opengl(self):
        if self.initialized_opengl:
            return False
        self.render_object = self.mgl.render_object(self.frag_path) if self.frag_path else self.mgl.default_ro()
        self.initialized_opengl = True
        return True

    @property
    def fps(self):
        return len(self.frame_log) / sum(self.frame_log) if self.frame_log else 0

    def cycle(self):
        if not self.initialized_opengl:
            self.initialize_opengl()
            
        uniforms = {
            'surface': self.surfaces.get('default', pygame.Surface((1, 1))),
            'bg_surf': self.surfaces.get('background', pygame.Surface((1, 1))),
            'ui_surf': self.surfaces.get('ui', pygame.Surface((1, 1)))
        }
        
        shader_uniforms = uniforms.copy()
        
        shader_uniforms.update({
            'time': self.dt,
            'tremor': self.tremor
        })
        
        self.render_count = 0
        for group in self.render_order:
            if group in self.render_queue:
                self.render_queue[group].sort()
                self.render_count += len(self.render_queue[group])
                for item in self.render_queue[group]:
                    if len(item) > 4:
                        item[2](self.surfaces[group], *item[3], **item[4])
                    else:
                        if item[0] != 107:
                            self.surfaces[group].blit(item[2], item[3])
                        else:
                            self.surfaces[group].blit(item[2], item[3], special_flags=pygame.BLEND_RGBA_ADD)
        
        if self.render_object:
            self.render_object.render(uniforms=shader_uniforms)
        else:
            self._fallback_render(uniforms)
            
        pygame.display.flip()
        
        self.clock.tick(self.fps_cap)
        self.dt = min(time.time() - self.last_frame, self.dt_cap)
        
        self.frame_log.append(self.dt)
        self.frame_log = self.frame_log[-60:]
        self.last_frame = time.time()
        self.mgl.ctx.clear(*[self.background_color[i] / 255 for i in range(3)], 1.0)
    
        self.time = self.last_frame
        self.frames += 1
        self.runtime = self.time - self.start_time
        
        for name in self.surfaces:
            self.surfaces[name].fill((0, 0, 0, 0))
        self.render_queue = {name: [] for name in self.render_order}
        self.i = 0

    def _fallback_render(self, uniforms):
        self.screen.fill(self.background_color)
        for key in ('surface', 'ui_surf'):
            if key in uniforms and uniforms[key]:
                self._render_scaled_surface(uniforms[key])

    def _render_scaled_surface(self, surface):
        if surface.get_size() != self.screen.get_size():
            scale = min(self.screen.get_width() / surface.get_width(), self.screen.get_height() / surface.get_height())
            scaled_surface = pygame.transform.scale(surface, (int(surface.get_width() * scale), int(surface.get_height() * scale)))
            self.screen.blit(scaled_surface, (
                (self.screen.get_width() - scaled_surface.get_width()) // 2,
                (self.screen.get_height() - scaled_surface.get_height()) // 2
            ))
        else:
            self.screen.blit(surface, (0, 0))