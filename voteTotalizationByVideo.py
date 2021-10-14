# -*- coding: utf-8 -*-
import cv2 as cv
import sys
import time
from datetime import datetime
import readVote
import os
import imprimeResultado


# TODO: Adicionar verificação de existencia de arquivo
cap = cv.VideoCapture(
    'Totalizacao--Zona_256-Secao_1-Data2021-10-13_20-46-30.avi')

totalVotosPresidente = {}
totalVotosDeputado = {}

while(cap.isOpened()):
    ret, img = cap.read()
    if(ret):
        img_gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        # cv.imshow('frame',img)
        # cv.waitKey(0)
        presidente, deputado = readVote.run2(img, img_gray)

        totalVotosPresidente[presidente] = totalVotosPresidente[presidente] + \
            1 if presidente in totalVotosPresidente else 1
        totalVotosDeputado[deputado] = totalVotosDeputado[deputado] + \
            1 if deputado in totalVotosDeputado else 1
        # if cv.waitKey(0) & 0xFF == ord('q'):
        #     break
    else:
        break

cap.release()
cv.destroyAllWindows()

imprimeResultado.run(totalVotosPresidente, 'Presidente')
imprimeResultado.run(totalVotosDeputado, 'Deputado')
