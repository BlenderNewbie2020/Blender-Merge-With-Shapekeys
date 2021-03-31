# Adapted from Narazaka's original code to export shapekeys https://github.com/Narazaka/blender-shapekey-exporter

import bpy
from bpy.props import *
from bpy.types import Scene

import mathutils
import itertools

bl_info = {
    "name" : "Merge Objects with Shapekeys",
    "author" : "BlenderNewbie2020",
    'category': 'Mesh',
    'location': 'View 3D > Tool Shelf > Object Merge',
    'warning': 'Requires more thorough testing and a more appropriate location.',
    'description': 'Given two objects with different geometry, attempts to join a first selected object with a second active object, replacing existing shapkeys.',
    "version" : (0, 1, 0),
    "blender" : (2, 79, 0),
    'tracker_url': 'https://github.com/BlenderNewbie2020/Blender-Merge-With-Shapekeys/issues',
}

class ObjectMerge_PT_Main(bpy.types.Panel):
    bl_idname = "object_merge.main"
    bl_label = "Object Merge"
    bl_category = "ObjectMerge"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        self.layout.operator(ObjectMerge_OT_Join.bl_idname)
        return None

class ObjectMerge_OT_Join(bpy.types.Operator, JoinHelper):
    bl_idname = "object_merge.join"
    bl_label = "Join"
    bl_options = {'REGISTER'}

    def execute(self, context):

        ''' Verify selection '''

        if len(bpy.context.selected_objects) != 2:
            raise RuntimeError("Two objects must be selected.")

        for obj in bpy.context.selected_objects:
            if obj.type != 'MESH':
                raise RuntimeError("Both objects must be meshes.")

        for obj in bpy.context.selected_objects:
            if obj == bpy.context.scene.objects.active:
                dest = obj
            else:
                srce = obj

        data = {}

        ''' Process the source object '''

        if not srce.data.shape_keys:
            # Add a basis shapekey and an empty shapekey
            srce.shape_key_add('Basis')
            srce.shape_key_add('Key')

        base_key_block = srce.data.shape_keys.reference_key
        srce_base_key_values = [item.co for item in base_key_block.data.values()]
        key_blocks = srce.data.shape_keys.key_blocks

        for key_block_name in key_blocks.keys():
            key_block = key_blocks[key_block_name]

            # Do nothing for the source base key
            if base_key_block == key_block:
                continue

            key_values = [item.co for item in key_block.data.values()]
            if len(key_values) != len(srce_base_key_values):
                raise RuntimeError("1. Source mesh vertex count is different: " + key_block_name)

            srce_diff_key_values = [a - b for a, b in zip(key_values, srce_base_key_values)]

        ''' Process the destination object '''

        base_key_block = dest.data.shape_keys.reference_key
        base_key_values = [item.co for item in base_key_block.data.values()]
        key_blocks = dest.data.shape_keys.key_blocks

        data[dest.name] = {
                        "base": base_key_block.name,
                        "diffs": [],
        }

        for key_block_name in key_blocks.keys():
            key_block = key_blocks[key_block_name]
            key_values = [item.co for item in key_block.data.values()]

            # If basis key, do nothing
            if base_key_block == key_block:
                continue

            diff_key_values = [a - b for a, b in zip(key_values, base_key_values)]
            
            # Append the source key values so the vertex count matches
            combined = [diff_key_values, srce_diff_key_values]
            diff_key_values = list(itertools.chain.from_iterable(combined))
            
            data[dest.name]["diffs"].append({
                "name": key_block_name,
                "values": diff_key_values,
            })

        """ Join the source to the destination """

        bpy.ops.object.join()

        """ Set the modified shapekeys """

        # Always clear and recreate the shapekeys
        for k in key_blocks:
            dest.shape_key_remove(k)

        dest.shape_key_add('Basis')

        base_key_block = dest.data.shape_keys.reference_key
        base_key_values = [item.co for item in base_key_block.data.values()]
        key_blocks = dest.data.shape_keys.key_blocks

        for key_block_data in data[dest.name]["diffs"]:
            key_block_name = key_block_data["name"]
            key_block = key_blocks.get(key_block_name)
            if not key_block:
                dest.shape_key_add()
                key_blocks[-1].name = key_block_name
            if base_key_block == key_block:
                continue
            key_values = [mathutils.Vector(vec) for vec in key_block_data["values"]]
            if len(key_values) != len(base_key_values):
                raise RuntimeError("3. mesh vertex count is different: " + key_block_name)
            for i in range(len(key_values)):
                key_blocks[key_block_name].data[i].co = key_values[i] + base_key_values[i]

        return {'FINISHED'}

classes = (
    ObjectMerge_PT_Main,
    ObjectMerge_OT_Join
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
