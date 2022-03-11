# -*- coding: utf-8 -*-
import cv2 as cv
from datetime import datetime
import os

import sys
sys.path.append('.')
import electionConfiguration
import readVote
import imprimeResultado

# Diretórios
ver = '/v1.0'
saida = '/Output/'

# O diretótio '/Output/' e '/v1.0/ são criados caso não existam
if not os.path.isdir(os.getcwd() + ver):
    os.mkdir(os.getcwd() + ver)
if not os.path.isdir(os.getcwd() + ver + saida):
    os.mkdir(os.getcwd() + ver + saida)

# TODO: Adicionar verificação de existencia de arquivo
cap = cv.VideoCapture(os.getcwd() + ver + saida +
    'Totalizacao--Zona_256-Secao_1-Data2021-10-13_20-46-30.avi')

# Executa a configuração da eleição
config, qtd_cargos = electionConfiguration.configElection()
cargos, linhas, campos = electionConfiguration.readConfigFile(config, qtd_cargos)

# Inicializa mapas de votação
votos = list()
for i in range(qtd_cargos):
    votos.append({})

while(cap.isOpened()):
    ret, img = cap.read()
    
    if(ret):
        # cv.imshow('frame',img)
        # cv.waitKey(0)

        # Lê os votos da boleta atual
        tupla_votos = readVote.run2(img, campos)

        # Contabiliza os votos da boleta
        for i in range(qtd_cargos):
            key = tupla_votos[i]
            votos[i][key] = votos[i][key] + \
                1 if key in votos[i] else 1
        # if cv.waitKey(0) & 0xFF == ord('q'):
            #break
    else:
        break

cap.release()
cv.destroyAllWindows()

for i in range(qtd_cargos):
    imprimeResultado.run(votos[i], cargos[i])
