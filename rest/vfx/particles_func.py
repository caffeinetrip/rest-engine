import math
from rest import G
import random

PARTICLE_FUNCS = {'behave': {}, 'init': {}} # type: ignore
ANIMATION_CACHE = {} # type: ignore
 
def particle_init(argument):
    def decorator(func):
        PARTICLE_FUNCS['init'][argument] = func
        return func
    return decorator

def particle_behavior(argument):
    def decorator(func):
        PARTICLE_FUNCS['behave'][argument] = func
        return func
    return decorator

@particle_init('walk_dust')
def walk_dust_init(self):
    self.acceleration[1] = 20
    self.velocity_caps[1] = 15
    self.velocity_normalization[0] = 10

@particle_behavior('walk_dust')
def walk_dust_behave(self, dt):
    wind_x = 2.0
    self.velocity[0] += wind_x * dt
    
    self.pos[0] += math.sin(G.window.time * random.uniform(0.6, 1.0) + self.pos[0] * random.uniform(0.05, 0.15)) * dt * 0.3
    self.pos[1] += math.cos(G.window.time * random.uniform(0.6, 1.0) + self.pos[1] * random.uniform(0.05, 0.15)) * dt * 0.2