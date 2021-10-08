# -*- coding: utf-8 -*-
import os
import glob
import readVote
import imprimeResultado
import cv2 as cv

# print glob.glob('UrnaFisica/*')
totalVotosPresidente = {}
totalVotosDeputado = {}
urna = '/UrnaFisica/'
boletas = os.listdir(os.getcwd()+urna)
for boleta in boletas:
    pre, dep = readVote.run(os.getcwd()+urna+boleta)
    totalVotosPresidente[pre] = totalVotosPresidente[pre]+1 if totalVotosPresidente.has_key(pre) else 1
    totalVotosDeputado[dep] = totalVotosDeputado[dep]+1 if totalVotosDeputado.has_key(dep) else 1
    #break

imprimeResultado.run(totalVotosPresidente, 'Presidente')
imprimeResultado.run(totalVotosDeputado, 'Deputado')

print
# print rankingPresidente
# print rankingdeputado
