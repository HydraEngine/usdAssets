#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from pxr import Usd, UsdGeom, UsdLux, UsdShade, Sdf, Gf

if __name__ == '__main__':
    # Create a new stage in memory
    stage = Usd.Stage.CreateNew("shadow.usda")

    # Define a ground plane
    ground_plane = UsdGeom.Mesh.Define(stage, '/GroundPlane')
    ground_plane.CreatePointsAttr([(-10, 0, -10), (10, 0, -10), (10, 0, 10), (-10, 0, 10)])
    ground_plane.CreateFaceVertexCountsAttr([4])
    ground_plane.CreateFaceVertexIndicesAttr([0, 1, 2, 3])

    # Create a material for the ground plane
    ground_material = UsdShade.Material.Define(stage, '/GroundMaterial')
    ground_shader = UsdShade.Shader.Define(stage, '/GroundMaterial/GroundShader')
    ground_shader.CreateIdAttr('UsdPreviewSurface')
    ground_shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set((0.5, 0.5, 0.5))
    ground_shader.CreateInput('metallic', Sdf.ValueTypeNames.Float).Set(0.0)
    ground_shader.CreateInput('roughness', Sdf.ValueTypeNames.Float).Set(0.5)
    ground_material.CreateSurfaceOutput().ConnectToSource(ground_shader.ConnectableAPI(), 'surface')
    UsdShade.MaterialBindingAPI(ground_plane).Bind(ground_material)

    # Define a sphere
    sphere = UsdGeom.Sphere.Define(stage, '/Sphere')
    sphere.GetRadiusAttr().Set(1.0)
    sphere.AddTranslateOp().Set(Gf.Vec3f(0, 1, 0))

    # Create a material for the sphere
    sphere_material = UsdShade.Material.Define(stage, '/SphereMaterial')
    sphere_shader = UsdShade.Shader.Define(stage, '/SphereMaterial/SphereShader')
    sphere_shader.CreateIdAttr('UsdPreviewSurface')
    sphere_shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set((1.0, 0.0, 0.0))
    sphere_shader.CreateInput('metallic', Sdf.ValueTypeNames.Float).Set(0.0)
    sphere_shader.CreateInput('roughness', Sdf.ValueTypeNames.Float).Set(0.5)
    sphere_material.CreateSurfaceOutput().ConnectToSource(sphere_shader.ConnectableAPI(), 'surface')
    UsdShade.MaterialBindingAPI(sphere).Bind(sphere_material)

    # Create a light
    light = UsdLux.DistantLight.Define(stage, '/Light')
    light.AddTranslateOp().Set(Gf.Vec3f(0, 5, 0))
    light.AddRotateXOp().Set(-80.0)
    light.CreateIntensityAttr().Set(100000.0)
    light.CreateColorAttr().Set(Gf.Vec3f(1.0, 0.0, 1.0))

    # Apply the ShadowAPI to the light
    shadowAPI = UsdLux.ShadowAPI.Apply(light.GetPrim())

    # Enable shadow
    shadowAPI.CreateShadowEnableAttr().Set(True)

    # Print the resulting stage
    stage.Save()
