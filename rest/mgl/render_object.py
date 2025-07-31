# rest/mgl/render_object.py
import moderngl
import pygame
from ..utils.io import read_f

class RenderObject:
    def __init__(self, mgl, frag_shader, vert_shader=None, default_ro=False, vao_args=['2f 2f', 'vert', 'texcoord'], buffer=None):
        self.mgl = mgl
        
        if not vert_shader:
            vert_shader = mgl.default_vert
            
        self.default = default_ro
        
        self.frag_raw = frag_shader
        self.vert_raw = vert_shader
        
        self.vao_args = vao_args
        
        self.program = mgl.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        
        if not buffer:
            buffer = mgl.quad_buffer
            
        self.vao = mgl.ctx.vertex_array(self.program, [(buffer, *vao_args)])
        
        self.temp_textures = []

    def update(self, uniforms={}):
        tex_id = 0
        uniform_list = list(self.program)
        for uniform in uniforms:
            if uniform in uniform_list:
                if isinstance(uniforms[uniform], moderngl.Texture):
                    uniforms[uniform].use(tex_id)
                    self.program[uniform].value = tex_id
                    tex_id += 1
                else:
                    self.program[uniform].value = uniforms[uniform]

    def parse_uniforms(self, uniforms):
        for name, value in uniforms.items():
            if isinstance(value, pygame.Surface):
                tex = self.mgl.pg2tx(value)
                uniforms[name] = tex
                self.temp_textures.append(tex)
        return uniforms

    def render(self, dest=None, uniforms={}):
        if not dest:
            dest = self.mgl.ctx.screen
            
        dest.use()
        
        uniforms = self.parse_uniforms(uniforms)
        self.update(uniforms=uniforms)
        self.vao.render(mode=moderngl.TRIANGLE_STRIP)

        for tex in self.temp_textures:
            tex.release()
            
        self.temp_textures = []
