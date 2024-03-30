"""
    util functions for destiny
"""

import bpy
from math import radians
from mathutils import Matrix
from typing import *


def RotateGlobalZAxis(obj: bpy.types.Object, angle_deg: float):
    """
        ref. https://blender.stackexchange.com/questions/44760/rotate-objects-around-their-origin-along-a-global-axis-scripted-without-bpy-op
    """
    # define some rotation
    rot_mat = Matrix.Rotation(radians(angle_deg), 4, 'Z')   # you can also use as axis Y,Z or a custom vector like (x,y,z)

    # decompose world_matrix's components, and from them assemble 4x4 matrices
    orig_loc, orig_rot, orig_scale = obj.matrix_world.decompose()
    orig_loc_mat = Matrix.Translation(orig_loc)
    orig_rot_mat = orig_rot.to_matrix().to_4x4()
    orig_scale_mat = Matrix.Scale(orig_scale[0],4,(1,0,0)) * Matrix.Scale(orig_scale[1],4,(0,1,0)) @ Matrix.Scale(orig_scale[2],4,(0,0,1))

    # assemble the new matrix
    # rot_mat is at last because we are dealing with global axis, so location should rotate, too
    obj.matrix_world = rot_mat @ orig_loc_mat @ orig_rot_mat @ orig_scale_mat 
    
def setStereoscopyMultiview(scene: bpy.types.Scene, suffix_ls: List[str]):
    """
        set the stereoscopy multiview to those list,
        i.e., no matter what the name in stereoscopy is, there will be exactly
              len(suffix_ls) > 2 views in there, and the suffix of those views
              will be those in suffix_ls
        also turns on the stereoscopy btw
    """
    if len(suffix_ls) < 2:
        raise Exception(f'setStereoscopyMultiview: {len(suffix_ls) = } < 2')

    # stereoscopy
    scene.render.use_multiview = True
    scene.render.views_format = 'MULTIVIEW'
    
    # add / delete the views to the specified amount
    expected_count = len(suffix_ls)
    view_list = list(scene.render.views)
    if len(view_list) < expected_count:
        for i in range(expected_count - len(view_list)):
            scene.render.views.new("")
    elif len(view_list) > expected_count:
        for view in view_list[expected_count+1:]:
            scene.render.views.remove(view)

    # change all view suffix to suffix_ls
    for i, suffix in enumerate(suffix_ls):
        scene.render.views[i].camera_suffix = suffix

def makeEightReferenceCameraStereoscopy(context: bpy.types.Context, camera: bpy.types.Object):
    """
        Given a camera object, do the following:
            - Make 8 cameras, rotating 45 degree * i related to global Z axis
            - Add those 8 cameras to stereoscopy multiview
            - Set the first camera (i.e., the copy of your given camera) as active
        Now if you render it should render 8 pieces at once. When you save the image
        as 'a.jpg' you will get 'a_1.jpg' ~ 'a_8.jpg' all at once.

        ref. https://www.youtube.com/watch?v=GX5YnybYFSI
    """
    if camera.type != 'CAMERA':
        raise Exception('Expected a object with type "CAMERA"')
    
    scene = context.scene
    
    # make a collection for all our cameras
    collection = bpy.data.collections.new("D2Ref_CameraCollection")
    context.scene.collection.children.link(collection)
    
    # add all cameras, with predetermined names
    cameras = []
    for i in range(8):
        new_camera = camera.copy()
        new_camera.name = f'D2Ref_Camera_{i+1}'
        collection.objects.link(new_camera)
        RotateGlobalZAxis(new_camera, 45 * i)
        cameras.append(new_camera)
    
    setStereoscopyMultiview(scene, [f"_{i+1}" for i in range(8)])

    # set the first camera as active
    scene.camera = cameras[0]

def addDefaultCameraAndLight(context: bpy.types.Context):
    """
        add the default camera and light into the scene, i.e.:
            1. set the rendering to 1080x1920 (portrait)
            2. add camera and set to active
            3. add some lights
        returns the camera object
    """
    context.scene.render.resolution_x = 1080
    context.scene.render.resolution_y = 1920

    # make a collection for out things
    collection = bpy.data.collections.new("D2Ref_DefaultCameraAndLight")
    context.scene.collection.children.link(collection)
    
    # make camera
    camera_data = bpy.data.cameras.new("D2Ref_DefaultCamera")
    camera = bpy.data.objects.new("D2Ref_DefaultCamera", camera_data)
    collection.objects.link(camera)
    camera.location = (0, -3, 1.5)
    camera.rotation_mode = "XYZ"
    camera.rotation_euler = (radians(80), 0, 0)
    context.scene.camera = camera
    context.view_layer.objects.active = camera

    # make 2 sun light for front and back
    light1_data = bpy.data.lights.new(name="D2Ref_DefaultSunLight1", type='SUN')
    light1_data.energy = 10
    light1 = bpy.data.objects.new("D2Ref_DefaultCamera", light1_data)
    collection.objects.link(light1)
    light1.rotation_mode = "XYZ"
    light1.rotation_euler = (radians(-40), 0, 0)

    light2_data = bpy.data.lights.new(name="D2Ref_DefaultSunLight2", type='SUN')
    light2_data.energy = 10
    light2 = bpy.data.objects.new("D2Ref_DefaultCamera", light2_data)
    collection.objects.link(light2)
    light2.rotation_mode = "XYZ"
    light2.rotation_euler = (radians(40), 0, 0)

    return camera
    
def setRenderingToJpeg(context: bpy.types.Context):
    context.scene.render.image_settings.file_format = 'JPEG'

# camera = addDefaultCameraAndLight(bpy.context)
# # mandatory scene update to actually make camera.matrix_world valid
# # https://blender.stackexchange.com/questions/258000/how-to-update-world-transformation-matrices-without-calling-a-scene-update
# bpy.context.evaluated_depsgraph_get().update()
# makeEightReferenceCameraStereoscopy(bpy.context, camera)