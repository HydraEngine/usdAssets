#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Gf

if __name__ == '__main__':
    refStage = Usd.Stage.CreateNew('override_bunny_collider.usda')
    UsdGeom.SetStageUpAxis(refStage, UsdGeom.Tokens.y)

    meshPrim = refStage.OverridePrim('/MeshRef')
    meshPrim.GetReferences().AddReference('../assets/bunny.usda', "/bunny/Node/Mesh")
    overMesh = UsdGeom.Mesh.Get(refStage, '/MeshRef')
    overMesh.CreateDisplayColorAttr().Set([Gf.Vec3f(165.0 / 255.0, 21.0 / 255.0, 21.0 / 255.0)])

    physicsAPI = UsdPhysics.RigidBodyAPI.Apply(meshPrim)

    # set it as collision
    collisionAPI = UsdPhysics.CollisionAPI.Apply(meshPrim)
    collisionAPI.CreateCollisionEnabledAttr().Set(True)

    meshCollisionAPI = UsdPhysics.MeshCollisionAPI.Apply(meshPrim)
    meshCollisionAPI.CreateApproximationAttr(UsdPhysics.Tokens.convexDecomposition)

    # define physics material
    materialPath = "/material"
    mu = 1.0
    UsdShade.Material.Define(refStage, materialPath)
    material = UsdPhysics.MaterialAPI.Apply(refStage.GetPrimAtPath(materialPath))
    material.CreateStaticFrictionAttr().Set(mu)
    material.CreateDynamicFrictionAttr().Set(mu)
    material.CreateRestitutionAttr().Set(0.0)
    material.CreateDensityAttr().Set(1000.0)

    # add the material to the collider
    bindingAPI = UsdShade.MaterialBindingAPI.Apply(collisionAPI.GetPrim())
    materialPrim = material.GetPrim()
    material = UsdShade.Material(materialPrim)
    bindingAPI.Bind(material, UsdShade.Tokens.weakerThanDescendants, "physics")

    # Save the modified stage to a new USD file
    refStage.GetRootLayer().Save()