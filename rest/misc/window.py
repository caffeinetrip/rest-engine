import time
import pygame
from ..mgl.mgl import MGL

class Window:
    def __init__(self, dimensions=(640, 480), caption='Window', flags=0, fps_cap=60, dt_cap=1, frag_path=None):
        
        self.frag_path = frag_path
        
        self.dimensions = dimensions
        
        self.flags = flags | pygame.DOUBLEBUF | pygame.OPENGL
        
        self.fps_cap = fps_cap
        self.dt_cap = dt_cap
        
        self.background_color = (255, 255, 255)
        
        self.time = time.time()
        self.start_time = time.time()
        self.runtime_ = self.time - self.start_time
        
        self.frames = 0
        self.frame_log = []
        
        pygame.init()
        pygame.display.set_caption(caption)
        
        self.screen = pygame.display.set_mode(self.dimensions, self.flags)
        self.clock = pygame.time.Clock()
        
        self.last_frame = time.time()
        
        self.dt = 0.1

    @property
    def fps(self):
        return len(self.frame_log) / sum(self.frame_log) if self.frame_log else 0
    
    def load_mgl(self):
        
        if not self.frag_path:
            self.render_object = self.mgl.default_ro()
            
        else:
            self.render_object = self.mgl.render_object(self.frag_path)

    def cycle(self, uniforms={}):
        
        if self.render_object.default and 'surface' not in uniforms:
            uniforms['surface'] = self.screen
            uniforms['time'] = self.dt
            
        self.render_object.render(uniforms=uniforms)
        pygame.display.flip()
        
        self.clock.tick(self.fps_cap)
        self.dt = min(time.time() - self.last_frame, self.dt_cap)
        
        self.frame_log.append(self.dt)
        self.frame_log = self.frame_log[-60:]
    
        self.last_frame = time.time()
        self.time = time.time()
        self.runtime_ = self.time - self.start_time
        
        self.screen.fill(self.background_color)
        
        self.frames += 1
        
