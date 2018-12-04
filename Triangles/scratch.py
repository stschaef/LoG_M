import numpy as np
import sys

'''
Run from command line to get .txt where each line has info for a triangle of the form
vertex1.x vertex1.y vertex1.z vertex2.x vertex2.y vertex2.z vertex3.x vertex3.y vertex3.z
where these three vertices form a floating triangle on the boundary

Use commands of this form:
python3 scratch.py OUTPUT.txt NUM_GENS
or
python scratch.py OUTPUT.txt NUM_GENS

Where NUM_GENS is how many recursive generations this will run for.
Be careful with this, as the number and runtime grows quickly.
NUM_GENS = 2, takes about 10-20 seconds
NUM_GENS = 3, takes over half an hour
'''

e1 = np.array([1, 0, 0, 0])
e2 = np.array([0, 1, 0, 0])
e3 = np.array([0, 0, 1, 0])
e4 = np.array([0, 0, 0, 1])

Id = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])

R1 = np.array([
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])

R2 = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]])

R3 = np.array([
    [0, 0, 0.5, 0],
    [0, 1, 0, 0],
    [2, 0, 0, 0],
    [0, 0, 0, 1]])

# Input \mu directly for now. Here, a = 2, d = 3, \mu = (cos pi/d)^2{(4a)/(a-1)^2} = 0.25(8) = 2
# n = \nu = 2+3m = 8
m = 2
n = 2 + 3 * m

R4 = np.array([
    [1 + m, m, m, -m],
    [m, 1 + m, m, -m],
    [m, m, 1 + m, -m],
    [n, n, n, 1 - n]])

R5 = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, -1]])


# R1R2R1R3
gam1 = np.dot(R1, np.dot(R2, np.dot(R1, R3)))
gam1_inv = np.linalg.pinv(gam1)

# R1R3R1R2
gam2 = np.dot(R1, np.dot(R3, np.dot(R1, R2)))
gam2_inv = np.linalg.pinv(gam2)

# project on chart ax+by+cz+dw = 1
# outputs change if basis matrix M
# normal vector is ([a,b,c,d]) divide by norm
def make_chart(a, b, c, d):
    n = np.linalg.norm(([a, b, c, d]))
    p = a / n
    q = b / n
    r = c / n
    s = d / n

    M = np.array([
        [s, -r, q, p],
        [r, s, -p, q],
        [-q, p, s, r],
        [-p, -q, -r, s],
    ])
    M.astype(float)
    return M


def proj_chart(vec_in, inv):
    vec = np.dot(inv, vec_in)
    return vec[0] / vec[3], vec[1] / vec[3], vec[2] / vec[3]


def triangle_4d(vec1, vec2, vec3, matr):
    # These are 4d right now
    pt1 = np.dot(matr, vec1)
    pt2 = np.dot(matr, vec2)
    pt3 = np.dot(matr, vec3)

    return pt1, pt2, pt3


def make_strings(num_gens):
    total = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    old_gen = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    new_gen = []
    str = "123456789"
    for i in range(num_gens):
        new_gen = []
        for char in str:
            for thing in old_gen:
                if thing[0] != char:
                    new_gen.append(char + thing)
        total += new_gen
        old_gen = new_gen
    print("Number of potential matrices:", len(total))
    return total


gens = [Id, R1, R2, R3, R4, R5, gam1, gam2, gam1_inv, gam2_inv]


# function to convert string into ordered list of matrices
def convert(str):
    product = np.dot(Id, Id)
    for char in str:
        product = np.dot(product, gens[int(char)])
    return product


def gen_mats(num_gens, matrices):
    perms = make_strings(num_gens)
    for perm in perms:
        matrices.append(convert(perm))


def main(argv):
    # for gam in [gam1, gam1_inv, gam2, gam2_inv]:
    #     vals, vecs = np.linalg.eig(gam)
    #     print(vals)
    #     print(vecs)
    # exit(1)

    f = open(argv[0], "w+")
    mats = []
    gen_mats(int(argv[1]), mats)
    print("matrices generated")

    tris_4d = []
    for mat in mats:
        tris_4d.append(triangle_4d(e1, e2, e3, mat))
    print("inital triangles made")

    '''
    Eigenvectors of gamma
    All gammas have e1, e2, e3, e4 as eigenvectors with eigenvalues in {.5, 1, 2}, but we must look at top and bottom eigenvectors

                top    bottom
    gam1        e1     e3
    gam1_inv    e3     e1
    gam2        e3     e2 
    gam2_inv    e2     e3

    For each transformation we will get pulled toward the top eigenvector. Becuase e3 is overrepresented in top eigenvectors, we can ignore
    one of gam1_inv or gam2 to make our runtime shorter. 
    So throw out gam2, but still consider gam2_inv

    This will make the size of with_gamma[] go from 4*len(mats) to 3*len(mats)
    ''' 
    gams = []
    order_of_gam = 4
    for gam in [gam1, gam1_inv, gam2_inv]:
        composed = np.dot(Id, gam)
        for _ in range(order_of_gam):
            composed = np.dot(composed, gam)
        gams.append(gam)
    print("gammas made")
    
    with_gamma = []
    for tri in tris_4d:
        for gam in gams:
            transformed_triangle = (np.dot(gam, tri[0]), np.dot(gam, tri[1]), np.dot(gam, tri[2]))
            with_gamma.append(transformed_triangle)
    print("triangles hit with gamma")
    print("Number of triangles with gamma:", len(with_gamma))
    print(len(with_gamma) * len(mats))
    i = 0
    for mat in mats:
        for element in with_gamma:
            i += 1
            if i % 100000 == 0:
                print(i)
            tris_4d.append((np.dot(mat, element[0]), np.dot(mat, element[1]), np.dot(mat, element[2])))
    print("things hit with gamma have been reflected")
    print("Number of triangles, with redundancy:", len(tris_4d))

    M = make_chart(1, 1, 1, 0)
    M_inv = np.linalg.inv(M)
    
    setty_boi = set()

    for tri in tris_4d:
        vert1 = proj_chart(tri[0], M_inv)
        vert2 = proj_chart(tri[1], M_inv)
        vert3 = proj_chart(tri[2], M_inv)
        strin = str(vert1[0]) + " " + str(vert1[1]) +  " " + str(vert1[2]) +  " " + str(vert2[0]) +  " " + str(vert2[1]) +  " " + str(vert2[2]) +  " " + str(vert3[0]) +  " " + str(vert3[1]) +  " " + str(vert3[2])
        setty_boi.add(strin)
    print("made setty boi")
    print("Number of unique triangles:", len(setty_boi))

    for thing in setty_boi:
        print(thing, file=f)
    print("DONE: printed to file")

    f.close()
    return

if __name__ == "__main__":
    main(sys.argv[1:])