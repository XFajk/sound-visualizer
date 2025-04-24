import pygame
from OpenGL.GL import *
from pyglm import glm
import os
import sys

from systems.time import TIME
from systems.render_context import RENDER_CONTEXT

from resources.shader import (
    init_default_shaders,
    assign_new_projection_to_default_shaders,
)

from objects.mesh_object import MeshObject
from objects.light_object import LightObject
from objects.debug_camera import DebugCamera

from resources.mesh import Mesh
from resources.texture import Texture


def main() -> None:
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
    )

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, GL_TRUE)

    window = pygame.display.set_mode(
        (800, 600), flags=pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE
    )
    clock = pygame.time.Clock()

    print("OpenGL version:", glGetString(GL_VERSION))

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glViewport(0, 0, window.get_width(), window.get_height())

    init_default_shaders()

    RENDER_CONTEXT.projection_transform = glm.perspective(45.0, 800 / 600, 0.01, 100.0)
    assign_new_projection_to_default_shaders(
        RENDER_CONTEXT.projection_transform
    )

    camera = DebugCamera(
        glm.vec3(0.0, 0.0, 5.0),
        glm.vec3(0.0, 0.0, 0.0),
    )

    mesh_object = MeshObject(
        Mesh(*Mesh.generate_cube_data(2.0, 3.0, 1.0)),
        Texture.from_color(pygame.Color.from_normalized(0.3, 0.5, 0.1, 1.0)),
        glm.vec3(0.0, 0.0, -5.0),
        glm.vec3(0.0, 0.0, 0.0),
        glm.vec3(1.0, 1.0, 1.0),
    )

    light = LightObject(
        glm.vec3(1.0, 1.0, 1.0),
        glm.vec3(45.0, 110, 0),
        glm.vec3(1.0, 1.0, 1.0),
        pygame.Color.from_normalized(1.0, 1.0, 1.0, 1.0),
    )

    running = True
    while running:

        TIME.update()

        camera.update()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        light.position.x += glm.cos(TIME.time) * 5 * TIME.delta_time
        light.position.z -= glm.sin(TIME.time) * 5 * TIME.delta_time
        light.draw()

        mesh_object.rotation.x += 90.0 * TIME.delta_time
        mesh_object.draw()
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                glViewport(0, 0, event.w, event.h)
                RENDER_CONTEXT.projection_transform = glm.perspective(45.0, 800 / 600, 0.01, 100.0)
                assign_new_projection_to_default_shaders(
                    RENDER_CONTEXT.projection_transform
                )
        pygame.display.set_caption(f"FPS: {int(clock.get_fps())}")
        clock.tick(120)


if __name__ == "__main__":
    pygame.init()

    # Check if the system platform is Linux
    if sys.platform.startswith("linux"):
        os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

    main()
    pygame.quit()
