from PIL import Image
from random import randint


def rgb2binary(image, thresh = 120):
    """ 
    Change the pixel rgb value to either white or black based on a gvien threshold.
    
    Param:
        image: the image object.
        thresh: a value in [0, 255]. average rgb value less than thresh is considered white, the others black.
    """
    w, h = image.size
    pixel = image.load()
    for i in range(w):
        for j in range(h):
            pixel[i,j] = (0, 0, 0) if sum(pixel[i, j])/3 < thresh else (255, 255, 255)
    image.save("binary.png")

def markBlock(pixel, i, j, w, h, color):
    """
    Traverse from a given pixel, find all connected black pixels which constituts a block, and mark the block in the given color.

    Param:
        pixel: PixelAccess object containing the rgb info of the image
        i, j: the coordination of the pixel currently visited.
        w, h: the width and height of the image.
        color: the color which the block is going to be marked.

    Return:
        The number of the pixels in the block.
    """
    discovered = set()
    discovered.add((i, j))
    count = 0
    rect = [i, i, j, j] #left, right, top, bottom
    while len(discovered) > 0:
        count += 1
        x, y = discovered.pop()
        pixel[x, y] = color

        rect[0] = min(rect[0], x)
        rect[1] = max(rect[1], x)
        rect[2] = min(rect[2], y)
        rect[3] = max(rect[3], y)

        dist = 1
        neighbors = [(nx, ny) for nx in range(x-dist, x+dist+1) for ny in range(y-dist, y+dist+1)]
        # neighbors = [(nx, ny) for (nx, ny) in neighbors if nx >= 0 and nx < w and ny >= 0 and ny < h and pixel[nx, ny] == (0, 0, 0)]
        for nx, ny in neighbors:
            if(nx >= 0 and nx < w and ny >= 0 and ny < h and pixel[nx, ny] == (0, 0, 0)):
                discovered.add((nx, ny))

    return count, rect

def markRects(image, rects):
    pixel = image.load()
    for rect, color in rects:
        for x in range(rect[0], rect[1]):
            pixel[x, rect[2]] = color
            pixel[x, rect[3]] = color
        for y in range(rect[2], rect[3]):
            pixel[rect[0], y] = color
            pixel[rect[1], y] = color
    image.save("rect.png")

def analyseImage(image):
    """
    Extract all blocks which contains only connected pixels.

    Param:
        image: the image to be analyzed.

    Return:
        A list of blocks in the form of (numOfPixels, x, y).
    """
    pixel = image.load()
    w, h = image.size
    blocks = []
    for i in range(w):
        for j in range(h):
            if(pixel[i, j] == (0, 0, 0)):
                color = (randint(0, 220), randint(0, 220), randint(0, 220))
                npix, rect = markBlock(pixel, i, j, w, h, color)
                # blocks.append((npix, i, j, rect, color))
                blocks.append((rect, color))
    image.save("colorful.png")
    return blocks

def main():
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else "penmen.png"
    print filename
    im = Image.open(filename)
    rgb2binary(im)
    rects = analyseImage(im)
    markRects(im, rects)
    area = lambda r : (r[0][1]-r[0][0]+1)*(r[0][3]-r[0][2]+1)
    ## sort the rectangles by area in descending order
    rects.sort(key = area, reverse = True)
    print "%d rectangles found." % len(rects)
    print "min_area = %d, max_area = %d" % (area(rects[-1]), area(rects[0]))

main()

