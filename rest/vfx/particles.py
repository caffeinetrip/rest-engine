from rest.vfx.particles_func import PARTICLE_FUNCS, ANIMATION_CACHE
from rest.utils.game_math import normalize
from rest.utils.gfx import palette_swap
from rest import G
import random
import pygame

class Particle:
    def __init__(self, pos, particle_type, velocity=(0, 0), decay_rate=1.0, advance=0.0, behavior='idle', colors=None, z=0, physics_source=None):
        super().__init__()
        particle_types = ['particles'] if particle_type == 'particles' else [particle_type]
        self.type = random.choice(particle_types)
        self.behavior = behavior
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.acceleration = [0, 0]
        self.velocity_caps = [99999, 99999]
        self.velocity_normalization = [0, 0]
        self.next_movement = [0, 0]
        self.bounce = 0.5
        self.decay_rate = decay_rate
        self.advance = advance
        self.physics_source = physics_source
        self.z = z
        self.own_offset = [1, 6]
        
        self.lifetime = 0.0
        self.max_lifetime = random.uniform(0.4, 0.6)
        self.fade_duration = 0.4
        self.fade_start_time = self.max_lifetime - self.fade_duration
        self.alpha = 150
        self.should_remove = False
        
        self.scale = random.uniform(0.1, 0.2)
        
        asset = G.asset_library[self.type]
        
        self.animation = asset.sequences[self.type].copy()
        
        self.animation_speed = random.uniform(0.8, 1.2)
        self.animation.frame_index = 0
        self.animation.timer = 0
        
        self.colors = colors
        if colors:
            colors_id = (self.type, tuple((tuple(k), tuple(v)) for k, v in colors.items()))
            if colors_id in ANIMATION_CACHE:
                self.animation = ANIMATION_CACHE[colors_id]
            else:
                self.animation = self.animation.hard_copy()
                self.animation.images = [palette_swap(img, colors) for img in self.animation.images]
                self.animation.frame_index = 0
                self.animation.timer = 0
                ANIMATION_CACHE[colors_id] = self.animation
        
        self.animation.update(advance)
        PARTICLE_FUNCS['init'][behavior](self)

    def update(self, dt=None):
        if not dt:
            dt = G.window.dt

        self.lifetime += dt

        if self.lifetime >= self.max_lifetime:
            self.should_remove = True
            return True

        if self.lifetime > self.fade_start_time:
            fade_progress = (self.lifetime - self.fade_start_time) / self.fade_duration
            fade_progress = min(1.0, max(0.0, fade_progress))
            self.alpha = int(150 * (1.0 - fade_progress))
        else:
            fade_in_duration = 0.05
            if self.lifetime < fade_in_duration:
                fade_in_progress = self.lifetime / fade_in_duration
                self.alpha = int(150 * fade_in_progress)
            else:
                self.alpha = 150

        PARTICLE_FUNCS['behave'][self.behavior](self, dt)

        self.next_movement[0] += self.velocity[0] * dt
        self.next_movement[1] += self.velocity[1] * dt
        self.pos[0] += self.next_movement[0]

        if self.physics_source:
            collision = self.physics_source.physics_gridtile(self.pos)
            if collision and (collision.physics_type == 'solid'):
                self.velocity[0] *= -self.bounce
                if self.next_movement[0] > 0:
                    self.pos[0] = collision.rect.left
                if self.next_movement[0] < 0:
                    self.pos[0] = collision.rect.right

        self.pos[1] += self.next_movement[1]

        if self.physics_source:
            collision = self.physics_source.physics_gridtile(self.pos)
            if collision and (collision.physics_type == 'solid'):
                self.velocity[1] *= -self.bounce
                if self.next_movement[1] > 0:
                    self.pos[1] = collision.rect.top
                if self.next_movement[1] < 0:
                    self.pos[1] = collision.rect.bottom

        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt
        self.velocity[0] = normalize(self.velocity[0], self.velocity_normalization[0] * dt)
        self.velocity[1] = normalize(self.velocity[1], self.velocity_normalization[1] * dt)
        self.velocity[0] = max(-self.velocity_caps[0], min(self.velocity_caps[0], self.velocity[0]))
        self.velocity[1] = max(-self.velocity_caps[1], min(self.velocity_caps[1], self.velocity[1]))
        self.next_movement = [0, 0]

        return False

    def render(self, surf, offset=(0, 0)):
        if self.should_remove or self.alpha <= 0:
            return

        img = self.animation.img.copy()

        if self.scale != 1.0:
            original_size = img.get_size()
            new_size = (max(1, int(original_size[0] * self.scale)), max(1, int(original_size[1] * self.scale)))
            img = pygame.transform.scale(img, new_size)

        if self.alpha < 150:
            img.set_alpha(self.alpha)

        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))

    def renderz(self, camera_offset=(0, 0), group='default'):
        if self.should_remove or self.alpha <= 0:
            return

        img = self.animation.img

        if self.scale != 1.0:
            original_size = img.get_size()
            new_size = (max(1, int(original_size[0] * self.scale)), max(1, int(original_size[1] * self.scale)))
            img = pygame.transform.scale(img, new_size)

        if self.alpha < 150:
            img = img.copy()
            img.set_alpha(self.alpha)

        render_pos = (
            int(self.pos[0] - camera_offset[0] - img.get_width() // 2 - self.own_offset[0]),
            int(self.pos[1] - camera_offset[1] - self.own_offset[1])
        )
        
        G.window.blit(img, render_pos, z=self.z, group=group)