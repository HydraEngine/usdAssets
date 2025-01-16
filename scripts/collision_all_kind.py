#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.
import random

from pxr import UsdGeom, Gf, UsdPhysics, UsdShade, Usd


def createCube(stage: Usd.Stage, name: str, translate: Gf.Vec3f, orient: Gf.Quatf):
    rigidCompoundPath = "/compoundRigid" + name
    rigidXform = UsdGeom.Xform.Define(stage, rigidCompoundPath)
    rigidPrim = stage.GetPrimAtPath(rigidCompoundPath)

    # Rigid body transform
    rigidXform.AddTranslateOp().Set(translate)
    rigidXform.AddOrientOp().Set(orient)

    physicsAPI = UsdPhysics.RigidBodyAPI.Apply(rigidPrim)

    # Collision shape
    collisionShape = rigidCompoundPath + "/physicsBoxShape" + name

    size = 2.0
    shapePos = Gf.Vec3f(0.0)
    shapeQuat = Gf.Quatf(1.0)

    cubeGeom = UsdGeom.Cube.Define(stage, collisionShape)
    cubeGeom.CreateSizeAttr(size)
    cubeGeom.AddTranslateOp().Set(shapePos)
    cubeGeom.AddOrientOp().Set(shapeQuat)

    # set it as collision
    cubePrim = stage.GetPrimAtPath(collisionShape)
    collisionAPI = UsdPhysics.CollisionAPI.Apply(cubePrim)
    collisionAPI.CreateCollisionEnabledAttr().Set(True)

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


if __name__ == '__main__':
    stage = Usd.Stage.CreateNew("collision_all_kind.usda")
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    stage.SetEndTimeCode(1000)
    stage.SetStartTimeCode(0)

    # Physics scene definition
    scene = UsdPhysics.Scene.Define(stage, "/physicsScene")

    # setup gravity
    # note that gravity has to respect the selected units, if we are using cm, the gravity has to respect that
    scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, 0.0, -1.0))
    scene.CreateGravityMagnitudeAttr().Set(9.81)

    # ==================================================================================================================
    for i in range(10):
        for j in range(10):
            translate = Gf.Vec3f(i * 5 - 25, j * 5 - 25, 10)
            orient = Gf.Quatf(random.random(), random.random(), random.random(), random.random())
            createCube(stage, f"{i}{j}", translate, orient.GetNormalized())

    # ==================================================================================================================
    # plane static
    planeActorPath = "/plane"

    # plane props
    planeGeom = UsdGeom.Plane.Define(stage, planeActorPath)
    planeGeom.CreateAxisAttr("Z")
    planeGeom.CreateWidthAttr(100)
    planeGeom.CreateLengthAttr(100)
    planeGeom.CreateDisplayColorAttr().Set([Gf.Vec3f(165.0 / 255.0, 21.0 / 255.0, 21.0 / 255.0)])

    # make it a static body - just apply PhysicsCollisionAPI
    planePrim = stage.GetPrimAtPath(planeActorPath)
    UsdPhysics.CollisionAPI.Apply(planePrim)

    stage.Save()
