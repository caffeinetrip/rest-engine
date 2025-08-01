import time
import pygame

class Window:
    def __init__(self, dimensions=(640, 480), caption='pygpen window', flags=0, fps_cap=60, dt_cap=1, frag_path=None):
        self.dimensions = dimensions
        self.caption = caption
        self.flags = flags | pygame.DOUBLEBUF | pygame.OPENGL
        self.fps_cap = fps_cap
        self.dt_cap = dt_cap
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

        pygame.init()
        pygame.display.set_caption(self.caption)
        self.screen = pygame.display.set_mode(self.dimensions, self.flags)
        self.clock = pygame.time.Clock()

        self.render_object = None
        self.initialized_opengl = False
        self.input_comp = None

    def initialize_opengl(self):
        if self.initialized_opengl:
            return False

        if self.frag_path:
            self.render_object = self.mgl.render_object(self.frag_path)
        else:
            self.render_object = self.mgl.default_ro()
        self.initialized_opengl = True
        return True


    @property
    def fps(self):
        return len(self.frame_log) / sum(self.frame_log) if self.frame_log else 0

    def cycle(self, uniforms):


        if not self.initialized_opengl:
            self.initialize_opengl()

        if self.render_object:
            shader_uniforms = uniforms.copy()
            shader_uniforms['time'] = self.dt
            shader_uniforms['tremor'] = self.tremor
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

        self.time = time.time()
        self.frames += 1
        self.runtime = self.time - self.start_time

    def _fallback_render(self, uniforms):
        self.screen.fill(self.background_color)

        if 'surface' in uniforms and uniforms['surface']:
            surface = uniforms['surface']
            self._render_scaled_surface(surface)

        if 'ui_surf' in uniforms and uniforms['ui_surf']:
            ui = uniforms['ui_surf']
            self._render_scaled_surface(ui)

    def _render_scaled_surface(self, surface):
        if surface.get_size() != self.screen.get_size():
            scale_x = self.screen.get_width() / surface.get_width()
            scale_y = self.screen.get_height() / surface.get_height()
            scale = min(scale_x, scale_y)
            scaled_width = int(surface.get_width() * scale)
            scaled_height = int(surface.get_height() * scale)

            scaled_surface = pygame.transform.scale(surface, (scaled_width, scaled_height))
            x = (self.screen.get_width() - scaled_width) // 2
            y = (self.screen.get_height() - scaled_height) // 2
            self.screen.blit(scaled_surface, (x, y))

        else:
            self.screen.blit(surface, (0, 0))