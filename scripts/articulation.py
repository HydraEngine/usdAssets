#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import sys

from pxr import UsdGeom, Gf, UsdPhysics, Usd, Sdf

if __name__ == '__main__':
    stage = Usd.Stage.CreateNew("articulation.usda")
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

    radius = 1.0
    halfHeight = 1.0
    color = Gf.Vec3f(0.4, 0.2, 0.1)
    nbBoxes = 15

    initPos = Gf.Vec3f(0.0, 0.0, 24.0)
    pos = Gf.Vec3f(0.0, 0.0, 0.0)

    # setup the articulation as a parent of the hierarchy
    UsdGeom.Xform.Define(stage, "/articulation")
    UsdPhysics.ArticulationRootAPI.Apply(stage.GetPrimAtPath("/articulation"))

    parentName = "/articulation"

    # Create chain
    for i in range(nbBoxes):
        # articulation link
        linkName = "/articulation/articulationLink" + str(i)

        # capsule geom
        capsuleGeom = UsdGeom.Capsule.Define(stage, linkName)
        capsulePrim = stage.GetPrimAtPath(linkName)
        capsuleGeom.CreateHeightAttr(halfHeight)
        capsuleGeom.CreateRadiusAttr(radius)
        capsuleGeom.CreateAxisAttr("X")
        capsuleGeom.AddTranslateOp().Set(initPos + pos)
        capsuleGeom.AddOrientOp().Set(Gf.Quatf(1.0))
        capsuleGeom.AddScaleOp().Set(Gf.Vec3f(1.0, 1.0, 1.0))
        capsuleGeom.CreateDisplayColorAttr().Set([color])

        # articulation link is just a regular rigid body
        UsdPhysics.CollisionAPI.Apply(capsulePrim)
        UsdPhysics.RigidBodyAPI.Apply(capsulePrim)

        if i != 0:
            articulatedJointName = "/articulation/articulatedRevoluteJoint" + str(i)

            # joint definition between the articulation links
            component = UsdPhysics.RevoluteJoint.Define(stage, articulatedJointName)
            val0 = [Sdf.Path(parentName)]
            val1 = [Sdf.Path(linkName)]

            if parentName != "":
                component.CreateBody0Rel().SetTargets(val0)
            component.CreateLocalPos0Attr().Set(Gf.Vec3f(radius + halfHeight, 0.0, 0.0))
            component.CreateLocalRot0Attr().Set(Gf.Quatf(1.0))

            component.CreateBody1Rel().SetTargets(val1)
            component.CreateLocalPos1Attr().Set(Gf.Vec3f(-(radius + halfHeight), 0.0, 0.0))
            component.CreateLocalRot1Attr().Set(Gf.Quatf(1.0))

            component.CreateBreakForceAttr().Set(sys.float_info.max)
            component.CreateBreakTorqueAttr().Set(sys.float_info.max)

            component.CreateAxisAttr("Y")
            component.CreateLowerLimitAttr(float(-3.14 / 32.0))
            component.CreateUpperLimitAttr(float(3.14 / 32.0))

        else:
            # create the root joint
            articulatedJointName = "/articulation/rootJoint"
            component = UsdPhysics.FixedJoint.Define(stage, articulatedJointName)

            val1 = [Sdf.Path(linkName)]
            component.CreateLocalPos0Attr().Set(initPos)
            component.CreateLocalRot0Attr().Set(Gf.Quatf(1.0))

            component.CreateBody1Rel().SetTargets(val1)
            component.CreateLocalPos1Attr().Set(Gf.Vec3f(0.0, 0.0, 0.0))
            component.CreateLocalRot1Attr().Set(Gf.Quatf(1.0))

            component.CreateBreakForceAttr().Set(sys.float_info.max)
            component.CreateBreakTorqueAttr().Set(sys.float_info.max)

        parentName = linkName
        pos[0] += (radius + halfHeight) * 2.0

    stage.Save()