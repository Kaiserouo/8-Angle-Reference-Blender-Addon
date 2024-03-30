bl_info = {
    "name": "8 Angle Refernce Blender Addon",
    "description": "Blender addon for fast setup and rendering for 8 angle reference.",
    "author": "Kaiserouo",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "View3D > Object Context Menu / Pose Context Menu > 8 Angle Reference",
    "doc_url": "https://github.com/Kaiserouo/Apex-Legends-Auto-Shader-Blender-Addon",
    "category": "Object"
}

import bpy
from . import menu

def register():
    menu.register()
    
def unregister():
    menu.unregister()

if __name__ == "__main__":
    register()