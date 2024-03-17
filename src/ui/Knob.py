# This Python file uses the following encoding: utf-8
from PySide6.QtCore    import QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui     import QPainter, QPixmap
from PySide6.QtWidgets import QWidget

def clamp(n, min, max):
  t = min if (n < min) else n
  return max if (t > max) else t

class Range:
  def __init__(self):
    self.minimum    = 0.0
    self.maximum    = 1.0
    self.value      = 0.0
    self.isDragging = False

  def setMinimum(self, minimum):
    if (minimum == self.minimum):
      return False
    elif (minimum > self.value):
      if (minimum > self.maximum):
        self.maximum = minimum
      self.value = minimum
    self.minimum = minimum
    return True

  def setMaximum(self, maximum):
    if (maximum == self.maximum):
      return False
    elif (maximum < self.value):
      if (maximum < self.minimum):
        self.minimum = maximum
      self.value = maximum
    self.maximum = maximum
    return True

  def setValue(self, value):
    if (self.value == value):
        return False
    clamp(value, self.minimum, self.maximum);
    self.value = value
    return True

class KnobPrivate:
  def __init__(self, knob):
    self.q = knob
    self.framesPixmap  = QPixmap()
    self.previousPoint = QPointF()
    self.currentFrameY =   0
    self.frameCount    = 100
    self.frameHeight   =  64
    self.frameWidth    =  64
    self.param         =  -1
    self.defaultValue  =   0
    self.inverted      = False

class Knob(QWidget):
  pixmapChanged = Signal(QPixmap)
  valueChanged  = Signal(float)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.d = KnobPrivate(self)
    self.r = Range()

  def sizeHint(self):
    if (not self.d.framesPixmap.isNull()):
      return QSize(self.d.frameWidth, self.d.frameHeight)
    return QWidget.sizeHint(self)

  def minimumSizeHint(self):
    return self.sizeHint()

  def mouseMoveEvent(self, event):
    if (self.d.framesPixmap.isNull() or not self.r.isDragging):
      return
    if (event.pos().x() > self.d.previousPoint.x() or
      event.pos().y() < self.d.previousPoint.y()):
        if (self.d.currentFrameY < self.d.framesPixmap.height()):
            self.d.currentFrameY += self.d.frameHeight;
        else:
          if (self.d.currentFrameY >= self.d.frameHeight):
            self.d.currentFrameY -= self.d.frameHeight
    self.d.previousPoint = event.pos()
    rnge     = self.r.maximum - self.r.minimum
    newValue = self.d.currentFrameY * rnge / self.d.framesPixmap.height() + self.r.minimum
    self.setValue(newValue)

  def mousePressEvent(self, event):
    if (event.button() == Qt.LeftButton):
      self.r.isDragging = True

  def mouseReleaseEvent(self, event):
    self.r.isDragging = False

  def paintEvent(self, event):
    if (self.d.framesPixmap.isNull()):
      print("[Knob.py] pixmap is null")
      return;
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    if (self.d.currentFrameY == self.d.framesPixmap.height()):
        self.d.currentFrameY-= self.d.frameHeight;
    painter.drawPixmap(
      QRectF(0, 0, -1, -1),
      self.d.framesPixmap,
      QRectF(0, self.d.currentFrameY, self.d.frameWidth, self.d.frameHeight)
    )

  def setInverted(self, inverted):
    if (self.inverted == inverted):
      return
    self.d.inverted = inverted;
    self.update()

  def isInverted(self):
    return self.d.inverted

  def setPixmap(self, pixmap, frameCount = None):
    self.d.framesPixmap  = pixmap
    self.d.currentFrameY = 0
    self.d.frameWidth    = pixmap.width()
    self.d.frameHeight   = pixmap.height() / self.d.frameCount
    self.d.previousPoint = QPointF();
    self.pixmapChanged.emit(pixmap)
    self.update()
    if (frameCount is not None):
      self.setFrameCount(frameCount)

  def pixmap(self):
    return self.d.framesPixmap

  def setFrameCount(self, frameCount):
    if (self.d.frameCount == frameCount):
      return
    self.d.frameCount = frameCount

  def frameCount(self):
    return self.d.frameCount

  def setParam(self, param):
    if (self.d.param == param):
      return
    self.d.param = param

  def param(self):
    return self.d.param

  def setDefaultValue(self, defaultValue):
    if (defaultValue == self.d.defaultValue):
      return
    self.d.defaultValue = defaultValue

  def defaultValue(self):
    return self.d.defaultValue

  def setMinimum(self, minimum):
    self.r.minimum = minimum

  def minimum(self):
    return self.r.minimum

  def setMaximum(self, maximum):
    self.r.maximum = maximum

  def maximum(self):
    return self.r.maximum

  def setValue(self, value):
    if (not self.isEnabled() or not self.r.setValue(value)):
      return
    rnge = self.r.maximum - self.r.minimum;
    self.d.currentFrameY = self.d.frameHeight * value / rnge;
    self.d.value  = value;
    self.valueChanged.emit(value)
    self.update()

  def value(self):
    return self.r.value
