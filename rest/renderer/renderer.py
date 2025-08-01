from rest import G

class Renderer:
    def __init__(self):
        self.surfaces = {}
        self.render_order = []

    def add_surfaces(self, surfs):
        
        for name, surf in surfs.items():
            self.surfaces[name] = surf
            if name not in self.render_order:
                self.render_order.append(name)

    def set_render_order(self, order):
        self.render_order = order

    def get_surface(self, name):
        return self.surfaces.get(name)

    def cycle(self, surfaces={}):
        for name, surface in surfaces.items():
            self.surfaces[name] = surface


        # window_comp = G.window
        # if window_comp and window_comp.render_object:
        #     window_comp.cycle(surfaces)
            
        render_object = G.mgl.default_ro()
        render_object.render(uniforms=surfaces)

        if 'default' in self.surfaces:
            main_surface = self.surfaces['default']

            if 'background' in self.surfaces:
                main_surface.blit(self.surfaces['background'], (0, 0))

            for name in self.render_order:
                if name != 'default' and name != 'background' and name != 'ui':
                    if name in self.surfaces:
                        main_surface.blit(self.surfaces[name], (0, 0))

            if 'ui' in self.surfaces:
                main_surface.blit(self.surfaces['ui'], (0, 0))

    def blit(self, surface, pos, z=0, group='default'):
        if group in self.surfaces:
            self.surfaces[group].blit(surface, pos)