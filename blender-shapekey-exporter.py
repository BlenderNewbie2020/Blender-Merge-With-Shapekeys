import bpy
from bpy.props import *
from bpy.types import Scene

import mathutils
import json

bl_info = {
    "name" : "Object Join with Shapekeys",
    "author" : "BlenderNewbie2020",
    'category': 'Mesh',
    'location': 'View 3D > Tool Shelf > Object Merge',
    'warning': 'Does nothing. Badly.',
    'description': 'Join selected object with active, updating existing shapkeys. Original shapekey exporter code by Narazaka.',
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
        
        """
        Method:
        
        For the active object:
            
            1. detect a base and shapekeys:
                if None, raise info and exit.
                else Loop over the shapekeys to store the datavalues.
            
        For the selected object:
            
            1. detect a base shapekey:
                if none add base and create a new key
                else, delete all keys, create base and one new key
            
            2. Loop over the the new key to store the data values.
           
            3. For each key in the active object (1), append the data values from (2).
            
            4. Delete all the keys in the active object.
            
            5. Join selected object to active.
            
            6. Assign shapekeys from (3).
            
        """
            
        """
        # Original export
        
        data = {}
        for object_name in bpy.data.objects.keys():
            obj = bpy.data.objects[object_name]
            if obj.type != 'MESH' or not obj.data.shape_keys:
                continue
            base_key_block = obj.data.shape_keys.reference_key
            base_key_values = [item.co for item in base_key_block.data.values()]

            key_blocks = obj.data.shape_keys.key_blocks
            data[object_name] = { 
                "base": base_key_block.name,
                "diffs": [], 
            }
            for key_block_name in key_blocks.keys():
                key_block = key_blocks[key_block_name]
                if base_key_block == key_block: # base
                    continue
                key_values = [item.co for item in key_block.data.values()]
                if len(key_values) != len(base_key_values):
                    raise RuntimeError("mesh vertex count is different: " + key_block_name)
                diff_key_values = []
                for i in range(len(key_values)):
                    diff_key_values.append((key_values[i] - base_key_values[i])[:])
                data[object_name]["diffs"].append({
                    "name": key_block_name,
                    "values": diff_key_values,
                })

        """
        
        """
        # Original import
        data = None
        with open(self.filepath, mode='r', encoding="utf8") as f:
            data = json.load(f)

        for object_name in data.keys():
            if len(data[object_name]["diffs"]) == 0:
                continue
            obj = bpy.data.objects[object_name]
            if obj.type != 'MESH':
                continue

            # ensure base key
            if not obj.data.shape_keys:
                obj.shape_key_add()
                obj.data.shape_keys.key_blocks[-1].name = data[object_name]["base"]
            base_key_block = obj.data.shape_keys.reference_key
            base_key_values = [item.co for item in base_key_block.data.values()]

            key_blocks = obj.data.shape_keys.key_blocks
            # overwrite always (TODO: selectable)
            for key_block_data in data[object_name]["diffs"]:
                key_block_name = key_block_data["name"]
                key_block = key_blocks.get(key_block_name)
                if not key_block:
                    obj.shape_key_add()
                    key_blocks[-1].name = key_block_name
                if base_key_block == key_block: # base
                    continue
                key_values = [mathutils.Vector(vec) for vec in key_block_data["values"]]
                if len(key_values) != len(base_key_values):
                    raise RuntimeError("mesh vertex count is different: " + key_block_name)
                for i in range(len(key_values)):
                    key_blocks[key_block_name].data[i].co = key_values[i] + base_key_values[i]

        return {'FINISHED'}
        """

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
