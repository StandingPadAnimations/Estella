# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Estalla",
    "author": "Forked by Mahid Sheikh, originally written by Atticus",
    "blender": (3, 2, 0),
    "version": (0, 5),
    "category": "Lighting",
    "support": "COMMUNITY",
    "doc_url": "",
    "tracker_url": "",
    "description": "A simple script to help you manage your light groups",
    "warning": "",
    "location": "3D View N Panel",
}

from . import op_set_obj, op_set_lightgroup, set_comp_nodes, ui


def register():
    op_set_obj.register()
    op_set_lightgroup.register()
    set_comp_nodes.register()
    ui.register()


def unregister():
    op_set_obj.register()
    op_set_lightgroup.register()
    set_comp_nodes.register()
    ui.register()


if __name__ == "__main__":
    register()
