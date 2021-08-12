from . import OMIExtension
import bpy

ID = "OMI_audio_emitter"

class OMIAudioEmitterExtension(OMIExtension):
    def gather_gltf_hook(self, gltf2_object, export_settings):
        if gltf2_object.extensions is None:
            gltf2_object.extensions = {}
        gltf2_object.extensions[ID] = OMIExtension.Extension(
            name = ID,
            extension = {
                "#audioClips": len(bpy.types.Scene.OMI_audio_clips),
                #"#audioEmitters": len(bpy.data.objects) #[ obj in bpy.data.objects if obj.OMI_audio_emitter is not None ])
            },
            required = False
        )

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        if blender_object.OMI_audio_emitter is None:
            return
        if gltf2_object.extensions is None:
            gltf2_object.extensions = {}
        gltf2_object.extensions[ID] = OMIExtension.Extension(
            name = ID,
            extension =  {
              "name": "emitter",
              "type": "positional",
              "volume": 0.8,
              "loop": false,
            },
            required = False
        )

    @staticmethod
    def register():
        import os
        if os.environ.get("OMI_DEBUG", False): bpy.app.timers.register(omi_emitter_debug)
    
        OMIExtension.autoregister(globals())

        # audio clips arrays
        bpy.types.Scene.OMI_audio_clips = bpy.props.PointerProperty(type=AudioClipArrayProperty)

        # per-object audio emitter (... can "objects" have multiple emitters?)
        bpy.types.Object.OMI_audio_emitter = bpy.props.PointerProperty(type=AudioEmitterProperties)
        
        # scene audio emitters (... can "scenes" have multiple emitters)
        bpy.types.Scene.OMI_audio_emitter = bpy.props.PointerProperty(type=AudioEmitterProperties)
        # bpy.types.Scene.OMI_audio_emitters = bpy.props.PointerProperty(type=AudioEmitterArrayProperty)
        
    @staticmethod
    def unregister():
        raise "TODO... unregister not fully implemented yet"
        del bpy.types.Object.OMI_audio_emitter
        del bpy.types.Scene.OMI_audio_clips
        del bpy.types.Scene.OMI_audio_emitter
        
    @staticmethod
    def findClipByIndex(context, index):
        for clip in context.scene.OMI_audio_clips.value:
            if clip.index == index: return clip
        return None

