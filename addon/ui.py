import bpy
from . import util 

class LGH_PT_ToolPanel(bpy.types.Panel):
    bl_label = "Light Groups"
    bl_region_type = "UI"
    bl_category = "Estella"
    bl_space_type = "VIEW_3D"

    def draw(
        self,
        context,
    ):
        layout = self.layout
        row = layout.row()
        row.alignment = "CENTER"
        row.menu("lgh.lightgroup_menu")
        row.enabled = bool(context.selected_objects)
        row.separator()
        row = layout.row()
        row.operator("view.reset_solo_lightgroup")

        self.draw_all_lightgroups(context, layout)

    def draw_single_lightgroup(self, view_layer, obj, layout):
        row = layout.row(align=True)
        # solo light in light group
        solo = row.operator("view.solo_light_in_lightgroup", text="", icon="EVENT_S")
        solo.lightgroup = obj.lightgroup
        solo.obj_name = obj.name
        row.separator()
        # select objects
        row.operator(
            "view.set_active_obj",
            icon="OBJECT_DATA" if obj.type != "LIGHT" else "LIGHT",
            text=obj.name,
        ).obj_name = obj.name
        row.separator()
        # object property
        row.prop(obj, "hide_viewport", text="")
        row.prop(obj, "hide_render", text="")

    def draw_all_lightgroups(self, context, layout):
        for lightgroup_item in context.view_layer.lightgroups:
            fit_list = util.get_obj_list_in_lightgroup(lightgroup_item.name)
            col = layout.box().column(align=True)
            col.use_property_split = True
            col.use_property_decorate = False

            row = col.row(align=True)
            row.scale_x = 1.15
            row.operator(
                "view.solo_lightgroup_object", text="", icon="EVENT_S"
            ).lightgroup = lightgroup_item.name
            row.separator(factor=1)
            row.operator(
                "lgh.rename_light_group", text=lightgroup_item.name
            ).lightgroup_name = lightgroup_item.name

            row.separator(factor=2)

            row.operator(
                "view.toggle_lightgroup_visibility", icon="HIDE_OFF", text=""
            ).lightgroup = lightgroup_item.name
            row.operator(
                "view.select_obj_by_lightgroup", text="", icon="RESTRICT_SELECT_OFF"
            ).lightgroup = lightgroup_item.name

            row.separator(factor=2)
            row.operator(
                "lgh.remove_light_group", icon="X", text=""
            ).lightgroup_name = lightgroup_item.name

            col.separator()

            if len(fit_list) == 0:
                col.label(text="Nothing in this Light Group")

            for obj in fit_list:
                self.draw_single_lightgroup(context.view_layer, obj, col)


class LGH_PT_ObjectPanel(bpy.types.Panel):
    bl_label = "Object"
    bl_region_type = "UI"
    bl_category = "Estella"
    bl_space_type = "VIEW_3D"

    def draw(self, context):
        ob = context.object
        view_layer = context.view_layer

        if ob is None and not hasattr(ob, "lightgroup"):
            return
        layout = self.layout
        col = layout.column(align=True)
        col.use_property_split = True
        col.use_property_decorate = False

        col.prop(ob, "name", icon="OBJECT_DATA" if ob.type != "LIGHT" else "LIGHT")
        col.prop_search(ob, "lightgroup", view_layer, "lightgroups", text="Light Group")

        col = layout.box().column(align=True)
        col.use_property_split = True
        col.use_property_decorate = False

        col.label(text="Visibility")
        row = col.row(align=True)
        row.scale_y = 1.15
        row.scale_x = 1.25
        row.alignment = "CENTER"
        row.prop(
            ob,
            "hide_select",
            text="",
        )
        row.prop(
            ob,
            "hide_viewport",
            text="",
        )
        row.prop(
            ob,
            "hide_render",
            text="",
        )
        row.prop(ob, "is_holdout", text="", icon="HOLDOUT_ON")
        row.prop(ob, "is_shadow_catcher", text="", icon="GHOST_ENABLED")

        col.separator()

        col.label(text="Ray Visibility")
        row = col.row(align=True)
        row.scale_y = 1.15
        row.scale_x = 1.25
        row.alignment = "CENTER"
        row.prop(ob, "visible_camera", text="", icon="CAMERA_DATA")
        row.prop(ob, "visible_diffuse", text="", icon="SHADING_SOLID")
        row.prop(ob, "visible_glossy", text="", icon="NODE_MATERIAL")
        row.prop(ob, "visible_transmission", text="", icon="MATERIAL")
        row.prop(ob, "visible_volume_scatter", text="", icon="VOLUME_DATA")

        col.separator()

        col.label(text="Viewport Display")
        row = col.row(align=True)
        row.scale_y = 1.15
        row.scale_x = 1.25
        row.alignment = "CENTER"
        row.prop(ob, "show_name", icon="EVENT_N", text="")
        row.prop(ob, "show_axis", icon="EMPTY_AXIS", text="")
        row.prop(ob, "show_wire", icon="MOD_WIREFRAME", text="")
        row.prop(ob, "show_in_front", icon="AXIS_FRONT", text="")
        row = col.row(align=True)
        row.scale_y = 1.15
        row.scale_x = 1.25
        row.alignment = "CENTER"
        row.prop(ob, "display_type")

