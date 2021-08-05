from .extensions.OMI_audio_emitter import OMIAudioEmitterExtension
from .extensions.OMI_physics import OMIPhysicsExtension

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

extensions = []

def register():
    # TODO: Dynamically load and instantiate extensions
    extensions = [
        OMIAudioEmitterExtension(),
        OMIPhysicsExtension()
    ]

def unregister():
    extensions = []

class glTF2ExportUserExtension:

    def gather_gltf_hook(self, gltf2_object, export_settings):
        for extension in extensions:
            extension.gather_gltf_hook(gltf2_object, export_settings)

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        for extension in extensions:
            extension.gather_node_hook(gltf2_object, blender_object, export_settings)