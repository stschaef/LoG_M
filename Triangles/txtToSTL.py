import sys
'''
Run from command line to get .stl file with the tiled triangles a set of vertices

Use commands of this form:
python3 txtToSTL.py INPUT.txt OUTPUT.stl
or
python txtToSTL.py INPUT.txt OUTPUT.stl

where input is a .txt with each line as 
vertex1.x vertex1.y vertex1.z vertex2.x vertex2.y vertex2.z vertex3.x vertex3.y vertex3.z
where these three vertices form a floating triangle on the boundary
'''

def main(argv):
    f_out = open(argv[1], "w+")

    f_in = open(argv[0])

    f_input = f_in.readlines()
    print("solid", file=f_out)
    for x in f_input:
        verts = x.split(" ")
        pt1 = (verts[0], verts[1], verts[2])
        pt2 = (verts[3], verts[4], verts[5])
        pt3 = (verts[6], verts[7], verts[8])
        print(" facet normal 0.000000e+000 0.000000e+000 0.000000e+000", file=f_out)
        print("  outer loop", file=f_out)
        print("   vertex", pt1[0], pt1[1], pt1[2], file=f_out)
        print("   vertex", pt2[0], pt2[1], pt2[2], file=f_out)
        print("   vertex", pt3[0], pt3[1], pt3[2], file=f_out)
        print("  endloop", file=f_out)
        print(" endfacet", file=f_out)
    print("endsolid", file=f_out)
    f_in.close()
    f_out.close()


if __name__ == "__main__":
    main(sys.argv[1:])