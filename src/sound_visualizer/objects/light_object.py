import pygame
from OpenGL.GL import *
import numpy as np
from pyglm import glm

from ctypes import c_void_p

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

        vertices, indices = Mesh.generate_cube_data(
            0.1, 0.1, 0.1, data_mask=(1, 1, 1, 0, 0, 0, 0, 0)
        )
        vertices, indices = np.array(vertices, dtype=np.float32), np.array(
            indices, dtype=np.uint32
        )

        self._index_count = len(indices)

        self._vao = glGenVertexArrays(1)
        glBindVertexArray(self._vao)

        self._vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        self._ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        self._texture = Texture.from_color(color)

        self._color = color
        self._color_location = self._shader.uniform_locations["light_color"]
        self._light_pos_location = self._object_shader.uniform_locations["light_pos"]

        self.position = position
        self.rotation = rotation
        self.scale = scale

    def draw(self) -> None:
        color = self._color.normalized

        self._object_shader.use()
        glUniform4f(
            self._object_shader.uniform_locations["light_color"],
            color[0],
            color[1],
            color[2],
            color[3],
        )
        glUniform3f(
            self._light_pos_location, self.position.x, self.position.y, self.position.z
        )

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

        glBindVertexArray(self._vao)
        glDrawElements(
            GL_TRIANGLES,
            self._index_count,
            GL_UNSIGNED_INT,
            None,
        )

    def __del__(self):
        glDeleteBuffers(
            2,
            (
                self._vbo,
                self._ebo,
            ),
        )
        glDeleteVertexArrays(1, (self._vao,))
