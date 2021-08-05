from io_scene_gltf2.io.com.gltf2_io_extensions import Extension

class OMIAudioEmitterExtension:

    def gather_gltf_hook(self, gltf2_object, export_settings):
        if gltf2_object.extensions is None:
                gltf2_object.extensions = {}

        gltf2_object.extensions["OMI_audio_emitter"] = Extension(
            name="OMI_audio_emitter",
            extension={
                "audioEmitters": 1,
                "audioClips": 1
            },
            required=False
        )

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        if gltf2_object.extensions is None:
            gltf2_object.extensions = {}

        gltf2_object.extensions["OMI_audio_emitter"] = Extension(
            name="OMI_audio_emitter",
            extension={"test": 123},
            required=False
        )