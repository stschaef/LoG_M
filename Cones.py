import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import numpy as np
import random

WIDTH = 800
HEIGHT = int(3 * WIDTH / 4)


image = Image.new("RGB", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

# Attempt to use 2nd image to draw just the boundary by following orbit of boundary point
image_2 = Image.new("RGB", (WIDTH, HEIGHT))
draw_2 = ImageDraw.Draw(image_2)

B = np.array([
    [2, -1, -3],
    [-1, 2, -1],
    [-1, -1, 2]])
Id = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]])
B_inv = np.linalg.pinv(B)
L1 = B_inv[0]
L2 = B_inv[1]
L3 = B_inv[2]

R1 = Id - np.array([
    B.T[0],
    [0, 0, 0],
    [0, 0, 0]])
R2 = Id - np.array([
    [0, 0, 0],
    B.T[1],
    [0, 0, 0]])
R3 = Id - np.array([
    [0, 0, 0],
    [0, 0, 0],
    B.T[2]])

# Change of basis on R3
# Orthonormal basis with one basis element being perpendicular to our chart, other two span the chart
M = np.array([
    [0, - np.sqrt(2) / np.sqrt(3), 1 / 3],
    [1 / np.sqrt(2), 1 / np.sqrt(6), 1 / 3],
    [-1 / np.sqrt(2), 1 / np.sqrt(6), 1 / 3]])


# Related to affine chart
# x = x / z
# y = y / z
# z = 1
def project_z1(v):
    return v[0]/(v[2]), v[1]/(v[2])


def project_xyz1(v):
    M_inv = np.linalg.pinv(M)
    vec = np.dot(M_inv, v)
    return vec[0] / vec[2], vec[1] / vec[2]


# Height Scaling, Width Scaling, x-offset, y-offset
opts = {project_z1: (.4, .4, -50, -50), project_xyz1: (1.2, 1.2, -450, -300)}


# pt should be a tuple of coordinates to draw
def drawable(pt, project):
    x, y, x_off, y_off = opts[project]

    # Pretend that the origin is midpoint of drawing window
    x = WIDTH - pt[0] * int(WIDTH * x)
    y = HEIGHT - pt[1] * int(HEIGHT * y)

    # Offset should be used to center image, but may not be necessary
    return x + x_off, y + y_off


def tiling(matrices, project):
    for mat in matrices:
        # Projectivize the lines
        p1 = project(np.dot(mat, L1))
        p2 = project(np.dot(mat, L2))
        p3 = project(np.dot(mat, L3))
        p4 = project(np.dot(mat, L1))

        # Switch from a scale close to origin to be within the drawing window
        p1 = drawable(p1, project)
        p2 = drawable(p2, project)
        p3 = drawable(p3, project)
        p4 = drawable(p4, project)
        # TO DO: Color may be used to fill in tiles, but the order in which we color must be determined
        # color = (random.randrange(125, 255), random.randrange(125, 155), random.randrange(155, 255))
        # draw.polygon((p1, p2, p3), fill=color)

        # Draw line between appropriate points
        # Unsure why there must be four points here
        draw.line((p1, p2, p3, p4), fill=(255, 0, 0), width=2)


pts = []


def draw_orbit(vec, matrices, project):
    for mat in matrices:
        pt = project(np.dot(mat, vec))
        pt = drawable(pt, project)
        # draw.point(pt, fill=(int(.6*255), int(.4*255), int(0*255)))
        # print(pt)
        # draw.ellipse([(pt[0], pt[0] + 10), (pt[1], pt[1] + 10)], fill=(250, 250, 100))
        pts.append(pt)


def draw_hull(points):
    # draw.polygon(points, outline=(0, 255, 0))
    for pt1 in points:
        for pt2 in points:
            dist = lambda pt1_, pt2_: np.sqrt((pt2_[0] - pt1_[0])**2 + (pt2_[1] - pt1_[1])**2)
            if dist(pt1, pt2) < 30:
                draw.line((pt1, pt2), fill=(0, 255, 0), width=2)



mats = [Id, R1, R2, R3]

COUNT_MAX = 1500


def gen_mats(matrices):
    count = 0
    for mat in matrices:
        # Redundant check, they are reflections so they are their own inverses
        # if not any((np.linalg.inv(mat) == x).all() for x in mats):
        #     mats.append(np.linalg.inv(mat))
        #     count += 1
        #     if count > COUNT_MAX:
        #         return

        # If pairwise products of matrices not in group, add them
        for matrix in matrices:
            if not any((np.dot(mat, matrix) == x).all() for x in mats):
                mats.append(np.dot(mat, matrix))
                count += 1
                if count > COUNT_MAX:
                    return


gen_mats(mats)
# print(mats)
tiling(mats, project_z1)
# tiling(mats, project_xyz1)
composed = np.dot(R2, R3)
composed = np.dot(R1, composed)
vals, vecs = np.linalg.eig(composed)
print("R1 R2 R3:\n", composed)
print("Eigenvalues:\n", vals)
print("Eigenvectors:\n", vecs)
draw_orbit(vecs.T[0], mats, project_z1)
draw_orbit(vecs.T[1], mats, project_z1)
draw_hull(pts)
image.save('cone_and_boundary.png', 'PNG')
image.show()

