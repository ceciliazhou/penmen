from PIL import Image
from math import sqrt

BLACK = '*'
WHITE = ' '

def image2matrix(image, thresh = 128):
    w, h = image.size
    pixel = image.load()
    info = [ [BLACK if sum(pixel[i, j])/3 < thresh else WHITE for j in range(h)] for i in range(w) ]
    # info = [ [sum(pixel[i, j])/3 for j in range(h)] for i in range(w) ]
    return info


def expand(matrix, i, j, area):
    w, h = len(matrix), len(matrix[0])
    if i < 0 or j < 0 or i >= w or j >= h or (matrix[i][j] == WHITE):
        return

    area[0] = min(area[0], i) #updtopAe left
    area[1] = max(area[1], i) #updtopAe right
    area[3] = max(area[3], j) #updtopAe bottom
    matrix[i][j] = WHITE

    expand(matrix, i+1, j, area) 
    expand(matrix, i+1, j, area) 
    expand(matrix, i, j+1, area) 


def getRegions(matrix):
    w, h = len(matrix), len(matrix[0])
    # w, h = len(matrix)/20, len(matrix[0])/20
    # result = []
    for i in  range(w):
        for j in range(h):
            if(matrix[i][j] == BLACK):
                region = [i, i, j, j] #left, right, top, bottom
                expand(matrix, i, j, region)
                yield region
    #             result.append(region)
    # return result

def mark(pixel, region):
    left, right, top, bottom = region
    for i in range(left, right+1):
        pixel[i, top] = (255, 0, 0)
        pixel[i, bottom] = (255, 0, 0)
    for j in range(top, bottom+1):
        pixel[left, j] = (255, 0, 0)
        pixel[right, j] = (255, 0, 0)


def splitImage(image, regions):
    pixel = image.load()
    for region in regions:
        mark(pixel, region)
    image.save("test.png")

def main():
    im = Image.open("penmen.png")
    matrix = image2matrix(im)
    regions = getRegions(matrix)
    splitImage(im, regions)

main()

# def distance(p1, p2):
#     diffX, diffY = p1[0] - p2[0], p1[1] - p2[1]
#     return sqrt(diffX*diffX + diffY*diffY)

# def closeEnough(rectA, rectB, thresh = 2):
#     leftA, rightA, topA, bottomA = rectA
#     leftB, rightB, topB, bottomB = rectB
#     dist = 1000000
#     if(leftA in range(leftB, rightB) or rightA in range(leftB, rightB)): 
#         dist = min(abs(topA - bottomB), abs(bottomA - topB))
#     elif(topA in range(topB, bottomB) or bottomA in range(topB, bottomB)):
#         dist = min(abs(rightA - leftA), abs(leftA - rightB))
#     else:
#         points = (((rectA[x], rectA[y+2]), (rectB[1-x], rectB[3-y])) for x in range(2) for y in range(2))
#         dist = min((distance(p[0], p[1]) for p in points))
#     return dist < thresh

# def merge(rect, rects):
#     for r in rects:
#             if(closeEnough(rect, r)):
#                 r[0] = min(rect[0], r[0])
#                 r[1] = max(rect[1], r[1])
#                 r[2] = min(rect[2], r[2])
#                 r[3] = max(rect[3], r[3])
#                 return True
#     return False

# def process(rects):
#     result = []
#     for r in rects:
#         if not (merge(r, result)):
#             result.append(r)
#     return result