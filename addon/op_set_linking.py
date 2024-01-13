import bpy

# Wrapper for object.light_linking_receiver_collection_new
# to automatically set the active object
class ESTELLA_OT_light_linking_new_reciever_collection(bpy.types.Operator):
    bl_label = "Create New Light Linking Reciever Collection"
    bl_idname = "estella.light_linking_receiver_collection_new"
    
    def execute(self, context):
        scene = context.scene
        active = context.active_object
        light = scene.objects[scene.light_index]
        context.view_layer.objects.active = light
        res = bpy.ops.object.light_linking_receiver_collection_new()
        context.view_layer.objects.active = active
        return res

# Wrapper for object.light_linking_blocker_collection_new
# to automatically set the active object
class ESTELLA_OT_light_linking_new_blocker_collection(bpy.types.Operator):
    bl_label = "Create New Light Linking Blocker Collection"
    bl_idname = "estella.light_linking_blocker_collection_new"
    
    def execute(self, context):
        scene = context.scene
        active = context.active_object
        light = scene.objects[scene.light_index]
        context.view_layer.objects.active = light
        res = bpy.ops.object.light_linking_blocker_collection_new()
        context.view_layer.objects.active = active
        return res

classes = [
    ESTELLA_OT_light_linking_new_reciever_collection,
    ESTELLA_OT_light_linking_new_blocker_collection
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
