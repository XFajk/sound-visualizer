from OpenGL.GL import *
import numpy as np
from numpy.typing import NDArray
from pyglm import glm
from ctypes import c_void_p


class Mesh:
    def __init__(self, vertices: list[float], indices: list[int]) -> None:
        vertices = np.array(vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)

        self.index_count = len(indices)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, c_void_p(6 * 4))
        glEnableVertexAttribArray(2)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def draw(self) -> None:
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.index_count, GL_UNSIGNED_INT, None)

    def __del__(self):
        glDeleteBuffers(
            2,
            (
                self.vbo,
                self.ebo,
            ),
        )
        glDeleteVertexArrays(1, (self.vao,))

    @staticmethod
    def generate_cube_data(
        w: float, h: float, d: float
    ) -> tuple[list[float], list[int]]:
        vertices: list[float] = []
        indices: list[int] = []

        face_positions = [
            glm.vec3(1.0, 1.0, -1.0),
            glm.vec3(1.0, -1.0, -1.0),
            glm.vec3(-1.0, -1.0, -1.0),
            glm.vec3(-1.0, 1.0, -1.0),
        ]

        face_normal = glm.vec3(0.0, 0.0, -1.0)
        face_tex_coords = [
            glm.vec2(1.0, 1.0),
            glm.vec2(1.0, 0.0),
            glm.vec2(0.0, 0.0),
            glm.vec2(0.0, 1.0),
        ]

        def get_transformed_face_data(
            position_transform: glm.mat4, normal_transform: glm.mat4, index_offset: int
        ) -> tuple[NDArray[np.float32], NDArray[np.uint32]]:
            face_data = []
            index_data = list(map(lambda x: x+index_offset, [0, 1, 2, 3, 0, 2]))
        
            
            for i, p in enumerate(face_positions):
                transformed_position: glm.vec4 = position_transform @ glm.vec4(p, 1.0)
                transformed_normal: glm.vec4 = normal_transform @ glm.vec4(
                    face_normal, 0.0
                )

                vertex = [
                    transformed_position.x,
                    transformed_position.y,
                    transformed_position.z,
                    transformed_normal.x,
                    transformed_normal.y,
                    transformed_normal.z,
                    face_tex_coords[i].x,
                    face_tex_coords[i].y,
                ]
                face_data.extend(vertex)

            return face_data, index_data

        for i in range(4):
            rotation_transform = glm.rotate(
                glm.radians(90.0 * i), glm.vec3(0.0, 1.0, 0.0)
            )
            scale_transform = glm.scale(glm.vec3(w, h, d))

            vertex_data, index_data = get_transformed_face_data(
                rotation_transform @ scale_transform, rotation_transform, 4 * i
            )

            vertices.extend(vertex_data) 
            indices.extend(index_data)
            
        for i in range(2):
            rotation_transform = glm.rotate(
                glm.radians(180.0 * i + 90), glm.vec3(1.0, 0.0, 0.0)
            )
            scale_transform = glm.scale(glm.vec3(w, h, d))

            vertex_data, index_data = get_transformed_face_data(
                rotation_transform @ scale_transform, rotation_transform, 4 * (i + 4)
            )

            vertices.extend(vertex_data) 
            indices.extend(index_data)

        return vertices, indices

    @staticmethod
    def generate_plain_data(
        w: float, h: float, cuts_x: int, cuts_y: int
    ) -> tuple[list[float], list[int]]:
        return [], []
