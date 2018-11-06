import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import numpy as np
import random

WIDTH = 800
HEIGHT = 600


image = Image.new("RGB", (WIDTH, HEIGHT))
image_2 = Image.new("RGB", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
draw_2 = ImageDraw.Draw(image_2)

B= np.array([
    [2, -1, -3],
    [-1, 2, -1],
    [-1, -1, 2]
])
Id = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])
B_inv = np.linalg.inv(B)
L1 = B_inv[0]
L2 = B_inv[1]
L3 = B_inv[2]



R1=Id - np.array([
    B.T[0],
    [0, 0, 0],
    [0, 0, 0]])
R2=Id - np.array([
    [0, 0, 0],
    B.T[1],
    [0, 0, 0]])
R3=Id - np.array([
    [0, 0, 0],
    [0, 0, 0],
    B.T[2]])

# Related to affine chart
# x = x / z
# y = y / z
# z = 1


def proj(v):
    return v[0]/v[2], v[1]/v[2]


# pt should be a tuple of coordinates to draw
def drawable(pt):
    # print('Point:', pt)
    # Pretend that the origin is midpoint of drawing window
    x = WIDTH - pt[0] * 250
    y = HEIGHT - pt[1] * 250

    offset = -100, -50
    # print('X:', x, 'Y:', y)
    return x + offset[0], y + offset[1]


def tiling(matrices):

    for mat in matrices:
        p1 = proj(np.dot(mat, L1))
        p2 = proj(np.dot(mat, L2))
        p3 = proj(np.dot(mat, L3))
        p4 = proj(np.dot(mat, L1))

        p1 = drawable(p1)
        p2 = drawable(p2)
        p3 = drawable(p3)
        p4 = drawable(p4)

        # color = (random.randrange(125, 255), random.randrange(125, 155), random.randrange(155, 255))
        draw.line((p1, p2, p3, p4), fill=(255, 255, 255), width=2)
        # draw.polygon((p1, p2, p3), fill=color)

def colored_tiling(matrices):
    # Don't know how to incorporate this function
    for mat in matrices:
        p1 = proj(np.dot(mat, L1))
        p2 = proj(np.dot(mat, L2))
        p3 = proj(np.dot(mat, L3))

        p1 = drawable(p1)
        p2 = drawable(p2)
        p3 = drawable(p3)

        # print(p1, p2, p3)
        draw.polygon((p1, p2, p3), fill=200)


mats = [Id, R1, R2, R3]

COUNT_MAX = 1500

def gen_mats(matrices):
    count = 0
    for mat in mats:
        # Redundant check, they are reflections so they are their own inverses
        # if not any((np.linalg.inv(mat) == x).all() for x in mats):
        #     mats.append(np.linalg.inv(mat))
        #     count += 1
        #     if count > COUNT_MAX:
        #         return
        for matrix in mats:
            if not any((np.dot(mat, matrix) == x).all() for x in mats):
                mats.append(np.dot(mat, matrix))
                count += 1
                if count > COUNT_MAX:
                    return


gen_mats(mats)
print(mats)
tiling(mats)
image.show()

