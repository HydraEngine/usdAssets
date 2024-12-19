#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from pxr import UsdGeom, Gf, UsdPhysics, UsdShade, Usd

if __name__ == '__main__':
    stage = Usd.Stage.CreateNew("collision_mesh.usda")
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
    collisionShape = rigidCompoundPath + "/physicsBoxShape"

    size = 25.0
    shapePos = Gf.Vec3f(0.0)
    shapeQuat = Gf.Quatf(1.0)

    meshGeom = UsdGeom.Mesh.Define(stage, collisionShape)
    meshPrim = stage.GetPrimAtPath(collisionShape)
    meshGeom.AddTranslateOp().Set(shapePos)
    meshGeom.AddOrientOp().Set(shapeQuat)
    meshGeom.CreatePointsAttr(
        [Gf.Vec3f(1, 1, 1), Gf.Vec3f(0, 1, 0), Gf.Vec3f(1, 1, 0), Gf.Vec3f(0, 1, 1),
         Gf.Vec3f(1, 0, 1), Gf.Vec3f(0, 0, 0), Gf.Vec3f(1, 0, 0), Gf.Vec3f(0, 0, 1)])
    meshGeom.CreateFaceVertexIndicesAttr([
        3, 7, 6,
        2, 3, 6,
        8, 5, 1,
        8, 1, 4,
        2, 3, 1,
        2, 1, 4,
        6, 7, 5,
        6, 5, 8,
        7, 5, 1,
        7, 1, 3,
        6, 8, 4,
        6, 4, 2
    ])
    meshGeom.CreateFaceVertexCountsAttr([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])

    # set it as collision
    collisionAPI = UsdPhysics.CollisionAPI.Apply(meshPrim)
    collisionAPI.CreateCollisionEnabledAttr().Set(True)

    meshCollisionAPI = UsdPhysics.MeshCollisionAPI.Apply(meshPrim)
    meshCollisionAPI.CreateApproximationAttr(UsdPhysics.Tokens.convexDecomposition)

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
    scale = Gf.Vec3f(1, 0.1, 1)

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
