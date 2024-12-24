#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from pxr import Usd, UsdGeom, UsdPhysics

if __name__ == '__main__':
    # Load the existing USD file
    stage = Usd.Stage.Open("../bunny.usda")

    # Get the mesh prim that you want to add collision to
    mesh_prim = stage.GetPrimAtPath("/bunny/Node/Mesh")

    # Apply the Collision API to the mesh prim
    collision_api = UsdPhysics.CollisionAPI.Apply(mesh_prim)

    # Save the modified stage to a new USD file
    stage.Save()