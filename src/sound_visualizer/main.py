import pygame
from OpenGL.GL import *
from pyglm import glm
import os
import sys

from time import perf_counter

from shader import ShaderProgram

from objects.mesh_object3d import MeshObject3D

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
    glClearColor(0.4, 0.6, 0.2, 1.0)
    glViewport(0, 0, window.get_width(), window.get_height())

    base_program = ShaderProgram("./shaders/vertex.glsl", "./shaders/fragment.glsl")
    base_program.use(0.0)

    glUniform1i(base_program.texture_location, 0)

    projection = glm.perspective(45.0, 800 / 600, 0.01, 100.0)
    glUniformMatrix4fv(
        base_program.projection_location, 1, GL_FALSE, glm.value_ptr(projection)
    )

    mesh = Mesh(*Mesh.generate_cube_data(1.0, 1.0, 1.0))
    texture = Texture("./assets/wall.jpg")

    mesh_object = MeshObject3D(
        mesh,
        texture,
        glm.vec3(0.0, 0.0, -5.0),
        glm.vec3(0.0, 0.0, 0.0),
        glm.vec3(1.0, 1.0, 1.0),
        base_program,
    )

    last_frame_time = perf_counter()

    running = True
    while running:

        current_frame_time = perf_counter()
        dt = current_frame_time - last_frame_time
        last_frame_time = current_frame_time

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        base_program.use(dt)

        mesh_object.rotation.x += 90.0 * dt
        mesh_object.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.WINDOWRESIZED:
                glViewport(0, 0, window.get_width(), window.get_height())
                projection = glm.perspective(
                    45.0, window.get_width() / window.get_height(), 0.01, 100.0
                )
                glUniformMatrix4fv(
                    base_program.projection_location,
                    1,
                    GL_FALSE,
                    glm.value_ptr(projection),
                )

        pygame.display.set_caption(f"FPS: {int(clock.get_fps())}")
        clock.tick(1000)


if __name__ == "__main__":
    pygame.init()

    # Check if the system platform is Linux
    if sys.platform.startswith("linux"):
        os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

    main()
    pygame.quit()
