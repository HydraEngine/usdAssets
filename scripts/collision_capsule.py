#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from pxr import Usd, UsdGeom, Gf, UsdPhysics, UsdShade, Usd, Usd

if __name__ == '__main__':
    stage = Usd.Stage.CreateNew("collision_capsule.usda")
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    stage.SetEndTimeCode(1000)
    stage.SetStartTimeCode(0)

    # Physics scene definition
    scene = UsdPhysics.Scene.Define(stage, "/physicsScene")

    # setup gravity
    # note that gravity has to respect the selected units, if we are using cm, the gravity has to respect that
    scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, -1.0, 0.0))
    scene.CreateGravityMagnitudeAttr().Set(9.81)

    # ==================================================================================================================
    # Top level actor, contains rigid body
    rigidCompoundPath = "/compoundRigid"
    rigidXform = UsdGeom.Xform.Define(stage, rigidCompoundPath)
    rigidPrim = stage.GetPrimAtPath(rigidCompoundPath)

    # Rigid body transform
    rigidCompoundPos = Gf.Vec3f(0.0, 10.0, 0.0)
    rigidXform.AddTranslateOp().Set(rigidCompoundPos)
    rigidXform.AddOrientOp().Set(Gf.Quatf(1.0, 0.0, 0.0, 0.0))

    physicsAPI = UsdPhysics.RigidBodyAPI.Apply(rigidPrim)

    # Collision shape
    collisionShape = rigidCompoundPath + "/physicsCapsuleShape"

    shapePos = Gf.Vec3f(0.0)
    shapeQuat = Gf.Quatf(1.0)

    capsuleGeom = UsdGeom.Capsule.Define(stage, collisionShape)
    capsuleGeom.CreateRadiusAttr(30)
    capsuleGeom.CreateHeightAttr(60)
    capsuleGeom.CreateAxisAttr("Y")
    capsuleGeom.AddTranslateOp().Set(shapePos)
    capsuleGeom.AddOrientOp().Set(shapeQuat)
    # hide it from rendering
    # capsuleGeom.CreatePurposeAttr(UsdGeom.Tokens.guide)

    # set it as collision
    capsulePrim = stage.GetPrimAtPath(collisionShape)
    collisionAPI = UsdPhysics.CollisionAPI.Apply(capsulePrim)
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

    # ==================================================================================================================
    # box0 static
    boxActorPath = "/box0"

    # box0 props
    position = Gf.Vec3f(0.0, -50.0, 0.0)
    orientation = Gf.Quatf(1.0)
    color = Gf.Vec3f(165.0 / 255.0, 21.0 / 255.0, 21.0 / 255.0)
    size = 100.0
    scale = Gf.Vec3f(10, 0.1, 10)

    cubeGeom = UsdGeom.Cube.Define(stage, boxActorPath)
    cubeGeom.CreateSizeAttr(size)
    cubeGeom.AddTranslateOp().Set(position)
    cubeGeom.AddOrientOp().Set(orientation)
    cubeGeom.AddScaleOp().Set(scale)
    cubeGeom.CreateDisplayColorAttr().Set([color])

    # make it a static body - just apply PhysicsCollisionAPI
    cubePrim = stage.GetPrimAtPath(boxActorPath)
    UsdPhysics.CollisionAPI.Apply(cubePrim)

    stage.Save()
