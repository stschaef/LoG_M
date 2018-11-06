import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import numpy as np

# image = Image.new("RGB", (640, 480))
#
# draw = ImageDraw.Draw(image)
#
# # points = ((1,1), (2,1), (2,2), (1,2), (0.5,1.5))
# points = ((100, 100), (200, 100), (200, 200), (100, 200), (50, 150))
# draw.polygon((points), fill=200)
#
# image.show()

WIDTH = 800
HEIGHT = 600


image = Image.new("RGB", (WIDTH, HEIGHT))

draw = ImageDraw.Draw(image)

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
    x = WIDTH / 2 - pt[0] * 200
    y = HEIGHT / 2 - pt[1] * 200
    # print('X:', x, 'Y:', y)
    return x, y



def tiling(matrices):
    print("Line")
    for mat in matrices:
        p1 = proj(np.dot(mat, L1))
        p2 = proj(np.dot(mat, L2))
        p3 = proj(np.dot(mat, L3))
        p4 = proj(np.dot(mat, L1))

        p1 = drawable(p1)
        p2 = drawable(p2)
        p3 = drawable(p3)
        p4 = drawable(p4)

        draw.line((p1, p2, p3, p4), fill=200, width=1)


def colored_tiling(matrices):
    for mat in matrices:
        p1 = proj(np.dot(mat, L1))
        p2 = proj(np.dot(mat, L2))
        p3 = proj(np.dot(mat, L3))

        p1 = drawable(p1)
        p2 = drawable(p2)
        p3 = drawable(p3)

        # print(p1, p2, p3)
        draw.polygon((p1, p2, p3), fill=200)

# draw_these_lines=[matrix.identity(3),R1*R2,R1*R2*R1*R2,R1,R1*R2*R1,R1*R2*R1*R2*R1,R3]
# draw_these_polygons=[matrix.identity(3),R1*R2,R1*R2*R1*R2]
# draw_these3=[(R1*R2*R3)^i for i in [-4..4]]
#     tiling(draw_these3)+
#     tiling(draw_these_lines)+
#      colored_tiling(draw_these_polygons)
# ).show(axes=false,aspect_ratio=1)

draw_these_lines=[Id,R1*R2,R1*R2*R1*R2,R1,R1*R2*R1,R1*R2*R1*R2*R1,R3]
mats = [Id, R1*R2,R1*R2*R1*R2,R1,R1*R2*R1,R1*R2*R1*R2*R1]
tiling(mats)
tiling(draw_these_lines)
#colored_tiling(mats)
points = ((100, 100), (200, 100), (200, 200), (100, 200), (50, 150))
# draw.polygon((points), fill=200)
image.show()

