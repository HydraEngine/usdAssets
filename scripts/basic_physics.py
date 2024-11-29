#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from pxr import CameraUtil, Usd, UsdImagingGL, UsdGeom, Gf, Sdf, Ar, UsdLux, Glf

if __name__ == '__main__':
    stage = Usd.Stage.CreateNew("basic_physics.usda")
    stage.DefinePrim('/Sphere', 'Xform')
    sphere = stage.DefinePrim('/Sphere/Sphere', 'Sphere')
    sphereSchema = UsdGeom.Sphere(sphere)
    sphereSchema.GetDisplayColorAttr().Set([(0, 0, 1)])

    xform = stage.DefinePrim('/Light', 'Xform')
    xformSchema = UsdGeom.XformCommonAPI(xform)
    xformSchema.SetRotate((37.26105, 3.1637092, 106.936325))
    xformSchema.SetScale((1, 0.99999994, 1))
    xformSchema.SetTranslate((4.076245307922363, 1.0054539442062378, 5.903861999511719))

    light = stage.DefinePrim('/Light/Light', 'SphereLight')
    lightSchema = UsdLux.SphereLight(light)
    lightSchema.GetExtentAttr().Set([(-0.1, -0.1, -0.1), (0.1, 0.1, 0.1)])
    lightSchema.GetColorAttr().Set((1, 1, 1))
    lightSchema.GetDiffuseAttr().Set(1)
    lightSchema.GetExposureAttr().Set(0)
    lightSchema.GetIntensityAttr().Set(318.30988)
    lightSchema.GetNormalizeAttr().Set(1)
    lightSchema.GetRadiusAttr().Set(0.1)
    lightSchema.GetSpecularAttr().Set(1)

    xform = stage.DefinePrim('/Camera', 'Xform')
    xformSchema = UsdGeom.XformCommonAPI(xform)
    xformSchema.SetRotate((63.559296, 2.2983238e-7, 46.691944))
    xformSchema.SetScale((1, 1, 1))
    xformSchema.SetTranslate((7.358891487121582, -6.925790786743164, 4.958309173583984))

    stage.Save()