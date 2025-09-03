import math
from rest import G

PARTICLE_FUNCS = {'behave': {}, 'init': {}}
ANIMATION_CACHE = {}

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
    self.acceleration[1] = 50  # Меньше гравитации
    self.velocity_caps[1] = 30  # Меньше максимальная скорость падения
    self.velocity_normalization[0] = 15  # Меньше сопротивление воздуха

@particle_behavior('walk_dust')
def walk_dust_behave(self, dt):
    # Очень слабое колебание
    self.pos[0] += math.sin(G.window.time * 0.8 + self.pos[0] * 0.1) * dt * 0.5