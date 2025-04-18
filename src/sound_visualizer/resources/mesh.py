from OpenGL.GL import *
import numpy as np
from numpy.typing import NDArray
from ctypes import c_void_p


class Mesh:
    def __init__(self, vertices: NDArray[np.float32], indices: NDArray[np.uint32]) -> None:
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

    def draw(self, index_count) -> None:
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, index_count, GL_UNSIGNED_INT, None)

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
    ) -> tuple[NDArray[np.float32], NDArray[np.uint32]]:
        vertices: NDArray[np.float32] = np.array([], dtype=np.float32)
        indices: NDArray[np.uint32] = np.array([], dtype=np.uint32)

        face_positions = np.array(
            [
                [1.0, 1.0, -1.0],
                [1.0, -1.0, -1.0],
                [-1.0, -1.0, -1.0],
                [-1.0, 1.0, -1.0],
            ],
            dtype=np.float32,
        )
        face_normal = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        tex_coords = np.array(
            [[1.0, 1.0], [1.0, 0.0], [0.0, 0.0], [0.0, 1.0]], dtype=np.float32
        )
        
        rotation = 0
        for i in range(4):
            face_transform = Matrix44.from_y_rotation(
                rotation, dtype=np.float32
            ) @ Matrix44.from_scale(
                np.array([w, h, d], dtype=np.float32), dtype=np.float32
            )
            
            # Transform the face positions by the transform matrix
            transformed_positions = np.empty((0, 3), dtype=np.float32)
            for p in face_positions:
                transformed_position = face_transform @ np.array(
                    [p[0], p[1], p[2], 1.0], dtype=np.float32
                )
                transformed_positions = np.vstack(
                    (transformed_positions, transformed_position[:3])
                )

            rotation_only = Matrix44.from_y_rotation(rotation, dtype=np.float32)
            transformed_normal = rotation_only @ np.array(
                [face_normal[0], face_normal[1], face_normal[2], 0.0], dtype=np.float32
            )
            transformed_normals = np.resize(
                transformed_normal[:3], transformed_positions.shape
            )


            face_data = np.column_stack((transformed_positions, transformed_normals, tex_coords)).flatten()
            
            vertices = np.append(vertices, face_data)
            indices = np.append(indices, np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32) + 4 * i)
            
            rotation += np.pi / 2
            
        rotation = np.pi / 2
        for i in range(2):
            face_transform = Matrix44.from_x_rotation(
                rotation, dtype=np.float32
            ) @ Matrix44.from_scale(
                np.array([w, h, d], dtype=np.float32), dtype=np.float32
            )
            
            # Transform the face positions by the transform matrix
            transformed_positions = np.empty((0, 3), dtype=np.float32)
            for p in face_positions:
                transformed_position = face_transform @ np.array(
                    [p[0], p[1], p[2], 1.0], dtype=np.float32
                )
                transformed_positions = np.vstack(
                    (transformed_positions, transformed_position[:3])
                )

            rotation_only = Matrix44.from_x_rotation(rotation, dtype=np.float32)
            transformed_normal = rotation_only @ np.array(
                [face_normal[0], face_normal[1], face_normal[2], 0.0], dtype=np.float32
            )
            transformed_normals = np.resize(
                transformed_normal[:3], transformed_positions.shape
            )


            face_data = np.column_stack((transformed_positions, transformed_normals, tex_coords)).flatten()
            
            vertices = np.append(vertices, face_data)
            indices = np.append(indices, np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32) + 4 * (i+4))
            
            rotation += np.pi 

        return vertices, indices

    @staticmethod
    def generate_plain_data(
        w: float, h: float, cuts_x: int, cuts_y: int
    ) -> tuple[list[float], list[int]]:
        return [], []