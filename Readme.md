# Blender Merge With Shapekeys (blender addon) for Blender 2.79 only.

Addon to merge selected object with active, updating the active shapekeys to reflect the change in geometry.

## Reasoning

Each shapekey is a list of coordinate offsets for *every* vertex in the object. Adding vertices to the mesh obviously changes the vertex count. However, it is possibe to append data from a shapekey on a selected object to each shapekey on the active object, relecting the change in vertex count, join the selected object to the active, and reassign the shapekeys.

## Install

Does not exist yet, and needs a home.

Download [Blender-Merge-With-Shapekeys.py](https://raw.githubusercontent.com/BlenderNewbie2020/Blender-Merge-With-Shapekeys/master/Blender-Merge-With-Shapekeys.py) and install it.

## License

[Zlib License](LICENSE)
