import bpy

def get_visible_collections():
    def check_child(child, vis_cols):
        if child.is_visible:
            vis_cols.append(child.collection)
            for sub_child in child.children:
                vis_cols = check_child(sub_child, vis_cols)
        return vis_cols

    vis_cols = [bpy.context.scene.collection]

    for child in bpy.context.window.view_layer.layer_collection.children:
        check_child(child, vis_cols)

    return vis_cols


def get_obj_list_in_lightgroup(lightgroup_name):
    view_layer = bpy.context.view_layer

    coll_list = get_visible_collections()
    obj_list = list()

    for coll in coll_list:
        for obj in coll.all_objects:
            if obj.lightgroup != view_layer.lightgroups[lightgroup_name].name:
                continue
            obj_list.append(obj)

    return list(set(obj_list))
