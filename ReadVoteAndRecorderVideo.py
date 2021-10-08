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

totalVotosPresidente = {}
totalVotosDeputado = {}

for boleta in boletas:
    img = cv.imread(os.getcwd()+urna+boleta)
    out.write(img)
    img_g = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    pre, dep = readVote.run2(img, img_g)

    totalVotosPresidente[pre] = totalVotosPresidente[pre]+1 if totalVotosPresidente.has_key(pre) else 1
    totalVotosDeputado[dep] = totalVotosDeputado[dep]+1 if totalVotosDeputado.has_key(dep) else 1


cv.destroyAllWindows()
out.release()

imprimeResultado.run(totalVotosPresidente, 'Presidente')
imprimeResultado.run(totalVotosDeputado, 'Deputado')

print
