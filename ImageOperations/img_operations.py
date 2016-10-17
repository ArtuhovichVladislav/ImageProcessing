from PIL import Image
from PIL import ImageDraw
import numpy
import math
from scipy.misc import toimage

max_brightness = 255

def logic(first_image, second_image, result_file, op):
    im1 = Image.open(first_image)
    im2 = Image.open(second_image)
    draw = ImageDraw.Draw(im1)

    w, h = im1.size

    pixels1, pixels2 = im1.load(), im2.load()
    for i in range(w):
        for j in range(h):
            r1, g1, b1 = pixels1[i, j]
            r2, g2, b2 = pixels2[i, j]
            r3, g3, b3 = eval("{}{}{}, {}{}{}, {}{}{}".format(r1, op, r2,
                         g1, op, g2, b1, op, b2))
            draw.point((i, j), (r3, g3, b3))

    im1.save(result_file)
    del draw
    print "Ready"

def logic_not(image):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    s = image.split('.')
    result_image = s[0] + "_not." + s[1]

    w, h = im.size
    pixels = im.load()

    for i in range(w):
        for j in range(h):
            r, g, b = pixels[i, j]
            r1, g1, b1 = max_brightness - r, max_brightness - g, max_brightness - b
            draw.point((i, j), (r1, g1, b1))

    im.save(result_image)
    del draw
    print "Ready"

def arithmetic(image, c, op):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    s = image.split('.')
    op_name = "add" if op == "+" else "mul"
    result_image = s[0] + "_" + op_name + "." + s[1]

    w, h = im.size
    pixels = im.load()

    for i in range(w):
        for j in range(h):
            r, g, b = pixels[i, j]
            r1, g1, b1 = r + c, g + c, b + c
            r1, g1, b1 = eval("{}{}{}, {}{}{}, {}{}{}".format(r, op, c,
                         g, op, c, b, op, c))
            draw.point((i, j), (r1, g1, b1))

    im.save(result_image)
    del draw
    print "Ready"

def arithmetic_pictures_addition(first_image, second_image, result_file, c, op):
    im1 = Image.open(first_image)
    im2 = Image.open(second_image)
    draw = ImageDraw.Draw(im1)

    w, h = im1.size

    pixels1, pixels2 = im1.load(), im2.load()

    for i in range(w):
        for j in range(h):
            r1, g1, b1 = pixels1[i, j]
            r2, g2, b2 = pixels2[i, j]
            r3, g3, b3 = eval("{}{}{}, {}{}{}, {}{}{}".format(int(c*r1),
                         op, int((1-c)*r2),int(c*g1), op, int((1-c)*g2),
                         int(c*b1), op, int((1-c)*b2)))
            draw.point((i, j), (r3, g3, b3))

    im1.save(result_file)
    del draw
    print "Ready"

def image_masking(image):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    s = image.split('.')
    result_image = s[0] + "_masked." + s[1]

    w, h = im.size
    mask_matrix = [[ 0 if (x > h / 2) and (y > w / 2)
                    else 1 for x in range(h)] for y in range(w)]

    pixels = im.load()

    for i in range(w):
        for j in range(h):
            r, g, b = pixels[i, j]
            r1, g1, b1 = r * mask_matrix[i][j], g * mask_matrix[i][j], b * mask_matrix[i][j]
            draw.point((i, j), (r1, g1, b1))

    im.save(result_image)
    del draw
    print "Ready"


def brightness(color):
    return color if type(color) == int else \
        int(color[0] * 0.3 + color[1] * 0.59 + color[2] * 0.11)

def draw_histogram(file_name, high, h):
    width = len(h)
    hist = Image.new("RGB", (width, high), "white")
    draw = ImageDraw.Draw(hist)
    max_high = float(max(h))

    if max_high != 0:
        for i in range(width):
            draw.line(((i, high), (i, high - h[i] / max_high * high)), fill = "black")
    hist.save(file_name)


def make_hist(file_name, histogram_name):
    im = Image.open(file_name)
    colors = im.getcolors(im.size[0] * im.size[1])
    width, height = 256, 256

    h = [0 for _ in range(width)]
    for cnt, color in colors:
        index = brightness(color)
        h[index] += cnt
    draw_histogram(histogram_name, height, h)
    print "Histogram ready"

def histogram_equalization(image):
    im = Image.open(image)
    im_matrix = numpy.array(im)

    s = image.split('.')
    result_image = s[0] + "_equalized." + s[1]
    result_image_hist = s[0] + "_equalized_hist." + s[1]
    original_image_hist = s[0] + "_hist." + s[1]

    width, height = im.size

    h = [0 for _ in range(max_brightness)]

    for i in range (0, width - 1):
        for j in range (0, height - 1):
            h[im_matrix[i, j]] = h[im_matrix[i, j]] + 1

    for i in range (1, max_brightness):
        h[i] += h[i - 1]

    for i in range (0, max_brightness):
        h[i] = int(max_brightness * h[i] / (width * height))

    res = numpy.zeros(shape = (width, height), dtype = int)

    for i in range (0, width - 1):
        for j in range (0, height - 1):
            res[i, j] = h[im_matrix[i, j]]

    toimage(res).save(result_image)

    make_hist(image, original_image_hist)
    make_hist(result_image, result_image_hist)

if __name__ == "__main__":
    logic_not("images/logic_op/2_for_not.jpg")

    logic("images/logic_op/car.jpg", "images/logic_op/car2.jpg", "images/logic_op/car_car2_or.jpg", "|")
    logic("images/logic_op/car.jpg", "images/logic_op/car2.jpg", "images/logic_op/car_car2_and.jpg", "&")
    logic("images/logic_op/car.jpg", "images/logic_op/car2.jpg", "images/logic_op/car_car2_xor.jpg", "^")

    arithmetic("images/arithmetic_op/4.jpg", 50, "+")
    arithmetic("images/arithmetic_op/4.jpg", 2, "*")

    arithmetic_pictures_addition("images/image_add_sub/1.jpg", "images/image_add_sub/2.jpg", "images/image_add_sub/3.jpg", 0.5, "+")
    image_masking("images/masking/1.jpg")

    histogram_equalization("images/equalization/lena.png")
