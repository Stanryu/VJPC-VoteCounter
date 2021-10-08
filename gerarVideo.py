#-*- coding: utf-8 -*-
import cv2 as cv
import sys
import time
from datetime import datetime
import readVote
import os
import imprimeResultado

zona = '256'
secao = "1"
nFrames = 30
now = datetime.now()
saida =  (str(now.date()) +'_'+ str(now.hour)+'-'+str(now.minute)+'-'+str(now.second)+'_' + zona + '_' + secao +'.avi')
saida = 'saida.avi'
fourcc = cv.VideoWriter_fourcc('M','J','P','G')

urna = '/UrnaFisica/'
boletas = os.listdir(os.getcwd()+urna)
img = cv.imread(os.getcwd()+urna+boletas[0])
height , width , layers =  img.shape

out = cv.VideoWriter(saida, fourcc, nFrames, (width, height))

for boleta in boletas:
    img = cv.imread(os.getcwd()+urna+boleta)
    out.write(img)

cv.destroyAllWindows()
out.release()



cap = cv.VideoCapture('saida.avi')

totalVotosPresidente = {}
totalVotosDeputado = {}

while(cap.isOpened()):
    ret, img = cap.read()
    if(ret):
        img_vini = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        # cv.imshow('frame',img)
        # cv.waitKey(0)
        # cv.imshow('frame',img_vini)
        pre, dep = readVote.run2(img, img_vini)
        #print pre, dep
        totalVotosPresidente[pre] = totalVotosPresidente[pre]+1 if totalVotosPresidente.has_key(pre) else 1
        totalVotosDeputado[dep] = totalVotosDeputado[dep]+1 if totalVotosDeputado.has_key(dep) else 1
        if cv.waitKey(0) & 0xFF == ord('q'):
            break
    else: break

cap.release()
cv.destroyAllWindows()

imprimeResultado.run(totalVotosPresidente, 'Presidente')
imprimeResultado.run(totalVotosDeputado, 'Deputado')

print
