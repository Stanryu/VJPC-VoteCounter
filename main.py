#-*- coding: utf-8 -*-
import cv2 as cv
import sys
import time
from datetime import datetime


zona = '256'
secao = "1"
camera_port = 0
nFrames = 30.0
emLoop = True

camera = cv.VideoCapture(camera_port)
fourcc = cv.VideoWriter_fourcc('M','J','P','G')
now = datetime.now()
saida =  (str(now.date()) +'_'+ str(now.hour)+'-'+str(now.minute)+'-'+str(now.second)+'_' + zona + '_' + secao +'.avi')

out = cv.VideoWriter(saida, fourcc, nFrames, (640,480))

if not camera.isOpened():
    print('Nao foi possivel abrir a web cam.')
    sys.exit(-1)

while(emLoop):
    retval, img = camera.read()
    if retval == True:
        out.write(img)
        cv.imshow('Foto', img)
        print ".",
    else:
        print('Oops! A captura falhou.')
        break

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

print('Captura encerrada.')

camera.release()
out.release()
cv.destroyAllWindows()