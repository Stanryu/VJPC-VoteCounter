import cv2 as cv
import os

fourcc = cv.VideoWriter_fourcc('M','J','P','G')

img1 = cv.imread('boletaBranca(1).jpg')
img2 = cv.imread('boletaBranca(1).jpg')
img3 = cv.imread('boletaBranca(1).jpg')

boletas = ['boletaBranca(1).jpg','boletaBranca(1).jpg','boletaBranca(1).jpg']
height , width , layers =  img1.shape
print height , width

video = cv.VideoWriter('video.avi',fourcc,1,(922,873))
for boleta in boletas:
    img = cv.imread(boleta)
    cv.imshow('titulo', img)
    cv.waitKey(0)
    video.write(img)


cv.destroyAllWindows()
video.release()
