import numpy as np

f = open("vertices.txt", "w+")

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
print("hello")
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


def proj_chart(vec_in):
    M = make_chart(1, 1, 1, 0)
    M_inv = np.linalg.inv(M)
    vec = np.dot(M_inv, vec_in)
    return vec[0] / vec[3], vec[1] / vec[3], vec[2] / vec[3]


threshold = .1

def draw_triangle(vec1, vec2, vec3, mat, project):
    pt1 = np.dot(mat, vec1)
    pt1 = project(pt1)
    pt2 = np.dot(mat, vec2)
    pt2 = project(pt2)
    pt3 = np.dot(mat, vec3)
    pt3 = project(pt3)
    if np.linalg.norm(np.array([pt1[0], pt1[1], pt1[2]]) - np.array([pt2[0], pt2[1], pt2[2]])) < threshold:
        return
    if np.linalg.norm(np.array([pt3[0], pt3[1], pt3[2]]) - np.array([pt2[0], pt2[1], pt2[2]])) < threshold:
        return
    if np.linalg.norm(np.array([pt1[0], pt1[1], pt1[2]]) - np.array([pt3[0], pt3[1], pt3[2]])) < threshold:
        return
    print(pt1[0], pt1[1], pt1[2], pt2[0], pt2[1], pt2[2], pt3[0], pt3[1], pt3[2], file=f)


mats = [Id, R1, R2, R3, R4, R5]

COUNT_MAX = 30000


def gen_mats(matrices):
    count = 0
    for mat in matrices:
        print(count)
        # If pairwise products of matrices not in group, add them
        for matrix in matrices:
            if not any((np.dot(mat, matrix) == x).all() for x in mats):
                mats.append(np.dot(mat, matrix))
                count += 1
                if count > COUNT_MAX:
                    return

print("yeet")
gen_mats(mats)
print("mats")
composed = np.dot(R4, R5)
composed = np.dot(R3, composed)
composed = np.dot(R2, composed)
composed = np.dot(R1, composed)
print("triangles made")
for mat in mats:
    draw_triangle(e1, e2, e3, mat, proj_chart)
print("end")
f.close()
