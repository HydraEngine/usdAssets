#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from pxr import UsdGeom, Gf, UsdPhysics, UsdShade, Usd

if __name__ == '__main__':
    stage = Usd.Stage.CreateNew("composition.usda")
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
    rigidXform = UsdGeom.Xform.Define(stage, '/compoundRigid')

    # Rigid body transform
    rigidXform.AddTranslateOp().Set(Gf.Vec3f(0.0, 0.0, 10.0))
    rigidXform.AddOrientOp().Set(Gf.Quatf(1.0, 0.0, 0.0, 0.0))
    rigidXform.AddScaleOp().Set(Gf.Vec3f(25, 25, 25))

    meshPrim = stage.OverridePrim('/compoundRigid/MeshRef')
    meshPrim.GetReferences().AddReference('override_bunny_collider.usda', "/MeshRef")

    # ==================================================================================================================
    # box0 static
    boxActorPath = "/box0"

    # box0 props
    cubeGeom = UsdGeom.Cube.Define(stage, boxActorPath)
    cubeGeom.CreateSizeAttr(100.0)
    cubeGeom.AddTranslateOp().Set(Gf.Vec3f(0.0, 0.0, -50.0))
    cubeGeom.AddOrientOp().Set(Gf.Quatf(1.0))
    cubeGeom.AddScaleOp().Set(Gf.Vec3f(5, 5, 0.1))
    cubeGeom.CreateDisplayColorAttr().Set([Gf.Vec3f(165.0 / 255.0, 21.0 / 255.0, 21.0 / 255.0)])

    # make it a static body - just apply PhysicsCollisionAPI
    cubePrim = stage.GetPrimAtPath(boxActorPath)
    UsdPhysics.CollisionAPI.Apply(cubePrim)

    stage.Save()
