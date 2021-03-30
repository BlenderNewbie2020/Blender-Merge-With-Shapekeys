# Blender Merge With Shapekeys (blender addon) for Blender 2.79 only.

## Merge two objects with differing geometries

Addon to merge a selected object with no shape keys to an active object with shape keys.

## Reasoning

Each shape key is a list of coordinate offsets for *every* vertex in the object. Adding vertices to the mesh obviously changes the vertex count breaking the geometry. However, it is possibe to append geometry from a shape key on a selected object to each shape key on the active object, relecting the change in vertex count, join the selected object to the active, and recreate the shape keys.

## Method

Select the first _source_ object. Shift-select the second _destination_ object. Running the script will merge the two objects recreating the destination shape keys to reflect the change in geometry. Currently, the _source_ object is not preserved.



## Install

Do not try this at home.

Download [Blender-Merge-With-Shapekeys.py](https://raw.githubusercontent.com/BlenderNewbie2020/Blender-Merge-With-Shapekeys/master/Blender-Merge-With-Shapekeys.py) and install it.

## License

[Zlib License](LICENSE)
