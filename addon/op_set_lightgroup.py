import bpy


class LGH_OT_create_light_group(bpy.types.Operator):
    bl_idname = "lgh.create_light_group"
    bl_label = "New Light Group"
    bl_description = "Create a new light group with the selected objects"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0 and context.object is not None

    def execute(self, context):
        bpy.ops.scene.view_layer_add_lightgroup()
        target_lightgroup = context.view_layer.lightgroups[-1].name

        for obj in context.selected_objects:
            obj.lightgroup = target_lightgroup
        return {"FINISHED"}


class LGH_OT_set_light_group(bpy.types.Operator):
    bl_idname = "lgh.set_light_group"
    bl_label = "Set Light Group"
    bl_description = "Set light group of selected object"

    target: bpy.props.StringProperty(name="Target Light Group", default="")

    def execute(self, context):
        for obj in context.selected_objects:
            obj.lightgroup = self.target
        return {"FINISHED"}


class LGH_MT_LightgroupMenu(bpy.types.Menu):
    bl_idname = "lgh.lightgroup_menu"
    bl_label = "Set Light Group for Object"
    bl_description = "Select or create a new light group for the selected objects"

    def draw(self, context):
        layout = self.layout
        layout.operator("lgh.create_light_group", icon="ADD")

        for group in context.view_layer.lightgroups:
            option = layout.operator(
                "lgh.set_light_group", icon="LIGHT", text=group.name
            )
            option.target = group.name


class LGH_OT_rename_light_group(bpy.types.Operator):
    bl_idname = "lgh.rename_light_group"
    bl_label = "Rename"
    bl_option = {"UNDO_GROUPED"}

    lightgroup_name: bpy.props.StringProperty(name="Light Group Name")
    new_name: bpy.props.StringProperty(name="New Name", default="")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "new_name")

    def execute(self, context):
        from .util import get_obj_list_in_lightgroup

        # Get all objects from the lightgroup. This
        # is because Blender doesn't provide a native
        # way of renaming light groups
        fit_list = get_obj_list_in_lightgroup(self.lightgroup_name)
        if self.new_name in [lg.name for lg in context.view_layer.lightgroups]:
            self.report({"ERROR"}, "Light Group Already Exists")
            return {"CANCELLED"}

        context.view_layer.lightgroups[self.lightgroup_name].name = self.new_name

        # We have to reassign all objects to the
        # renamed lightgroup cause again, Blender
        # doesn't provide a native function for this
        for obj in fit_list:
            obj.lightgroup = self.new_name
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        self.new_name = self.lightgroup_name
        return wm.invoke_props_dialog(self)


class LGH_OT_remove_light_group(bpy.types.Operator):
    bl_idname = "lgh.remove_light_group"
    bl_label = "Remove"
    bl_option = {"UNDO_GROUPED"}

    lightgroup_name: bpy.props.StringProperty(name="Light Group Name")

    def execute(self, context):
        for i, lightgroup_item in enumerate(context.view_layer.lightgroups):
            if lightgroup_item.name == self.lightgroup_name:
                bpy.ops.scene.view_layer_remove_lightgroup(i)
                break

        from .util import get_obj_list_in_lightgroup

        # Get all objects in the lightgroup
        # so we don't leave the field populated
        fit_list = get_obj_list_in_lightgroup(self.lightgroup_name)
        for obj in fit_list:
            obj.lightgroup = ""

        return {"FINISHED"}


classes = [
    LGH_OT_create_light_group,
    LGH_MT_LightgroupMenu,
    LGH_OT_set_light_group,
    LGH_OT_rename_light_group,
    LGH_OT_remove_light_group,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
