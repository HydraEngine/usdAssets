#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from pxr import Usd, UsdGeom, Gf, UsdPhysics, UsdShade

if __name__ == '__main__':
    stage = Usd.Stage.CreateNew("basic_physics.usda")

    # Physics scene definition
    scene = UsdPhysics.Scene.Define(stage, "/physicsScene")

    # setup gravity
    # note that gravity has to respect the selected units, if we are using cm, the gravity has to respect that
    scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, 0.0, -1.0))
    scene.CreateGravityMagnitudeAttr().Set(981.0)

    # Top level actor, contains rigid body
    rigidCompoundPath = "/compoundRigid"
    rigidXform = UsdGeom.Xform.Define(stage, rigidCompoundPath)
    rigidPrim = stage.GetPrimAtPath(rigidCompoundPath)

    # Rigid body transform
    rigidCompoundPos = Gf.Vec3f(0.0, 0.0, 10.0)
    rigidXform.AddTranslateOp().Set(rigidCompoundPos)
    rigidXform.AddOrientOp().Set(Gf.Quatf(1.0, 0.0, 0.0, 0.0))

    physicsAPI = UsdPhysics.RigidBodyAPI.Apply(rigidPrim)

    # Collision shape
    collisionShape = rigidCompoundPath + "/physicsBoxShape"

    size = 25.0
    shapePos = Gf.Vec3f(0.0)
    shapeQuat = Gf.Quatf(1.0)

    cubeGeom = UsdGeom.Cube.Define(stage, collisionShape)
    cubePrim = stage.GetPrimAtPath(collisionShape)
    cubeGeom.CreateSizeAttr(size)
    cubeGeom.AddTranslateOp().Set(shapePos)
    cubeGeom.AddOrientOp().Set(shapeQuat)

    # set it as collision
    UsdPhysics.CollisionAPI.Apply(cubePrim)

    # hide it from rendering
    cubeGeom.CreatePurposeAttr(UsdGeom.Tokens.guide)

    # rendering shape
    renderSphere = rigidCompoundPath + "/renderingSphere"

    sphereGeom = UsdGeom.Sphere.Define(stage, renderSphere)
    # sphereGeom.CreateSizeAttr(20.0)
    sphereGeom.AddTranslateOp().Set(shapePos)
    sphereGeom.AddOrientOp().Set(shapeQuat)

    # define physics material
    materialPath = "/material"
    mu = 1.0
    UsdShade.Material.Define(stage, materialPath)
    material = UsdPhysics.MaterialAPI.Apply(stage.GetPrimAtPath(materialPath))
    material.CreateStaticFrictionAttr().Set(mu)
    material.CreateDynamicFrictionAttr().Set(mu)
    material.CreateRestitutionAttr().Set(0.0)
    material.CreateDensityAttr().Set(1000.0)

    collisionAPI = UsdPhysics.CollisionAPI.Get(stage, collisionShape)

    # add the material to the collider
    bindingAPI = UsdShade.MaterialBindingAPI.Apply(collisionAPI.GetPrim())
    materialPrim = material.GetPrim()
    material = UsdShade.Material(materialPrim)
    bindingAPI.Bind(material, UsdShade.Tokens.weakerThanDescendants, "physics")

    stage.Save()