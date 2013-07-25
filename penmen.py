from PIL import Image
from random import randint


def rgb2binary(image, thresh = 110):
    w, h = image.size
    pixel = image.load()
    for i in range(w):
        for j in range(h):
            pixel[i,j] = (0, 0, 0) if sum(pixel[i, j])/3 < thresh else (255, 255, 255)

def neighbors(x, y, dist = 1):
    return [(nx, ny) for nx in range(x-dist, x+dist+1) for ny in range(y-dist, y+dist+1)]

def markBlock(pixel, i, j, w, h, color):
    S = set()
    S.add((i, j))
    while len(S) > 0:
        x, y = S.pop()
        pixel[x, y] = color
        for nx, ny in neighbors(x, y):
            if(nx >= 0 and nx < w and ny >= 0 and ny < h and pixel[nx, ny] == (0, 0, 0)):
                S.add((nx, ny))

def mark(image):
    pixel = image.load()
    w, h = image.size
    for i in range(w):
        for j in range(h):
            if(pixel[i, j] == (0, 0, 0)):
                markBlock(pixel, i, j, w, h, (randint(0, 220), randint(0, 220), randint(0, 220)))
    image.save("test.png")

def main():
    im = Image.open("penmen.png")
    rgb2binary(im)
    mark(im)

main()