class ESTELLA_UL_light_linking(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        scene = data
        light = item

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(light, "name", text="", emboss=False, icon_value=layout.icon(light))

    def filter_items(self, context, data, property):
        objects = getattr(data, property)
        filter_flags = [0] * len(objects)
        visible = 1 << 30

        for i, obj in enumerate(objects):
            if obj.type == "LIGHT":
                filter_flags[i] = visible

        return filter_flags, ()

class ESTELLA_PT_LightLinking(bpy.types.Panel):
    bl_label = "Light Linking"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scene = context.scene
        row.template_list("ESTELLA_UL_light_linking", 
                          "", 
                          scene,
                          "objects", 
                          scene, 
                          "light_index")

        if scene.light_index:
            object = scene.objects[scene.light_index]
            light_linking = object.light_linking

            col = row.column()
            col.template_ID(
                light_linking,
                "receiver_collection",
                new="estella.light_linking_receiver_collection_new")
            col.template_light_linking_collection(row, light_linking, "receiver_collection")

            col = row.column()
            sub = col.column(align=True)
            prop = sub.operator("object.light_linking_receivers_link", icon='ADD', text="")
            prop.link_state = 'INCLUDE'
            sub.operator("object.light_linking_unlink_from_collection", icon='REMOVE', text="")
            sub = col.column()
            sub.menu("CYCLES_OBJECT_MT_light_linking_context_menu", icon='DOWNARROW_HLT', text="")

class ESTELLA_PT_ShadowLinking(bpy.types.Panel):
    bl_label = "Shadow Linking"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scene = context.scene
        row.template_list("ESTELLA_UL_light_linking", 
                          "", 
                          scene,
                          "objects", 
                          scene, 
                          "light_index")

        if scene.light_index:
            object = scene.objects[scene.light_index]
            light_linking = object.light_linking

            col = row.column()
            col.template_ID(
                light_linking,
                "blocker_collection",
                new="estella.light_linking_blocker_collection_new")
            col.template_light_linking_collection(row, light_linking, "blocker_collection")

            col = row.column()
            sub = col.column(align=True)
            prop = sub.operator("object.light_linking_blockers_link", icon='ADD', text="")
            prop.link_state = 'INCLUDE'
            sub.operator("object.light_linking_unlink_from_collection", icon='REMOVE', text="")
            sub = col.column()
            sub.menu("CYCLES_OBJECT_MT_shadow_linking_context_menu", icon='DOWNARROW_HLT', text="")

classes = [
    LGH_PT_ToolPanel, 
    LGH_PT_ObjectPanel,
    ESTELLA_UL_light_linking,
    ESTELLA_PT_LightLinking,
    ESTELLA_PT_ShadowLinking
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.light_index = bpy.props.IntProperty()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.light_index
