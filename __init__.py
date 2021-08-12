bl_info = {
    "name" : "OMI Blender Exporter",
    "author" : "OMI Group",
    "description" : "",
    "blender" : (2, 93, 1),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

from .extensions import queryExtensions, OMIExtension
extensions = []

def register():
    OMIExtension.autoregister(globals()) # register main panels below
    autodetected = queryExtensions()
    print("[OMI]", autodetected)
    for Ext in autodetected:
        if hasattr(Ext, 'register'):
            Ext.register()
        else:
            print("Warning -- no .register found", Ext)
        instance = Ext()
        # print("[OMI]", instance.__module__)
        extensions.append(instance)
    print("[OMI] extensions:", [ext.__module__ for ext in extensions])
    # class tmp: extensions = {}
    # extensions[0].gather_gltf_hook(tmp(), {})

def unregister():
    for extension in extensions:
        if hasattr(extension.__class__, 'unregister'):
            extension.__class__.unregister()
        else:
            print("Warning -- no .unregister found", extension.__class__)
    extensions = []

class glTF2ExportUserExtension:

    def gather_gltf_hook(self, gltf2_object, export_settings):
        for extension in extensions:
            extension.gather_gltf_hook(gltf2_object, export_settings)

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        for extension in extensions:
            extension.gather_node_hook(gltf2_object, blender_object, export_settings)

import bpy
class OMIObjectExtensions(bpy.types.Panel):
    bl_label = 'OMI Extensions'
    bl_idname = "NODE_PT_OMI_extensions"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    def draw(self, context):
        pass # self.layout.label(text="OMIObjectPanel")

class OMISceneExtensions(bpy.types.Panel):
    bl_label = 'OMI Extensions'
    bl_idname = "NODE_PT_OMI_scene_extensions"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    def draw(self, context):
        pass

### GLTF Export Screen
class OMIGLTFExportPanel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_idname = "OMI_GLTF_PT_export_user_extensions"
    bl_label = "OMI Extensions"
    bl_parent_id = "GLTF_PT_export_user_extensions"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw(self, context):
        pass

