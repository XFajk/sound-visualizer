import pygame
from OpenGL.GL import *
from pyglm import glm

from resources.shader import assign_new_view_to_default_shaders
from systems.time import TIME

SPEED = 5.0
SUPER_SPEED = 10.0
MOUSE_SENSITIVITY = 0.1


class DebugCamera:
    def __init__(self, position: glm.vec3, rotation: glm.vec3) -> None: 
        self.position = position
        self.rotation = rotation
        self._front = glm.vec3(0.0)
        
        self.set_in_space()
        
        
    def set_in_space(self) -> None:
        self._front.x = glm.sin(glm.radians(self.rotation.y)) * glm.cos(glm.radians(self.rotation.x))
        self._front.y = glm.sin(glm.radians(self.rotation.x))
        self._front.z = -glm.cos(glm.radians(self.rotation.y)) * glm.cos(glm.radians(self.rotation.x))
        self._front = glm.normalize(self._front)
        
        view_transform = glm.lookAt(
            self.position,
            self.position + self._front,
            glm.vec3(0.0, 1.0, 0.0),
        )
        
        assign_new_view_to_default_shaders(view_transform)

    
    def update(self) -> None:
        self._look_around()
        self._move(TIME.delta_time) 
        self.set_in_space()
        
    def _look_around(self) -> None:
        if pygame.mouse.get_relative_mode():
            mouse_x, mouse_y = pygame.mouse.get_rel()
        else:
            mouse_x, mouse_y = 0, 0
        
        self.rotation.x -= mouse_y * MOUSE_SENSITIVITY
        self.rotation.y += mouse_x * MOUSE_SENSITIVITY
        
        self.rotation.x = glm.clamp(self.rotation.x, -89.0, 89.0)
        
        just_keys = pygame.key.get_just_pressed()
        if just_keys[pygame.K_F1] and not pygame.mouse.get_relative_mode():
            pygame.mouse.set_relative_mode(True)
        elif just_keys[pygame.K_F1] and pygame.mouse.get_relative_mode():
            pygame.mouse.set_visible(True)
            
    def _move(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        
        direction: glm.vec3 = glm.vec3(0.0)
        if keys[pygame.K_w]:
            direction += self._front
        if keys[pygame.K_s]:
            direction -= self._front
        if keys[pygame.K_a]:
            direction -= glm.normalize(glm.cross(self._front, glm.vec3(0.0, 1.0, 0.0)))
        if keys[pygame.K_d]:
            direction += glm.normalize(glm.cross(self._front, glm.vec3(0.0, 1.0, 0.0))) 
        
        if keys[pygame.K_LSHIFT]:
            speed = SUPER_SPEED
        else:
            speed = SPEED
            
        if glm.length(direction) > 0.0: 
            self.position += glm.normalize(direction) * speed * dt 