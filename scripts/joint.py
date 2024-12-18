#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from pxr import UsdGeom, Gf, UsdPhysics, Usd

if __name__ == '__main__':
    stage = Usd.Stage.CreateNew("joint.usda")
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    stage.SetEndTimeCode(1000)
    stage.SetStartTimeCode(0)

    # Physics scene definition
    scene = UsdPhysics.Scene.Define(stage, "/physicsScene")

    # setup gravity
    # note that gravity has to respect the selected units, if we are using cm, the gravity has to respect that
    scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, -1.0, 0.0))
    scene.CreateGravityMagnitudeAttr().Set(9.81)

    # box0 static
    boxActorPath = "/box0"

    # box0 props
    cubeGeom = UsdGeom.Cube.Define(stage, boxActorPath)
    cubeGeom.CreateSizeAttr(10)
    cubeGeom.AddTranslateOp().Set(Gf.Vec3f(0.0, 0.0, 0.0))
    cubeGeom.AddOrientOp().Set(Gf.Quatf(1.0))
    cubeGeom.CreateDisplayColorAttr().Set([Gf.Vec3f(165.0 / 255.0, 21.0 / 255.0, 21.0 / 255.0)])

    # make it a static body - just apply PhysicsCollisionAPI
    cubePrim = stage.GetPrimAtPath(boxActorPath)
    UsdPhysics.CollisionAPI.Apply(cubePrim)

    # Box1 dynamic body
    boxActorPath = "/box1"

    cubeGeom = UsdGeom.Cube.Define(stage, boxActorPath)
    cubeGeom.CreateSizeAttr(100)
    cubeGeom.AddTranslateOp().Set(Gf.Vec3f(60.0, 0.0, 0.0))
    cubeGeom.AddOrientOp().Set(Gf.Quatf(1))
    cubeGeom.AddScaleOp().Set(Gf.Vec3f(0.1, 1, 0.1))
    cubeGeom.CreateDisplayColorAttr().Set([Gf.Vec3f(71.0 / 255.0, 165.0 / 255.0, 1.0)])

    # setup dynamic rigid body
    cubePrim = stage.GetPrimAtPath(boxActorPath)
    UsdPhysics.CollisionAPI.Apply(cubePrim)
    UsdPhysics.RigidBodyAPI.Apply(cubePrim)

    ##==================================================================================================================
    # create revolute joint prim
    revoluteJoint = UsdPhysics.RevoluteJoint.Define(stage, "/revoluteJoint")

    # define revolute joint axis and its limits, defined in degrees
    revoluteJoint.CreateAxisAttr("X")
    revoluteJoint.CreateLowerLimitAttr(-90.0)
    revoluteJoint.CreateUpperLimitAttr(90.0)

    # define revolute joint bodies
    revoluteJoint.CreateBody0Rel().SetTargets(["/box0"])
    revoluteJoint.CreateBody1Rel().SetTargets(["/box1"])

    # define revolute joint local poses for bodies
    orientation = Gf.Rotation([0, 1, 0], 90)
    revoluteJoint.CreateLocalPos0Attr().Set(Gf.Vec3f(0.0, 0.0, 0.0))
    revoluteJoint.CreateLocalRot0Attr().Set(Gf.Quatf(orientation.GetQuat()))

    revoluteJoint.CreateLocalPos1Attr().Set(Gf.Vec3f(-60.0, 0.0, 0.0))
    revoluteJoint.CreateLocalRot1Attr().Set(Gf.Quatf(orientation.GetQuat()))

    # set break force/torque
    revoluteJoint.CreateBreakForceAttr().Set(1e20)
    revoluteJoint.CreateBreakTorqueAttr().Set(1e20)

    ##==================================================================================================================
    # # create revolute joint prim
    # distanceJoint = UsdPhysics.DistanceJoint.Define(stage, "/distanceJoint")
    #
    # # define revolute joint axis and its limits, defined in degrees
    # distanceJoint.CreateMinDistanceAttr(-10)
    # distanceJoint.CreateMaxDistanceAttr(10.0)
    #
    # # define revolute joint bodies
    # distanceJoint.CreateBody0Rel().SetTargets(["/box0"])
    # distanceJoint.CreateBody1Rel().SetTargets(["/box1"])
    #
    # # define revolute joint local poses for bodies
    # distanceJoint.CreateLocalPos0Attr().Set(Gf.Vec3f(0.0, 60.0, 0.0))
    # distanceJoint.CreateLocalRot0Attr().Set(Gf.Quatf(1.0))
    #
    # distanceJoint.CreateLocalPos1Attr().Set(Gf.Vec3f(0.0, -60.0, 0.0))
    # distanceJoint.CreateLocalRot1Attr().Set(Gf.Quatf(1.0))
    #
    # # set break force/torque
    # distanceJoint.CreateBreakForceAttr().Set(1e20)
    # distanceJoint.CreateBreakTorqueAttr().Set(1e20)

    #===================================================================================================================
    # optionally add angular drive for example
    # angularDriveAPI = UsdPhysics.DriveAPI.Apply(stage.GetPrimAtPath("/revoluteJoint"), "angular")
    # angularDriveAPI.CreateTypeAttr("force")
    # angularDriveAPI.CreateMaxForceAttr(1e20)
    # angularDriveAPI.CreateTargetVelocityAttr(1.0)
    # angularDriveAPI.CreateDampingAttr(1e10)
    # angularDriveAPI.CreateStiffnessAttr(0.0)

    stage.Save()
