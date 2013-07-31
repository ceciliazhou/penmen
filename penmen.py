#!/usr/bin/python

import matplotlib.pyplot as plt
from PIL import Image
from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def rgb2wb(pixel, size, thresh = 128):
    """
    Convert rgb pixels to white/black pixels based on some threshold.
    """
    w, h = size
    for i in range(w):
        for j in range(h):
            pixel[i, j] = BLACK if sum(pixel[i, j])/3 < thresh else WHITE

def findRects(pixel, size, thresh=400):
    """
    Find and mark connected sets by drawing a bounding box only if the resulted box contains no less than thresh pixels.
    """
    w, h = size
    rects = []
    area = lambda r : (r[1]-r[0])*(r[3]-r[2])
    for i in range(w):
        for j in range(h):
            if(pixel[i, j] == BLACK):
                r = findRect(pixel, size, i, j)
                if(area(r) >= thresh):
                    rects.append(r)
    return rects

def findRect(pixel, size, i, j):
    """
    Find and return the bounding box containing the pixel (i, j).
    """
    w, h = size
    discovered = set()
    discovered.add((i, j))
    neighbors = lambda (x, y) : [(nx, ny) for nx in range(x-1, x+2) for ny in range(y-1, y+2)]
    
    rect = [i, i, j, j]
    while(len(discovered) > 0):
        x, y = discovered.pop()
        pixel[x, y] = (1, 1, 1)
        rect[0] = min(x, rect[0])
        rect[1] = max(x, rect[1])
        rect[2] = min(y, rect[2])
        rect[3] = max(y, rect[3])
        
        for nx, ny in neighbors((x, y)):
            if(nx >= 0 and nx < w and ny >= 0 and ny < h and pixel[nx, ny] == BLACK):
                    discovered.add((nx, ny))
    
    return rect


def drawRects(pixel, rects, color=(255, 0, 0)):
    """
    Draw a rectangle in color.
    """
    for left, right, top, bottom in rects:
        for x in range(left, right+1):
            pixel[x, top] = color
            pixel[x, bottom] = color
        for y in range(top, bottom+1):
            pixel[left, y] = color
            pixel[right, y] = color


def closeness(pixel, A, B):
    """
    Return the closeness of two rectangles based on num_same_pixels / total_pixel
    """
    wA, hA = A[1]-A[0]+1, A[3]-A[2]+1
    wB, hB = B[1]-B[0]+1, B[3]-B[2]+1
    if(wA > 1.2*wB or wA < 0.8*wB or hA > 1.2*hB or hA < 0.8*hB):
        return 0
    w, h = min(wA, wB), min(hA, hB)
    
    total = 0
    samePixels = 0
    for x in range(w):
        for y in range(h):
            if(pixel[A[0]+x, A[2]+y] == BLACK or pixel[B[0]+x, B[2]+y] == BLACK):
                total += 1
                if(pixel[A[0]+x, A[2]+y] == pixel[B[0]+x, B[2]+y]):
                    samePixels += 1
                    
    return samePixels/float(total)


def findMatches(pixel, rects, thresh = 0.8):
    """
    Find most matching pairs whose closeness factor is no less than thresh.
    """
    matches = {}

    def addMatches(all, A, B, close):
        for m in all:
            if(abs(close - m) < 1e-4):
                all[m] += [A, B]
                return
        all[close] = [A, B]

    for i in range(len(rects)):
        for j in range(i+1, len(rects)):
            A, B = rects[i], rects[j]
            close = closeness(pixel, A, B)
            if(close > thresh):
                addMatches(matches, A, B, close)
                
    return matches

def main():
    import sys
    SOURCE_FILE = sys.argv[1] if len(sys.argv) > 1 else "sample.png"
    print SOURCE_FILE
    WB_FILE = "binary.png"
    RECT_FILE = "rect.png"
    DEST_FILE = "match.png"

    img = Image.open(SOURCE_FILE)
    rgb2wb(img.load(), img.size)
    img.save(WB_FILE)

    thresh = 400
    rects = findRects(img.load(), img.size, thresh)
    print "find %d rectangles that may be interested. (area >= %d)" % (len(rects), thresh)

    drawRects(img.load(), rects)
    img.save(RECT_FILE)

    img = Image.open(WB_FILE)
    matches = findMatches(img.load(), rects, 0.65)
    similarity = max(matches.keys())
    print "find %d sets of matches! The most matching set has a similarity of %.2f." % (len(matches), similarity)
    for k in matches:
        print k
        drawRects(img.load(), matches[k], (randint(0, 220), randint(0, 220), randint(0, 220)))
    img.save(DEST_FILE)


if __name__ == "__main__":
    main()



# def markConnectedSets(pixel, size):
#     """
#     find all sets of connected black pixels, mark pixels in the same set in same color.
#     """
#     w, h = size
#     sets = []
#     for i in range(w):
#         for j in range(h):
#             if(pixel[i, j] == BLACK):
#                 color = (randint(0, 220), randint(0, 220), randint(0, 220))
#                 sets.append(markSet(pixel, size, i, j, color))
#     return sets

# def markSet(pixel, size, i, j, color):
#     """
#     find all black pixels connected to (i, j) and mark then in color.
#     """
#     w, h = size
#     discovered = set()
#     visited = set()    
#     discovered.add((i, j))
#     neighbors = lambda (x, y) : [(nx, ny) for nx in range(x-1, x+2) for ny in range(y-1, y+2)]
    
#     while(len(discovered) > 0):
#         x, y = discovered.pop()
#         pixel[x, y] = color
#         for nx, ny in neighbors((x, y)):
#             if(nx >= 0 and nx < w and ny >= 0 and ny < h and pixel[nx, ny] == BLACK):
#                     discovered.add((nx, ny))
#         visited.add((nx, ny))
#     return visited



