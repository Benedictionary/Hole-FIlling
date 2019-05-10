import numpy
import matplotlib.pyplot as mplplt
import matplotlib.image as mplimg


##Upload Images to Test

'''
#Test Image
img = numpy.array([[0,0,0,0,0,0,1,0,0],
                   [0,0,0,0,0,0,0,0,0],
                   [0,0,1,1,1,1,1,1,0],
                   [1,0,1,0,0,0,0,1,0],
                   [0,0,1,0,0,0,0,1,0],
                   [0,0,1,1,1,1,1,1,0],
                   [0,0,0,0,0,0,0,0,0],
                   [0,0,1,0,0,0,0,0,0]])
'''
#Spells out CPP as a binaru image
img = numpy.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0],
                   [0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0],
                   [0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0],
                   [0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                   [0,0,1,1,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
'''
#Takes forever to compute with my implementation for the following image, but it works
img = mplimg.imread(r'BinaryImg2.jpg') 

def rgb2gray(image):
    imgNew = numpy.dot(image[...,:3], [0.2126, 0.7152, 0.0722])
    return imgNew

img = rgb2gray(img)/255.0
img = numpy.around(img)
img = img.astype(int)
'''
#Function for Displaying Binary Images with a title
def displayImg(img, title):
    img = img.astype(int)
    mplplt.imshow(img, cmap='gray')
    mplplt.title(title)
    mplplt.show()

##Display Original Image
displayImg(img, 'Original Image I(x,y)')

#Generate a mask of the image
maskImg = 1- img

##Display Mask
displayImg(maskImg, 'Mask Ic(x,y)')

#Function for making a marker of the image
def markerImage(img):
    imgXSize, imgYSize = numpy.shape(img)
    markerImg = numpy.zeros((imgXSize,imgYSize))
    for x in range(0,imgXSize):
        for y in range(0, imgYSize):
            if (x == 0 or y == 0 or x == imgXSize-1 or y == imgYSize-1):
                markerImg[x,y] = 1-img[x,y]
            else:
                markerImg[x,y] = 0
    return markerImg
markerImg = markerImage(img)

#Display the Marker
displayImg(markerImg, 'Marker F(x,y)')

BKernal = numpy.ones((3,3))

#Function for Padding the Image for Convolution
def padImage(img):
    padOneSideX = 1
    padOneSideY = 1
    paddedImg = numpy.lib.pad(img, ((padOneSideY,padOneSideY),(padOneSideX,padOneSideX)), 'constant', constant_values=0) #paddedImg = numpy.lib.pad(a, ((5,5), (2,2)), 'constant', constant_values=0)  # numpy.int finds integer floor of argument
    return paddedImg

#Function for Padding the Image for Convolution
def unpad1(img):
    imgXSize,imgYSize = numpy.shape(img)
    imgUnpad = numpy.delete(img, imgYSize-1, 1)
    imgUnpad = numpy.delete(imgUnpad, imgXSize-1, 0)
    imgUnpad = numpy.delete(imgUnpad, 0, 0)
    imgUnpad = numpy.delete(imgUnpad, 0, 1)
    return imgUnpad

#Function for Handling the elementwise Multiplication for the Convolution. Optimized for binary images
def convMult(Frame, matrix, sideMax, x, y):
    imgFiltEntry = 0.0
    for i in range(0, 3):
        for j in range (0, 3):
            imgFiltEntry = imgFiltEntry + matrix[j,i]*Frame[x-sideMax+j, y-sideMax+i]
            if imgFiltEntry > 0.0:
                break
        if imgFiltEntry > 0.0:
            break
    return imgFiltEntry

#A function for Generating the Convolution for the binary image
def convolution(matrix, Frame):
    imgXSize, imgYSize = numpy.shape(Frame)
    padFrame = padImage(Frame)
    sideMax = 1
    imgFilt = numpy.zeros((imgXSize + 2, imgYSize + 2)) * 1.0  # creates the zeroed out "canvas" that our filtered Image will be on
    imgXSize, imgYSize = numpy.shape(imgFilt)
    for x in range(1,imgXSize-1):
        for y in range (1, imgYSize-1):
            convCheck = convMult(padFrame, matrix, sideMax, x, y) #each element of the convoluted Image is computed with convMult()
            if convCheck >= 0.5:
                imgFilt[x, y] = 1
        #displayImg(imgFilt, "imgtest")

    imgFilt = unpad1(imgFilt)
    return imgFilt

#Obtain the Complement
fillPrevious = markerImg

iterations = 0 #Keeps track of the number of times we fill the holes

#Lets fill the holes by dilating the frame with the kernal and then finding the intersection between it and the complement of the image
while 1==1:
    fill = convolution(BKernal, fillPrevious) * maskImg
    iterations += 1
    if numpy.all(fillPrevious == fill):
       break
    else: fillPrevious = fill

#Generate Complement
fill= 1-fill

print("Total Iterations: ", iterations)
displayImg(fill, 'Final')
