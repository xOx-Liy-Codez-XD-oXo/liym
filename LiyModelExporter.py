import bpy
import bmesh
import os
import math

#model export options

exportVertexPositions = 1
exportFaceNormals = 0
exportVertexNormals = 1
exportTextureCoordinate = 1
exportVertexColors = 1

exportMatrixIndex = 1


# filename = "model"
C = bpy.context
filename = C.object.name
liymname = filename + ".liym"
file = open(os.environ['HOME'] + "/" + liymname, "w")

print("export")

tricount = 0
otherpol = 0
for poly in C.object.data.polygons:
	if len(poly.vertices) != 3:
		otherpol += 1

if otherpol == 0:
	isTriangulate = 1
else:
	isTriangulate = 0

if isTriangulate == 0:
	for modifier in C.object.modifiers:
		if modifier.type == "TRIANGULATE":
			isTriangulate = 1
	if isTriangulate == 0:
		C.object.modifiers.new(name='autogentriangulate', type='TRIANGULATE')

depsgraph = C.evaluated_depsgraph_get()

bm = bmesh.new()
bm.from_object(C.object, depsgraph)
bm.calc_loop_triangles()
bm.verts.ensure_lookup_table()
bm.faces.ensure_lookup_table()
tricount = len(bm.faces)

# 1 - vertex pos
# 2 - face normal
# 3 - per-vertex normal
# 4 - texture coordinate
# 5 - 
# 6 - vertex colors
# 7 - matrix index
# 8 - 

isvpos = int('00000001', 2)
isfacn = int('00000010', 2)
isvern = int('00000100', 2)
istexc = int('00001000', 2)

isvcol = int('00100000', 2)
ismtxi = int('01000000', 2)


filetype = 0

if(exportVertexPositions == 1):
    filetype = filetype | isvpos
    
if(exportFaceNormals == 1):
    filetype = filetype | isfacn
    
if(exportVertexNormals == 1):
    filetype = filetype | isvern
    
if(exportTextureCoordinate == 1):
    filetype = filetype | istexc
    
if(exportVertexColors == 1):
    filetype = filetype | isvcol
    
if(exportMatrixIndex == 1):
    filetype = filetype | ismtxi

file.write("o\n")

file.write(str(filetype) + "\n")

file.write(str(tricount))

if(exportVertexPositions == 1):
    file.write("\np\n")

    for f in bm.faces:
    	for v in f.verts:
    		# print(v.co.x)
    		lala1 = f"{v.co.x:.6f}"
    		lala2 = f"{v.co.y:.6f}"
    		lala3 = f"{v.co.z:.6f}"
    		out1 = lala1 + " " + lala2 + " " + lala3 + " "
    		file.write(out1)

if(exportFaceNormals == 1):
    file.write("\nn\n")
    
    for f in bm.faces:
    	# print(f.normal)
    	lala1 = f"{f.normal.x:.6f}"
    	lala2 = f"{f.normal.y:.6f}"
    	lala3 = f"{f.normal.z:.6f}"
    	out1 = lala1 + " " + lala2 + " " + lala3 + " "
    	file.write(out1)
    
if(exportVertexNormals == 1):
    file.write("\nn\n")
    
    for f in bm.faces:
        for v in f.verts:
            lala1 = f"{v.normal.x:.6f}"
            lala2 = f"{v.normal.y:.6f}"
            lala3 = f"{v.normal.z:.6f}"
            out1 = lala1 + " " + lala2 + " " + lala3 + " "
            file.write(out1)

if(exportTextureCoordinate == 1):
    file.write("\nt\n")
    
    for f in bm.faces:
        elem_seq = f.loops
        for e in elem_seq:
            loop = e
            loop_seq = bm.loops
            layers = loop_seq.layers
            # print(dir(layers))
            collection = layers.uv
            item = collection[0]
            luv = loop[item]
            uv = luv.uv
            lala1 = f"{uv.x:.6f}"
            lala2 = f"{uv.y:.6f}"
            out1 = lala1 + " " + lala2 + " "
            file.write(out1)
            
if(exportVertexColors == 1):
    file.write("\nc\n")
    
    color = bm.loops.layers.float_color.active
    # print(bm.loops.layers.color.active)
    # print(dir(bm.loops.layers.color.items))
    
    for f in bm.faces:
        for loop in f.loops:        
            lala1 = str(int(math.sqrt(loop[color].x) * 255))
            lala2 = str(int(math.sqrt(loop[color].y) * 255))
            lala3 = str(int(math.sqrt(loop[color].z) * 255))
            out1 = lala1 + " " + lala2 + " " + lala3 + " "
            file.write(out1)
    

if(exportMatrixIndex == 1):
    file.write("\nw\n")
    layerdeform = bm.verts.layers.deform.active
    assert layerdeform is not None
    
    for f in bm.faces:
        for v in f.verts:
            g = v[layerdeform]
        
            weights = [0 for i in range(len(C.object.vertex_groups))]
            for group_index in range(len(C.object.vertex_groups)):
                if group_index in g:
                    weights[group_index] = g[group_index]
                else:
                    weights[group_index] = 0.0
        
            biggestweightindex = 0 
            for w in range(len(weights)):
                if (weights[w] > weights[biggestweightindex]):
                    biggestweightindex = w
        
            out1 = str(biggestweightindex) + " "
            file.write(out1)
    
    
file.write("\n")

file.close()
    
bm.free()