# -- .audioClips
class AudioClipProperties(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty(name="index")
    name: bpy.props.StringProperty(name="name")
    filename: bpy.props.StringProperty(
        name="Audio File", description='Audio File', subtype='FILE_PATH'
    )

class AudioClipArrayProperty(bpy.types.PropertyGroup):
    value: bpy.props.CollectionProperty(name="value", type=AudioClipProperties)
    enabled: bpy.props.BoolProperty(name="enabled")

class AddAudioClip(bpy.types.Operator):
    bl_idname = "wm.add_audio_clip"
    bl_label = "Add Audio Clip"
    def execute(self, context):
        props = context.scene.OMI_audio_clips.value
        props.add()
        props[len(props)-1].index = len(props)-1
        return {'FINISHED'}

class RemoveAudioClip(bpy.types.Operator):
    bl_idname = "wm.remove_audio_clip"
    bl_label = "Remove Audio Clip"
    clip_index: bpy.props.IntProperty(name="index")
    def execute(self, context):
        props = context.scene.OMI_audio_clips.value
        for i, clip in enumerate(props):
            if clip.index == self.clip_index:
                # FIXME: should probably reset any emitters referencing the clip?
                props.remove(i)
                break;
        return {'FINISHED'}

# .audioEmitter
class AudioEmitterProperties(bpy.types.PropertyGroup):
    clip_index: bpy.props.IntProperty(name="clip_index", default=-1)
    volume: bpy.props.FloatProperty(name="Volume")
    muted: bpy.props.BoolProperty(name="Muted")
    type: bpy.props.EnumProperty(
        name='type',
        description='...',
        items={
            ('POSITIONAL', 'positional', 'Positional...'),
            ('GLOBAL', 'global', 'Global...'),
        },
        default='GLOBAL'
    )

class AudioEmitterArrayProperty(bpy.types.PropertyGroup):
    value: bpy.props.CollectionProperty(name="value", type=AudioEmitterProperties)

class PreviewEmitter(bpy.types.Operator):
    bl_idname = "wm.omi_preview_emitter"
    bl_label = "Preview"
    # object_path: bpy.props.StringProperty(name="object_path")

    target = None
    def execute(self, context):
        object = PreviewEmitter.target #findObjectByHash(context, self.object_path)
        emitter = object.OMI_audio_emitter
        clip = OMIAudioEmitterExtension.findClipByIndex(context, emitter.clip_index)
        self.report({'INFO'}, "TODO: Preview Emitter " + str(clip.filename if clip else clip) + "//"+str(clip))
        return {'FINISHED'}

class PreviewAudio(bpy.types.Operator):
    bl_idname = "wm.omi_preview_audio"
    bl_label = "Preview"
    clip_index: bpy.props.IntProperty(name="clip_index")
    # filename: bpy.props.StringProperty(name="audio file", description="audio file")

    def execute(self, context):
        props = context.scene.OMI_audio_clips.value
        # props = context.object.VariantMaterialArrayProperty.value
        # props.add()
        self.report({'INFO'}, "TODO: Preview Audio " + props[self.clip_index].filename)
        return {'FINISHED'}

class ClipsOperator(bpy.types.Operator):
    bl_idname = "wm.omi_clips_operator"
    bl_label = "Clip"
    def item_cb(self, context):  
        clips = [( "-1", "", "")]
        for clip in context.scene.OMI_audio_clips.value:
            clips.append((str(clip.index), clip.name, clip.name))
        return clips
    clip:  bpy.props.EnumProperty(items=item_cb)
    target = None
    def execute(self, context): 
        clip_index = int(self.clip)
        clip = OMIAudioEmitterExtension.findClipByIndex(context, clip_index)
        print("CLIPSOPERATOR", ClipsOperator.target, clip, clip_index)
        emitter = ClipsOperator.target.OMI_audio_emitter
        print(emitter, "EXECUTE", clip_index, self.clip, len(context.scene.OMI_audio_clips.value), context.scene.OMI_audio_clips.value)
        emitter.clip_index = clip_index
        self.report({'INFO'}, "OPERATOR: Select Clip " + str(clip.name if clip else None) +  "|" + str(emitter.clip_index))
        return {"FINISHED"}  

# Object custom property panel

class ObjectEmitterPanel(bpy.types.Panel):
    bl_label = 'Audio Emitter'
    bl_idname = "NODE_PT_OMI_object_audio_emitter"
    bl_parent_id = "NODE_PT_OMI_extensions"
    bl_space_type = 'PROPERTIES'
    # bl_options = {'HIDE_HEADER'}
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    def draw(self, context):
        box = self.layout.box()
        # box.label(text="asdfasdf")
        self._draw(context, box, context.object)

    def _draw(self, context, layout, object):
        emitter = object.OMI_audio_emitter
        clip = OMIAudioEmitterExtension.findClipByIndex(context, emitter.clip_index)
        ClipsOperator.target = object
        row = layout.split(factor=0.85)
        row.operator_menu_enum(ClipsOperator.bl_idname, "clip", text=clip.name if clip else "", icon="SCENE")
        op = row.operator("wm.omi_preview_emitter", icon="PLAY", text="")
        PreviewEmitter.target = object
        layout.label(text="index: " + str(emitter.clip_index))
        if True: #clip:
            layout.prop(emitter, 'type')
            layout.prop(emitter, 'volume')
            layout.prop(emitter, 'muted')
            # op = layout.operator("wm.omi_preview_emitter", icon="PLAY")
            # PreviewEmitter.target = object
        #op.object_path = hashObject(object)

# Scene custom property
class SceneAudioClipsPanel(bpy.types.Panel):
    bl_label = 'Audio Clips'
    bl_idname = "NODE_PT_OMI_scene_audio_clips"
    bl_parent_id = "NODE_PT_OMI_scene_extensions"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout
        for clip in context.scene.OMI_audio_clips.value:
            box = layout.box()
            row = box.row()
            preview_operator = row.operator("wm.omi_preview_audio", icon="PLAY")
            preview_operator.clip_index = clip.index
            remove_operator = row.operator("wm.remove_audio_clip", icon="X")
            remove_operator.clip_index = clip.index
            box.prop(clip, 'name')
            box.prop(clip, 'filename')
            #layout.separator()
        layout.operator(
            "wm.add_audio_clip",
            text="Add Audio Clip",
            icon="ADD"
        )

class SceneEmitterPanel(bpy.types.Panel):
    bl_label = 'Audio Emitter'
    bl_idname = "NODE_PT_OMI_scene_audio_emitter"
    bl_parent_id = "NODE_PT_OMI_scene_extensions"
    bl_space_type = 'PROPERTIES'
    # bl_options = {'HIDE_HEADER'}
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    def draw(self, context):
        ObjectEmitterPanel._draw(self, context, self.layout, context.scene)

### GLTF Export Screen
class OMIAudioGLTFExportPanel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "OMI Audio"
    bl_parent_id = "OMI_GLTF_PT_export_user_extensions"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw_header(self, context):
        self.layout.prop(bpy.context.scene.OMI_audio_clips, 'enabled', text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        props = bpy.context.scene.OMI_audio_clips
        layout.active = props.enabled

        box = layout.box()
        if len(bpy.context.scene.OMI_audio_clips.value) == 0:
            box.label(text="(scene has no audio clips)")

        for clip in bpy.context.scene.OMI_audio_clips.value:
            box.label(text=clip.name)

###########################################################################
# temporary testing -- env OMI_DEBUG=1 blender....
def omi_emitter_debug():
    scene = bpy.context.scene
    if len(scene.OMI_audio_clips.value) == 0:
        print("Adding test clip", scene.OMI_audio_clips.value)
        clip = scene.OMI_audio_clips.value.add()
        clip.name = "test clip"
        clip.filename = "test_clip.mp3"


# def hashObject(context, object):
#     return str(object.as_pointer())
# 
# def findObjectByHash(context, ptr):
#     if hashObject(context.scene) == ptr:
#         return context.scene
#     for obj in bpy.data.objects:
#         if hashObject(obj) == ptr:
#             return obj
#     return None
# 
