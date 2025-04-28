# LIYM
Liym is a model format designed for the limitations of the Nintendo Wii. It can be read at runtime on the Wii, or used as an intermediary format for processing model data for other tools. 

## LiyModelExporter.py usage

Open the script in a Blender text editor. Change the settings at the top of the file, then make sure your object is selected and press the play button at the top of the text editor. 

## LIYM file walkthrough

This section will be a walkthrough of the data of this model. It is a tetrahedron with custom normals, texture coordinates, vertex colors, and per-vertex modelview matrix indecies.

![tetr1](https://github.com/user-attachments/assets/cce2e110-d63f-4dd5-b050-663a567f6add) ![tetr2](https://github.com/user-attachments/assets/88ea4576-629f-4325-9c28-2e02ce967ba6)

This is the model data. 

```
o
109
4
p
1.000000 -1.000000 -1.000000 0.000000 0.000000 ...
n
0.000000 -0.866481 -0.499210 0.000000 -0.894427 ...
t
1.000000 0.500000 0.000000 0.500000 1.000000 ...
c
254 0 0 254 255 255 0 0 255 0 0 255 254 255 ...
w
0 1 0 0 1 0 0 1 0 0 0 0 
```

### `o`
LIYM files can have multiple objects. The start of each object is denoted by `o`. The end of an object is defined by a line break '\n' immediately before EOF or another object.
Note: libogc FAT filesystem driver sometimes will not present EOF, returning char 255 instead

### `109`
Filetype. An integer describing the content of the object. This can be ANDed with a table to determine the content features.

| Bit value | uint8 | Feature |
| --------- | ----- | ------- |
| 0000 0001 | 1     | Vertex positions |
| 0000 0010 | 2     | Face normals[1] |
| 0000 0100 | 4     | Vertex normals |
| 0000 1000 | 8     | Texture coordinates |
| 0001 0000 | 16    | Unused |
| 0010 0000 | 32    | Vertex colors |
| 0100 0000 | 64    | Matrix indecies |
| 1000 0000 | 128   | Unused |

1: Face normals eventually need to be converted to vertex normals. Vertex and face normals should not be selected at the same time. 


109 = 0b01101101

The file features can be determined with bitwise ANDs as follows: 
| task | result | conclusion|
| --- | --- | --- |
| 109 & 1 != 0 | true | vertex position |
| 109 & 2 != 0 | false | no face normal |
| 109 & 4 != 0 | true | vertex normal |
| 109 & 8 != 0 | true | texture coordinate |
| 109 & 32 != 0 | true | vertex color |
| 109 & 64 != 0 | true | matrix index |

### `4`
The triangle count. LIYM only supports triangles. LIYM has no support for quantization, so the `p`, and `c` arrays will each have 9 times the amount of elements as the triangle count (3 verticies per triangle, 3 axes per vertex). The w array will have 3 times the amount of elements as the triangle count (3 verticies per triangle). If face normals are selected, the `n` array will have 3 times the amount of elements as the triangle count, but if vertex normals are selected, the `n` array will have 9 times the amount of elements as the triangle count. The `t` array will have 6 times the amount of elements as the triangle count (3 verticies per triangle, 2 axes per vertex). 

### `p`
Denotes beginning of vertex position array. Followed by a line break. This array must be present if active in the filetype. The numbers that follow are floats, separated by spaces. A line break denotes the end of the array and the start of the next. If present, this array is always 9 * tricount elements long. 

### `n`
Denotes beginning of normal array, followed by a line break. This array must be present if either face normals or vertex normals are active in the filetype. The numbers that follow are floats, separated by spaces. A line break denotes the end of the array and the start of the next. If face normals are present, this array is 3 * tricount long. If vertex normals are present, this array is 9 * tricount long. 

### `t`
Denotes beginning of texture coordinate array. Followed by a line break. This array must be present if active in the filetype. The numbers that follow are floats, separated by spaces. A line break denotes the end of the array and the start of the next. If present, this array is always 6 * tricount elements long. 

### `c`
Denotes beginning of vertex color array. Followed by a line break. This array must be present if active in the filetype. The numbers that follow are unsigned integers, separated by spaces. A line break denotes the end of the array and the start of the next. If present, this array is always 9 * tricount elements long. 

### `w`
Denotes beginning of matrix index. Followed by a line break. This array must be present if active in the filetype. The numbers that follow are unsigned integers, separated by spaces. A line break denotes the end of the array and the start of the next. If present, this array is always 3 * tricount elements long. 

### `EOF` 
