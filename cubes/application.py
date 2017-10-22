from collections import namedtuple
from random import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import cubes.graphics as graphics

Material = namedtuple('Material', ['ambient', 'diffuse', 'specular', 'shine'])

class Rotation:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class Application:
    _ROTATION_DELTA = 5
    _ROTATIONS_KEYS_MAPPINGS = {
        GLUT_KEY_RIGHT : ('y', +1),
        GLUT_KEY_LEFT : ('y', -1),
        GLUT_KEY_UP : ('x', +1),
        GLUT_KEY_DOWN : ('x', -1),
        b'z' : ('z', +1),
        b'x' : ('z', -1)
    }
    _COLOR_MATERIAL = -1
    _MATERIALS = [
        _COLOR_MATERIAL,
        Material(
            ambient=[0.329412, 0.223529, 0.027451, 1.0],
            diffuse=[0.780392, 0.568627, 0.113725, 1.0],
            specular=[0.992157, 0.941176, 0.807843, 1.0],
            shine=27.8974
        ),
        Material(
            ambient=[0.2125, 0.1275, 0.054, 1.0],
            diffuse=[0.714, 0.4284, 0.18144, 1.0],
            specular=[0.393548, 0.271906, 0.166721, 1.0],
            shine=25.6
        ),
        Material(
            ambient=[0.25, 0.25, 0.25, 1.0],
            diffuse=[0.4, 0.4, 0.4, 1.0],
            specular=[0.774597, 0.774597, 0.774597, 1.0],
            shine=76.8
        ),
        Material(
            ambient=[0.05375, 0.05, 0.06625, 0.82],
            diffuse=[0.18275, 0.17, 0.22525, 0.82],
            specular=[0.332741, 0.328634, 0.346435, 0.82],
            shine=38.4
        )
    ]

    def __init__(self):
        self._colors = [(random(), random(), random()) for _ in range(0, 1000)] # Ploho
        self._scene_rotation = Rotation()
        self._light_rotation = Rotation()
        self._rotations = [self._scene_rotation, self._light_rotation]
        self._current_rotation = 0
        self._lightning = True
        self._spot_light = True
        self._material = 0
        self._model = 0
        self._colorify = True
        self._zoom = 100

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutCreateWindow(b"Hello world!")

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

        self.setup_callbacks()

        self.models = [
            graphics.ObjLoader("files/cubes.txt"),
            graphics.ObjLoader("files/plane.txt"),
            graphics.ObjLoader("files/scene.txt"),
            graphics.ObjLoader("files/cube.txt"),
            graphics.ObjLoader("files/monkey.txt")
        ]

    def render(self):
        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        self.setup_light()

        if self._lightning:
            self.light_transformations()
            self.draw_light()

        glLoadIdentity()

        gluPerspective(80, 4.0 / 3.0, 1.0, 100.0)
        gluLookAt(-3*100/self._zoom, 5*100/self._zoom, 5*100/self._zoom, 0, 0, 0, 0, 1, 0)

        self.scene_transformations()
        self.set_material()
        glColor3f(*self._colors[0])
        self.models[self._model].render_scene(self._colorify, self._colors)

        glFlush()
        glutSwapBuffers()

    def on_key_press(self, key, x, y):
        if key in self._ROTATIONS_KEYS_MAPPINGS:
            rotation = self._rotations[self._current_rotation]
            rotation_action = self._ROTATIONS_KEYS_MAPPINGS[key]
            coordinate, signum = rotation_action
            rotation_angle = getattr(rotation, coordinate)
            rotation_angle += self._ROTATION_DELTA * signum
            setattr(rotation, coordinate, rotation_angle)
        elif key == b'r':
            self._current_rotation = (self._current_rotation + 1) % len(self._rotations)
        elif key == b'l':
            self._lightning = not self._lightning
        elif key == b'd':
            self._spot_light = not self._spot_light
        elif key == b'm':
            self._material = (self._material + 1) % len(self._MATERIALS)
        elif key == b'n':
            self._model = (self._model + 1) % len(self.models)
        elif key == b'b':
            self._model = (self._model - 1) % len(self.models)
        elif key == b'c':
            self._colorify = not self._colorify
        elif key == b'q':
            self._zoom += 10
        elif key == b'a':
            if self._zoom > 10:
                self._zoom -= 10
        glutPostRedisplay()

    def rotate_transformation(self, rotation):
        glRotatef(rotation.x, 1.0, 0.0, 0.0)
        glRotatef(rotation.y, 0.0, 1.0, 0.0)
        glRotatef(rotation.z, 0.0, 0.0, 1.0)

    def scene_transformations(self):
        self.rotate_transformation(self._scene_rotation)

    def light_transformations(self):
        self.rotate_transformation(self._light_rotation)

    def draw_light(self):
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, -1, int(self._spot_light)))

    def set_material(self):
        material = self._MATERIALS[self._material]
        if material == self._COLOR_MATERIAL:
            glEnable(GL_COLOR_MATERIAL)
        else:
            glDisable(GL_COLOR_MATERIAL)
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, material.ambient)
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material.diffuse)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, material.specular)
            glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, material.shine)

    def setup_light(self):
        self.gl_set_bool(GL_LIGHT0, self._lightning)

    def setup_callbacks(self):
        glutDisplayFunc(self.render)
        glutSpecialFunc(self.on_key_press)
        glutKeyboardFunc(self.on_key_press)

    @staticmethod
    def gl_set_bool(name, value):
        if value:
            glEnable(name)
        else:
            glDisable(name)

    def start(self):
        glutMainLoop()
