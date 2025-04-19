import pygame
from OpenGL.GL import *
from pyglm import glm

from resources.shader import get_light_shader, get_object_shader 

from resources.mesh import Mesh
from resources.texture import Texture


class LightObject:
    def __init__(
        self,
        position: glm.vec3,
        rotation: glm.vec3,
        scale: glm.vec3,
        color: pygame.Color,
    ) -> None:
        
        self._shader = get_light_shader()
        self._object_shader = get_object_shader()
        
        self._model_transform = (
            glm.translate(position)
            @ glm.rotate(glm.radians(rotation.z), glm.vec3(0.0, 0.0, 1.0))
            @ glm.rotate(glm.radians(rotation.y), glm.vec3(0.0, 1.0, 0.0))
            @ glm.rotate(glm.radians(rotation.x), glm.vec3(1.0, 0.0, 0.0))
            @ glm.scale(scale)
        )
        self._model_transform_location = self._shader.uniform_locations["model"]

        self._mesh = Mesh(*Mesh.generate_cube_data(0.1, 0.1, 0.1))
        self._texture = Texture.from_color(color)

        self._color = color
        self._color_location = self._shader.uniform_locations["light_color"]

        self.position = position
        self.rotation = rotation
        self.scale = scale

    def draw(self) -> None:
        color = self._color.normalized
        
        self._object_shader.use() 
        glUniform4f(self._object_shader.uniform_locations["light_color"], color[0], color[1], color[2], color[3])
       
        self._shader.use() 
        glUniform4f(self._color_location, color[0], color[1], color[2], color[3])

        self._texture.use(GL_TEXTURE0)

        self._model_transform = (
            glm.translate(self.position)
            @ glm.rotate(glm.radians(self.rotation.z), glm.vec3(0.0, 0.0, 1.0))
            @ glm.rotate(glm.radians(self.rotation.y), glm.vec3(0.0, 1.0, 0.0))
            @ glm.rotate(glm.radians(self.rotation.x), glm.vec3(1.0, 0.0, 0.0))
            @ glm.scale(self.scale)
        )

        glUniformMatrix4fv(
            self._model_transform_location,
            1,
            GL_FALSE,
            glm.value_ptr(self._model_transform),
        )
         
        self._mesh.draw()
