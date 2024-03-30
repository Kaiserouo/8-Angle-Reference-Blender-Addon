"""
    Main menu for this addon
    
    (for making reference for Destiny 2 originally)
"""

from ..utils import utils_d2ref as utils
import bpy
from bpy_extras.io_utils import ImportHelper
import collections

class D2AddDefaultCameraAndLight(bpy.types.Operator):
    """
        Add a default camera and some light into the scene.
        i.e., a camera for portrait (set to 1080x1920) and 2 sun light from front and back
    """
    # (For my own personal use originally, this should work on most destiny 2 models, or generally
    #  a model that resides in global origin)

    bl_idname = "eight_angle_reference.d2ref_add_default_camera_and_light"
    bl_label = "Add default camera and lights"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        utils.addDefaultCameraAndLight(context)
        return {'FINISHED'}

class D2MakeEightReferenceCameraStereoscopy(bpy.types.Operator):
    """
        Given active object as camera, make 8 cameras and set the
        stereroscopy multiview to those 8 cameras, rotating along global Z axis.
        The suffix will be "_1" ~ "_8".

        i.e., now when you render and save as "a.jpg", you will get all 8 images
              as "a_1.jpg" ~ "a_8.jpg".
        
        WILL RUIN YOUR CURRENT STEREOSCOPY! Don't use this addon if you're using that
        in other ways.
        
        Make sure to set one of the generated cameras as active camera before rendering,
        in order for stereoscopy to take effect.

        ref. https://www.youtube.com/watch?v=GX5YnybYFSI
    """
    bl_idname = "eight_angle_reference.d2ref_make_ref_cam_stereoscopy"
    bl_label = "Make 8 Camera & Stereoscopy from Active Camera Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.active_object.type != 'CAMERA':
            raise Exception('Active item should be a camera. Did you actively select a camera?')
        utils.makeEightReferenceCameraStereoscopy(context, context.active_object)
        return {'FINISHED'}

class D2SetupWholeScene(bpy.types.Operator):
    """
        Setup all the scene. Including:
        1. Add default camera and light (also set the active object to camera)
        2. Make 8 reference camera by default
        3. Set the rendering output to JPEG

        If the model size fits the default camera frame, you should be able to directly
        click F12 to render and save the 8 images all at once after this.
    """
    bl_idname = "eight_angle_reference.d2ref_setup_whole_scene"
    bl_label = "Setup the Whole Scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        camera = utils.addDefaultCameraAndLight(context)
        # manually update or the camera's matrix world won't be updated
        context.evaluated_depsgraph_get().update()
        utils.makeEightReferenceCameraStereoscopy(context, camera)
        utils.setRenderingToJpeg(context)
        return {'FINISHED'}



register_classes = [
    D2AddDefaultCameraAndLight,
    D2MakeEightReferenceCameraStereoscopy, 
    D2SetupWholeScene
]

def draw_menu(layout):
    layout.operator(D2AddDefaultCameraAndLight.bl_idname)
    layout.operator(D2MakeEightReferenceCameraStereoscopy.bl_idname)
    layout.operator(D2SetupWholeScene.bl_idname)