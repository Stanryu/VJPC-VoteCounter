# -*- coding: utf-8 -*-
import os
import readVote
import imprimeResultado
import cv2 as cv


totalVotosPresidente = {}
totalVotosDeputado = {}
urna = '/UrnaFisica/'
boletas = os.listdir(os.getcwd()+urna)
for boleta in boletas:
    img = cv.imread(os.getcwd()+urna + boleta)
    img_g = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    pre, dep = readVote.run2(img, img_g)
    totalVotosPresidente[pre] = totalVotosPresidente[pre] + \
        1 if pre in totalVotosPresidente else 1
    totalVotosDeputado[dep] = totalVotosDeputado[dep] + \
        1 if dep in totalVotosDeputado else 1

imprimeResultado.run(totalVotosPresidente, 'Presidente')
imprimeResultado.run(totalVotosDeputado, 'Deputado')
