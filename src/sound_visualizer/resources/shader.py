from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader
from pyglm import glm

from systems.time import TIME

class ShaderProgram:
    def __init__(self, vertex_shader_path: str, fragment_shader_path: str, uniforms: list[str] = [], texture_units: int = 0) -> None:
        with open(vertex_shader_path) as vertex_file:
            vertex_src = vertex_file.readlines()
            vertex_shader = compileShader(
                vertex_src, GL_VERTEX_SHADER
            )

        with open(fragment_shader_path) as fragment_file:
            fragment_src = fragment_file.readlines()
            fragment_shader = compileShader(
                fragment_src, GL_FRAGMENT_SHADER
            )
            
        self.program = glCreateProgram()
        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program) 
        
        if glGetProgramiv(self.program, GL_LINK_STATUS) != GL_TRUE:
            glDeleteProgram(self.program)
            raise RuntimeError(
                f"Shader program linking failed: {glGetProgramInfoLog(self.program)}"
            )
            
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
            
        self.uniform_locations: dict[str, int] = {}
        self._TIME_location = glGetUniformLocation(self.program, "TIME")
        for uniform in uniforms:
            self.uniform_locations[uniform] = glGetUniformLocation(self.program, uniform)
            
        for i in range(texture_units):
            self.uniform_locations[f"texture{i}"] = glGetUniformLocation(self.program, f"texture{i}")
            if not self.uniform_locations[f"texture{i}"] == -1:
                glUniform1i(self.uniform_locations[f"texture{i}"], i)


    def use(self) -> None:
        glUseProgram(self.program)  
        glUniform1f(self._TIME_location, TIME.time)

        
    def __del__(self) -> None:
        glDeleteProgram(self.program)
        

_OBJECT_SHADER = None
_LIGHT_SHADER = None

def init_default_shaders() -> None:
    global _OBJECT_SHADER, _LIGHT_SHADER
    _OBJECT_SHADER = ShaderProgram("./shaders/object/vertex.glsl", "./shaders/object/fragment.glsl", ["projection", "view", "model", "normal_matrix", "light_color", "light_pos"], 1)
    _LIGHT_SHADER = ShaderProgram("./shaders/light/vertex.glsl", "./shaders/light/fragment.glsl", ["projection", "view", "model", "light_color"])

    
def get_object_shader() -> ShaderProgram:
    global _OBJECT_SHADER
    if _OBJECT_SHADER is None:
        raise RuntimeError("Shaders not initialized. Call init_default_shaders() after crating the OpenGL context.")
    return _OBJECT_SHADER

def get_light_shader() -> ShaderProgram:
    global _LIGHT_SHADER
    if _LIGHT_SHADER is None:
        raise RuntimeError("Shaders not initialized. Call init_default_shaders() after crating the OpenGL context.")
    return _LIGHT_SHADER

def assign_new_projection_to_default_shaders(projection: glm.mat4) -> None:
    global _OBJECT_SHADER, _LIGHT_SHADER
    if _OBJECT_SHADER is None or _LIGHT_SHADER is None:
        raise RuntimeError("Shaders not initialized. Call init_default_shaders() after crating the OpenGL context.")
    _OBJECT_SHADER.use() 
    glUniformMatrix4fv(_OBJECT_SHADER.uniform_locations["projection"], 1, GL_FALSE, glm.value_ptr(projection))
    _LIGHT_SHADER.use()
    glUniformMatrix4fv(_LIGHT_SHADER.uniform_locations["projection"], 1, GL_FALSE, glm.value_ptr(projection))
    
def assign_new_view_to_default_shaders(view: glm.mat4) -> None:
    global _OBJECT_SHADER, _LIGHT_SHADER
    if _OBJECT_SHADER is None or _LIGHT_SHADER is None:
        raise RuntimeError("Shaders not initialized. Call init_default_shaders() after crating the OpenGL context.")
    
    _OBJECT_SHADER.use() 
    glUniformMatrix4fv(_OBJECT_SHADER.uniform_locations["view"], 1, GL_FALSE, glm.value_ptr(view))
    _LIGHT_SHADER.use()
    glUniformMatrix4fv(_LIGHT_SHADER.uniform_locations["view"], 1, GL_FALSE, glm.value_ptr(view))