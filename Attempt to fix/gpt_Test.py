import pywavefront
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def load_obj(filename):
    scene = pywavefront.Wavefront(filename)
    print(f"Type of scene.mesh_list: {type(scene.mesh_list)}")
    if isinstance(scene.mesh_list, dict):
        print("Mesh names in scene:")
        for name, mesh in scene.mesh_list.items():
            print(f"Mesh name: {name}, Vertices count: {len(mesh.vertices)}")
    elif isinstance(scene.mesh_list, list):
        print("Meshes in scene (list format):")
        for mesh in scene.mesh_list:
            print(f"Vertices count: {len(mesh.vertices)}")
    return scene

def initialize_colors(scene):
    # Initialize color array for vertices; assume all white initially
    colors = {}
    if isinstance(scene.mesh_list, dict):
        for name, mesh in scene.mesh_list.items():
            colors[name] = np.ones((len(mesh.vertices), 3), dtype=np.float32)
    elif isinstance(scene.mesh_list, list):
        for i, mesh in enumerate(scene.mesh_list):
            colors[i] = np.ones((len(mesh.vertices), 3), dtype=np.float32)
    return colors

def draw_scene(scene, colors):
    glBegin(GL_TRIANGLES)
    if isinstance(scene.mesh_list, dict):
        for name, mesh in scene.mesh_list.items():
            color = colors[name]
            for i, vertex in enumerate(mesh.vertices):
                glColor3fv(color[i])
                glVertex3f(*vertex)
    elif isinstance(scene.mesh_list, list):
        for i, mesh in enumerate(scene.mesh_list):
            color = colors[i]
            for j, vertex in enumerate(mesh.vertices):
                glColor3fv(color[j])
                glVertex3f(*vertex)
    glEnd()

def process_click(x, y, width, height, scene, colors):
    print(f"Click at ({x}, {y})")
    # Implement logic to convert screen coordinates to object coordinates
    # and update the color array accordingly

def main(filename):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    glEnable(GL_DEPTH_TEST)

    scene = load_obj(filename)
    colors = initialize_colors(scene)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                process_click(x, y, display[0], display[1], scene, colors)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_scene(scene, colors)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main("feet.obj")