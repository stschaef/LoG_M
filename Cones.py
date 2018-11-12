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

M = np.array([
    [0, - np.sqrt(2) / np.sqrt(3), 1 / 3],
    [1 / np.sqrt(2), 1 / np.sqrt(6), 1 / 3],
    [-1 / np.sqrt(2), 1 / np.sqrt(6), 1 / 3]])
print(M)
print("*")
print(np.linalg.inv(M))
print("*")
print(np.linalg.pinv(M))

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



# pt should be a tuple of coordinates to draw
def drawable(pt):
    # print('Point:', pt)
    # Pretend that the origin is midpoint of drawing window
    x = WIDTH - pt[0] * int(WIDTH * .5)
    y = HEIGHT - pt[1] * int(HEIGHT * .5)

    # Offset should be used to center image, but may not be necessary
    offset = -200, -200
    # print('X:', x, 'Y:', y)
    return x + offset[0], y + offset[1]


def tiling(matrices, project):
    for mat in matrices:
        # Projectivize the lines
        p1 = project(np.dot(mat, L1))
        p2 = project(np.dot(mat, L2))
        p3 = project(np.dot(mat, L3))
        p4 = project(np.dot(mat, L1))

        # Switch from a scale close to origin to be within the drawing window
        p1 = drawable(p1)
        p2 = drawable(p2)
        p3 = drawable(p3)
        p4 = drawable(p4)

        # TO DO: Color may be used to fill in tiles, but the order in which we color must be determined
        # color = (random.randrange(125, 255), random.randrange(125, 155), random.randrange(155, 255))
        # draw.polygon((p1, p2, p3), fill=color)

        # Draw line between appropriate points
        # Unsure why there must be four points here
        draw.line((p1, p2, p3, p4), fill=(255, 255, 255), width=2)


def colored_tiling(matrices, project):
    # Don't know how to incorporate this function, its functionality could be taken by tiling(matrices)
    for mat in matrices:
        # Projectivize the lines
        p1 = project(np.dot(mat, L1))
        p2 = project(np.dot(mat, L2))
        p3 = project(np.dot(mat, L3))

        # Switch from a scale close to origin to be within the drawing window
        p1 = drawable(p1)
        p2 = drawable(p2)
        p3 = drawable(p3)

        # Attempt to color in polygons
        draw.polygon((p1, p2, p3), fill=200)


mats = [Id, R1, R2, R3]

COUNT_MAX = 500


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
# tiling(mats, project_z1)
tiling(mats, project_xyz1)
image.save('cone.png', 'PNG')
image.show()

