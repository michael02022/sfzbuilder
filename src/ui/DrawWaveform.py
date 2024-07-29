'''
from PySide6.QtCore    import Property, QPointF, QRectF, QSize, Qt, Signal, QTimer
from PySide6.QtGui     import QPainter, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QWidget
from OpenGL.GL         import *
from OpenGL.GLUT       import *
from OpenGL.GLU        import *
from PySide6.QtOpenGLWidgets import QOpenGLWidget
import sys, importlib.util
name   = "rc_resources"
spec   = importlib.util.spec_from_file_location(name, "src/ui/rc_resources.py")
module = importlib.util.module_from_spec(spec)
sys.modules[name] = module
spec.loader.exec_module(module)
from rc_resources import *

class DrawWaveform(QOpenGLWidget):
    def __init__(self, parent=None):
        QOpenGLWidget.__init__(self)
        self.setFixedSize(QSize(100, 50))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(0)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)

    def paintGL(self):
        glMatrixMode(GL_PROJECTION)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 0.0, 0.0)

        glBegin(GL_LINES)
        glLineWidth(8)
        #glColor3f(1.0, 0.0, 0.0)
        glVertex2f(1.99, 1.99)
        glEnd
        glFlush()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
'''
