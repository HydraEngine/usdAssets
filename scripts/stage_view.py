#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import random
import sys
from typing import override

from PySide6.QtCore import Signal, QTimer
from PySide6.QtOpenGLWidgets import QOpenGLWidget as QGLWidget
from PySide6.QtWidgets import QApplication, QMainWindow
from pxr import CameraUtil, Usd, UsdImagingGL, UsdGeom, Gf, Sdf, Ar, UsdLux, Glf


class StageView(QGLWidget):
    updateSignal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(parent.size())
        parent.setCentralWidget(self)

        self.renderParams = UsdImagingGL.RenderParams()
        params = UsdImagingGL.Engine.Parameters()
        self._renderer = UsdImagingGL.Engine(params)

        # Create a new USD stage
        self.stage = Usd.Stage.CreateNew("red_sphere.usda")

        self._timer = QTimer(self)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self.update)
        self._timer.start()

    def computeWindowSize(self):
        size = self.size() * self.devicePixelRatioF()
        return (int(size.width()), int(size.height()))

    def computeWindowViewport(self):
        return (0, 0) + self.computeWindowSize()

    @staticmethod
    def _ComputeCameraFraming(viewport, renderBufferSize):
        x, y, w, h = viewport
        renderBufferWidth = renderBufferSize[0]
        renderBufferHeight = renderBufferSize[1]

        # Set display window equal to viewport - but flipped
        # since viewport is in y-Up coordinate system but
        # display window is y-Down.
        displayWindow = Gf.Range2f(
            Gf.Vec2f(x, renderBufferHeight - y - h),
            Gf.Vec2f(x + w, renderBufferHeight - y))

        # Intersect the display window with render buffer rect for
        # data window.
        renderBufferRect = Gf.Rect2i(
            Gf.Vec2i(0, 0), renderBufferWidth, renderBufferHeight)
        dataWindow = renderBufferRect.GetIntersection(
            Gf.Rect2i(
                Gf.Vec2i(x, renderBufferHeight - y - h),
                w, h))

        return CameraUtil.Framing(displayWindow, dataWindow)

    @override
    def paintGL(self):
        self.updateSignal.emit()

        viewport = self.computeWindowViewport()

        from OpenGL import GL
        # Workaround an apparent bug in some recent versions of PySide6
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glClearColor(0.0, 0.3, 0.3, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        # ensure viewport is right for the camera framing
        GL.glViewport(*viewport)

        renderBufferSize = Gf.Vec2i(self.computeWindowSize())
        self._renderer.SetRenderBufferSize(renderBufferSize)
        self._renderer.SetFraming(StageView._ComputeCameraFraming(viewport, renderBufferSize))
        self._renderer.Render(self.stage.GetPseudoRoot(), self.renderParams)

    def setAmbient(self, sceneAmbient):
        material = Glf.SimpleMaterial()
        self._renderer.SetLightingState([], material, sceneAmbient)

    def setCameraPath(self, path: str | Sdf.Path):
        self._renderer.SetCameraPath(path)

    def setCameraState(self, view_mat: Gf.Matrix4d, projection_mat: Gf.Matrix4d):
        self._renderer.SetCameraState(view_mat, projection_mat)

    def setRendererAov(self, aov: str | Ar.ResolvedPath):
        self._renderer.SetRendererAov(aov)

    def getRendererAovs(self):
        self._renderer.GetRendererAovs()

    def save(self):
        self.stage.Save()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setFixedSize(640, 480)

    view = StageView(window)
    view.setRendererAov("color")
    view.setAmbient((1, 1, 1, 1.0))
    view.renderParams.complexity = 1.2

    # setup stage
    view.stage.DefinePrim('/Sphere', 'Xform')
    sphere = view.stage.DefinePrim('/Sphere/Sphere', 'Sphere')
    sphereSchema = UsdGeom.Sphere(sphere)
    sphereSchema.GetDisplayColorAttr().Set([(0, 0, 1)])

    xform = view.stage.DefinePrim('/Light', 'Xform')
    xformSchema = UsdGeom.XformCommonAPI(xform)
    xformSchema.SetRotate((37.26105, 3.1637092, 106.936325))
    xformSchema.SetScale((1, 0.99999994, 1))
    xformSchema.SetTranslate((4.076245307922363, 1.0054539442062378, 5.903861999511719))

    light = view.stage.DefinePrim('/Light/Light', 'SphereLight')
    lightSchema = UsdLux.SphereLight(light)
    lightSchema.GetExtentAttr().Set([(-0.1, -0.1, -0.1), (0.1, 0.1, 0.1)])
    lightSchema.GetColorAttr().Set((1, 1, 1))
    lightSchema.GetDiffuseAttr().Set(1)
    lightSchema.GetExposureAttr().Set(0)
    lightSchema.GetIntensityAttr().Set(318.30988)
    lightSchema.GetNormalizeAttr().Set(1)
    lightSchema.GetRadiusAttr().Set(0.1)
    lightSchema.GetSpecularAttr().Set(1)

    xform = view.stage.DefinePrim('/Camera', 'Xform')
    xformSchema = UsdGeom.XformCommonAPI(xform)
    xformSchema.SetRotate((63.559296, 2.2983238e-7, 46.691944))
    xformSchema.SetScale((1, 1, 1))
    xformSchema.SetTranslate((7.358891487121582, -6.925790786743164, 4.958309173583984))

    camera = view.stage.DefinePrim('/Camera/Camera', 'Camera')
    cameraSchema = UsdGeom.Camera(camera)
    cameraSchema.GetProjectionAttr().Set("perspective")
    cameraSchema.GetFocalLengthAttr().Set(0.5)
    cameraSchema.GetHorizontalApertureAttr().Set(0.36)
    cameraSchema.GetHorizontalApertureOffsetAttr().Set(0)
    cameraSchema.GetVerticalApertureAttr().Set(0.2025)
    cameraSchema.GetVerticalApertureOffsetAttr().Set(0)
    cameraSchema.GetClippingRangeAttr().Set((0.1, 100))

    view.setCameraPath("/Camera/Camera")
    view.save()


    def update():
        a = random.random()
        print(a)
        lightSchema.GetColorAttr().Set((a, a, a))


    view.updateSignal.connect(update)

    window.show()
    app.exec()
