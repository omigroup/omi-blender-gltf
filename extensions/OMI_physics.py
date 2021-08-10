from . import OMIExtension

ID = "OMI_physics"
class OMIPhysicsExtension(OMIExtension):
    def gather_gltf_hook(self, gltf2_object, export_settings):
        if gltf2_object.extensions is None:
                gltf2_object.extensions = {}

        gltf2_object.extensions[ID] = Extension(
            name=ID,
            extension={"test": 1},
            required=False
        )

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        if gltf2_object.extensions is None:
            gltf2_object.extensions = {}

        gltf2_object.extensions[ID] = Extension(
            name=ID,
            extension={"test": 123},
            required=False
        )