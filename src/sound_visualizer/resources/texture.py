import pygame
from OpenGL.GL import *


class Texture:
    def __init__(self, file_path: str) -> None:
        self._texture_id = glGenTextures(1)

        image = pygame.image.load(file_path).convert()
        self._width, self._height = image.get_width(), image.get_height()
        
        image_data = pygame.image.tobytes(image, "RGB", True)    
    
        glBindTexture(GL_TEXTURE_2D, self._texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            self._width,
            self._height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            image_data,
        )
        
        glGenerateMipmap(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, 0)
        
    def use(self, texture_unit) -> None:
        glActiveTexture(texture_unit)
        glBindTexture(GL_TEXTURE_2D, self._texture_id)
        
    def __del__(self) -> None:
        glDeleteTextures(1, [self._texture_id])