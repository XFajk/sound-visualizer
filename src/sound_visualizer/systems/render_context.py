from pyglm import glm

class _RenderContext:
    def __init__(self) -> None:
        self.view_transfrom = glm.mat4(1.0)
        self.projection_transform = glm.mat4(1.0)
        
        
RENDER_CONTEXT = _RenderContext()