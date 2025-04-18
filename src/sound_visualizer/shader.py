from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader


class ShaderProgram:
    def __init__(self, vertex_shader_path: str, fragment_shader_path: str):
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
            
        self.TIME_location = glGetUniformLocation(self.program, "TIME")
        self.model_location = glGetUniformLocation(self.program, "model")
        self.projection_location = glGetUniformLocation(self.program, "projection")
        self.view_location = glGetUniformLocation(self.program, "view")
        self.texture_location = glGetUniformLocation(self.program, "texture1")
        
        self.TIME = 0.0
        

    def use(self, dt: float) -> None:
        glUseProgram(self.program)
        self.TIME += dt
        
        glUniform1f(self.TIME_location, self.TIME) 