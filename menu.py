from . import config
import bpy
from bpy_extras.io_utils import ImportHelper
import collections
import itertools

"""
    import all menus
    all menu py file should have "register_classes: List[class]" to register all classes
    and "draw_menu(layout)" for the submenu to call
"""
from .menus import menu_d2ref

menu_py_list = [
    menu_d2ref
]

# class contains everything that is not a submenu
# used for (un)registering
classes = list(itertools.chain.from_iterable([m.register_classes for m in menu_py_list]))

class Submenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_eight_angle_reference_submenu"
    bl_label = "8 Angle Reference"

    def draw(self, context):
        layout = self.layout
        for i, m in enumerate(menu_py_list):
            if i != 0:
                layout.separator()
            m.draw_menu(layout)

def menu_func(self, context):
    layout = self.layout
    layout.menu(Submenu.bl_idname)

def register():
    for c in classes:
        if c != None:
            bpy.utils.register_class(c)
    bpy.utils.register_class(Submenu)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)
    bpy.types.VIEW3D_MT_pose_context_menu.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(menu_func)
    bpy.utils.unregister_class(Submenu)
    for c in classes:
        if c != None:
            bpy.utils.unregister_class(c)