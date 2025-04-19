import pygame
from OpenGL.GL import *

class Texture:
    def __init__(self, image: pygame.Surface) -> None:
        self._texture_id = glGenTextures(1)
        self.width, self.height = image.get_size()
        
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
            self.width,
            self.height,
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
        
        
    @classmethod
    def from_file(cls, file_path: str) -> "Texture":
        image = pygame.image.load(file_path).convert()
        texture = cls(image)
        return texture
    
    @classmethod
    def from_color(cls, color: pygame.Color) -> "Texture":
        image = pygame.Surface((1, 1))
        image.fill(color)
        texture = cls(image)
        return texture