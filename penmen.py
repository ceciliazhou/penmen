from PIL import Image
from random import randint


def rgb2binary(image, thresh = 110):
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
    S = set()
    S.add((i, j))
    count = 0
    while len(S) > 0:
        count += 1
        x, y = S.pop()
        pixel[x, y] = color
        dist = 1
        neighbors = [(nx, ny) for nx in range(x-dist, x+dist+1) for ny in range(y-dist, y+dist+1)]
        for nx, ny in neighbors:
            if(nx >= 0 and nx < w and ny >= 0 and ny < h and pixel[nx, ny] == (0, 0, 0)):
                S.add((nx, ny))
    return count

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
                npix = markBlock(pixel, i, j, w, h, (randint(0, 220), randint(0, 220), randint(0, 220)))
                blocks.append((npix, i, j))
    image.save("test.png")
    return blocks

def main():
    im = Image.open("penmen.png")
    rgb2binary(im)
    blocks = analyseImage(im)
    blocks.sort()
    print "%d blocks found." % len(blocks)
    print "min_pix = %d, max_pix = %d" % (blocks[0][0], blocks[-1][0])

main()

