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

from .extensions import queryExtensions
extensions = []

def register():
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